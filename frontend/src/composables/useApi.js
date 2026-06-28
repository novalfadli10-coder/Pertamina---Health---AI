/**
 * useApi.js
 * Satu tempat untuk semua request ke FastAPI backend.
 * Ganti BASE_URL sesuai environment Anda.
 */
import { ref } from 'vue'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Request gagal')
  }
  return res.json()
}

// ── Composable ─────────────────────────────────────────────────────────────
export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  async function run(fn) {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (e) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  // Daftar semua karyawan
  function fetchEmployees() {
    return run(() => apiFetch('/employees'))
  }

  // Detail satu karyawan
  function fetchEmployee(id) {
    return run(() => apiFetch(`/employees/${id}`))
  }

  // Profil risiko saja (cepat, tanpa LLM)
  function fetchProfile(mcuData) {
    return run(() =>
      apiFetch('/profile', { method: 'POST', body: JSON.stringify(mcuData) })
    )
  }

  // Rekomendasi AI lengkap (dari data manual/upload)
  function fetchRecommendation(mcuData) {
    return run(() =>
      apiFetch('/recommend', { method: 'POST', body: JSON.stringify(mcuData) })
    )
  }

  // Shortcut: rekomendasi dari ID karyawan dummy
  function fetchRecommendationById(id) {
    return run(() => apiFetch(`/employees/${id}/recommend`))
  }

  return {
    loading,
    error,
    fetchEmployees,
    fetchEmployee,
    fetchProfile,
    fetchRecommendation,
    fetchRecommendationById,
  }
}
