<template>
  <div class="view">
    <div class="view-header">
      <div>
        <h1 class="view-title">Input Manual MCU</h1>
        <p class="view-sub">Masukkan data MCU secara manual untuk mendapatkan rekomendasi AI.</p>
      </div>
    </div>

    <div class="form-grid card">
      <!-- Identitas -->
      <div class="form-section">
        <h3 class="form-section-title">Identitas</h3>
        <div class="field-row">
          <FormField label="ID Karyawan" v-model="form.id_karyawan" />
          <FormField label="Nama" v-model="form.nama_dummy" />
          <FormField label="Usia" v-model.number="form.usia" type="number" />
        </div>
        <div class="field-row">
          <div class="field">
            <label class="field-label">Jenis Kelamin</label>
            <select v-model="form.jenis_kelamin" class="field-input">
              <option value="L">Laki-laki</option>
              <option value="P">Perempuan</option>
            </select>
          </div>
          <FormField label="Unit Kerja" v-model="form.unit_kerja" />
          <div class="field">
            <label class="field-label">Jenis Pekerjaan</label>
            <select v-model="form.jenis_pekerjaan" class="field-input">
              <option value="Kantor">Kantor</option>
              <option value="Lapangan">Lapangan</option>
              <option value="Shift">Shift</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Antropometri -->
      <div class="form-section">
        <h3 class="form-section-title">Antropometri & Vital Sign</h3>
        <div class="field-row">
          <FormField label="Tinggi (cm)" v-model.number="form.tinggi_badan_cm" type="number" />
          <FormField label="Berat (kg)" v-model.number="form.berat_badan_kg" type="number" />
          <FormField label="Lingkar Perut (cm)" v-model.number="form.lingkar_perut_cm" type="number" />
        </div>
        <div class="field-row">
          <FormField label="Sistolik (mmHg)" v-model.number="form.sistolik" type="number" />
          <FormField label="Diastolik (mmHg)" v-model.number="form.diastolik" type="number" />
          <FormField label="Nadi (bpm)" v-model.number="form.nadi" type="number" />
          <FormField label="SpO2 (%)" v-model.number="form.SpO2" type="number" />
        </div>
      </div>

      <!-- Lab -->
      <div class="form-section">
        <h3 class="form-section-title">Laboratorium</h3>
        <div class="field-row">
          <FormField label="Gula Darah Puasa" v-model.number="form.gula_darah_puasa" type="number" />
          <FormField label="HbA1c (%)" v-model.number="form.HbA1c" type="number" step="0.1" />
          <FormField label="Kolesterol Total" v-model.number="form.kolesterol_total" type="number" />
        </div>
        <div class="field-row">
          <FormField label="HDL" v-model.number="form.HDL" type="number" />
          <FormField label="LDL" v-model.number="form.LDL" type="number" />
          <FormField label="Trigliserida" v-model.number="form.trigliserida" type="number" />
        </div>
        <div class="field-row">
          <FormField label="SGOT" v-model.number="form.SGOT" type="number" />
          <FormField label="SGPT" v-model.number="form.SGPT" type="number" />
          <FormField label="Kreatinin" v-model.number="form.kreatinin" type="number" step="0.1" />
          <FormField label="eGFR" v-model.number="form.eGFR" type="number" />
          <FormField label="Asam Urat" v-model.number="form.asam_urat" type="number" step="0.1" />
        </div>
      </div>

      <!-- Riwayat -->
      <div class="form-section">
        <h3 class="form-section-title">Riwayat & Status</h3>
        <div class="field-row">
          <FormField label="Riwayat Penyakit Pribadi" v-model="form.riwayat_penyakit_pribadi" placeholder="cth: hipertensi;diabetes" />
          <FormField label="Riwayat Penyakit Keluarga" v-model="form.riwayat_penyakit_keluarga" />
        </div>
        <div class="field-row">
          <FormField label="Obat Rutin" v-model="form.obat_rutin" />
          <FormField label="Alergi Makanan" v-model="form.alergi_makanan" />
          <div class="field">
            <label class="field-label">Status Merokok</label>
            <select v-model="form.status_merokok" class="field-input">
              <option value="tidak">Tidak</option>
              <option value="pernah">Pernah</option>
              <option value="aktif">Aktif</option>
            </select>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn btn--primary" :disabled="loading" @click="submit">
          {{ loading ? 'Memproses…' : '✦ Buat Rekomendasi AI' }}
        </button>
      </div>
    </div>

    <p v-if="error" class="alert alert--error">{{ error }}</p>

    <RecommendationPanel v-if="recData" :data="recData" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useApi } from '../composables/useApi'
import FormField from '../components/FormField.vue'
import RecommendationPanel from '../components/RecommendationPanel.vue'

const { loading, error, fetchRecommendation } = useApi()
const recData = ref(null)

const form = ref({
  id_karyawan: 'EMP000',
  nama_dummy: '',
  usia: 35,
  jenis_kelamin: 'L',
  unit_kerja: '',
  jenis_pekerjaan: 'Kantor',
  tanggal_mcu: new Date().toISOString().slice(0, 10),
  tinggi_badan_cm: 170,
  berat_badan_kg: 70,
  BMI: 0,
  lingkar_perut_cm: 85,
  sistolik: 120,
  diastolik: 80,
  nadi: 76,
  SpO2: 98,
  gula_darah_puasa: 90,
  HbA1c: 5.3,
  kolesterol_total: 180,
  HDL: 50,
  LDL: 110,
  trigliserida: 120,
  SGOT: 25,
  SGPT: 30,
  kreatinin: 1.0,
  eGFR: 100,
  asam_urat: 5.5,
  status_EKG: 'normal',
  status_rontgen_thorax: 'normal',
  status_spirometri: 'normal',
  riwayat_penyakit_pribadi: 'tidak_ada',
  riwayat_penyakit_keluarga: 'tidak_ada',
  obat_rutin: 'tidak_ada',
  alergi_makanan: 'tidak_ada',
  status_merokok: 'tidak',
})

async function submit() {
  const res = await fetchRecommendation(form.value)
  if (res) {
    recData.value = res
    // scroll ke hasil
    setTimeout(() => {
      document.querySelector('.rec-panel')?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }
}
</script>
