"""
Health AI — FastAPI Backend
Jalankan dengan: uvicorn api:app --reload --port 8000
"""
from __future__ import annotations

import os
from typing import Any, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from health_data import build_health_profile, normalize_raw_data, load_data
from llm_client import build_prompt, call_openrouter, estimate_message_tokens, local_recommendation
from settings import DEFAULT_MODEL

# ── App ────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Pertamina Health AI API",
    description="Backend rekomendasi kesehatan berbasis LLM",
    version="1.0.0",
)

def get_allowed_origins() -> list[str]:
    raw_origins = os.getenv("CORS_ORIGINS", "")
    if raw_origins:
        return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]


# ── CORS — izinkan Vue dev server dan domain produksi ─────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Schema Input ───────────────────────────────────────────────────────────
class MCUInput(BaseModel):
    id_karyawan: str = "EMP000"
    nama_dummy: str = "Karyawan Baru"
    usia: int = 35
    jenis_kelamin: str = "L"
    unit_kerja: str = "tidak_ada"
    jenis_pekerjaan: str = "Kantor"
    tanggal_mcu: str = "2026-01-01"
    tinggi_badan_cm: float = 170
    berat_badan_kg: float = 70
    BMI: float = 0
    lingkar_perut_cm: float = 85
    sistolik: int = 120
    diastolik: int = 80
    nadi: int = 76
    SpO2: float = 98
    gula_darah_puasa: float = 90
    HbA1c: float = 5.3
    kolesterol_total: float = 180
    HDL: float = 50
    LDL: float = 110
    trigliserida: float = 120
    SGOT: float = 25
    SGPT: float = 30
    kreatinin: float = 1.0
    eGFR: float = 100
    asam_urat: float = 5.5
    status_EKG: str = "normal"
    status_rontgen_thorax: str = "normal"
    status_spirometri: str = "normal"
    riwayat_penyakit_pribadi: str = "tidak_ada"
    riwayat_penyakit_keluarga: str = "tidak_ada"
    obat_rutin: str = "tidak_ada"
    alergi_makanan: str = "tidak_ada"
    status_merokok: str = "tidak"


# ── Helper ─────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    return os.getenv("OPENROUTER_API_KEY", "")

def get_model() -> str:
    return os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)

def input_to_series(data: MCUInput) -> pd.Series:
    raw_df = pd.DataFrame([data.model_dump()])
    normalized = normalize_raw_data(raw_df)
    return normalized.iloc[0]

def build_result(row: pd.Series, source: str, model: Optional[str],
                 recommendation: dict, token_usage: Optional[dict]) -> dict:
    from health_data import build_health_profile
    profile = build_health_profile(row)
    return {
        "source": source,
        "model": model,
        "token_usage": token_usage,
        "profile": {
            "bmi": round(float(row["BMI"]), 1),
            "bmi_category": profile.bmi_category,
            "risk_level": profile.risk_level,
            "main_focus": profile.main_focus,
            "constraints": profile.constraints,
            "red_flags": profile.red_flags,
        },
        "recommendation": recommendation,
    }


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "service": "Pertamina Health AI API", "version": "1.0.0"}


@app.get("/employees")
def list_employees():
    """Daftar semua karyawan dari data dummy."""
    try:
        raw, _ = load_data()
        employees = raw[["id_karyawan", "nama_dummy", "usia", "jenis_kelamin", "unit_kerja"]].to_dict(orient="records")
        return {"data": employees, "total": len(employees)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/employees/{emp_id}")
def get_employee(emp_id: str):
    """Detail satu karyawan dari data dummy."""
    try:
        raw, _ = load_data()
        row_df = raw[raw["id_karyawan"] == emp_id]
        if row_df.empty:
            raise HTTPException(status_code=404, detail=f"Karyawan {emp_id} tidak ditemukan.")
        return {"data": row_df.iloc[0].to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/profile")
def get_profile(data: MCUInput):
    """Hitung profil risiko saja (rule-based, tanpa LLM)."""
    try:
        row = input_to_series(data)
        profile = build_health_profile(row)
        messages = build_prompt(row, profile)
        return {
            "bmi": round(float(row["BMI"]), 1),
            "bmi_category": profile.bmi_category,
            "risk_level": profile.risk_level,
            "main_focus": profile.main_focus,
            "constraints": profile.constraints,
            "red_flags": profile.red_flags,
            "estimated_tokens": estimate_message_tokens(messages),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recommend")
def get_recommendation(data: MCUInput):
    """Rekomendasi AI lengkap dari input manual. Fallback lokal jika tidak ada API key."""
    try:
        row = input_to_series(data)
        profile = build_health_profile(row)
        messages = build_prompt(row, profile)

        api_key = get_api_key()
        model = get_model()
        source = "local"
        token_usage = None
        recommendation = None

        if api_key:
            try:
                recommendation, tu = call_openrouter(messages, model, api_key)
                source = "openrouter"
                token_usage = {
                    "estimated_input": tu.estimated_input_tokens,
                    "prompt_tokens": tu.prompt_tokens,
                    "completion_tokens": tu.completion_tokens,
                    "total_tokens": tu.total_tokens,
                }
            except Exception as llm_err:
                recommendation = local_recommendation(row, profile)
                source = "local_fallback"
                token_usage = {"error": str(llm_err)}
        else:
            recommendation = local_recommendation(row, profile)

        return build_result(row, source, model if source == "openrouter" else None,
                            recommendation, token_usage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/employees/{emp_id}/recommend")
def recommend_by_id(emp_id: str):
    """Shortcut: rekomendasi langsung dari ID karyawan dummy."""
    try:
        raw, _ = load_data()
        row_df = raw[raw["id_karyawan"] == emp_id]
        if row_df.empty:
            raise HTTPException(status_code=404, detail=f"Karyawan {emp_id} tidak ditemukan.")

        row = row_df.iloc[0]
        profile = build_health_profile(row)
        messages = build_prompt(row, profile)

        api_key = get_api_key()
        model = get_model()
        source = "local"
        token_usage = None

        if api_key:
            try:
                recommendation, tu = call_openrouter(messages, model, api_key)
                source = "openrouter"
                token_usage = {
                    "prompt_tokens": tu.prompt_tokens,
                    "completion_tokens": tu.completion_tokens,
                    "total_tokens": tu.total_tokens,
                }
            except Exception:
                recommendation = local_recommendation(row, profile)
                source = "local_fallback"
        else:
            recommendation = local_recommendation(row, profile)

        return build_result(row, source, model if source == "openrouter" else None,
                            recommendation, token_usage)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
