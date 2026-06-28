<template>
  <div class="view">
    <!-- Back -->
    <RouterLink to="/" class="back-link">← Kembali</RouterLink>

    <!-- Loading awal -->
    <div v-if="loadingEmp" class="loading-full">Memuat data karyawan…</div>

    <template v-else-if="empData">
      <!-- Header karyawan -->
      <div class="view-header">
        <div class="emp-hero">
          <div class="emp-avatar emp-avatar--lg">{{ initials(empData.nama_dummy) }}</div>
          <div>
            <h1 class="view-title">{{ empData.nama_dummy }}</h1>
            <p class="view-sub">{{ empData.id_karyawan }} · {{ empData.unit_kerja }} · {{ empData.jenis_pekerjaan }}</p>
          </div>
        </div>
      </div>

      <!-- Metric cards -->
      <div class="metric-row">
        <MetricCard label="Usia" :value="`${empData.usia} tahun`" />
        <MetricCard label="BMI" :value="`${empData.BMI}`" :tone="bmiTone(empData.BMI)" />
        <MetricCard label="Tekanan Darah" :value="`${empData.sistolik}/${empData.diastolik}`" :tone="tdTone(empData.sistolik)" />
        <MetricCard label="Gula Darah Puasa" :value="`${empData.gula_darah_puasa} mg/dL`" />
        <MetricCard label="Kolesterol" :value="`${empData.kolesterol_total} mg/dL`" />
        <MetricCard label="HbA1c" :value="`${empData.HbA1c}%`" />
      </div>

      <!-- Tabs data MCU -->
      <div class="tabs">
        <button
          v-for="tab in ['Vital Sign', 'Lab Darah', 'Riwayat']"
          :key="tab"
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === tab }"
          @click="activeTab = tab"
        >{{ tab }}</button>
      </div>

      <div class="tab-content card">
        <template v-if="activeTab === 'Vital Sign'">
          <DataRow label="Tinggi Badan" :value="`${empData.tinggi_badan_cm} cm`" />
          <DataRow label="Berat Badan" :value="`${empData.berat_badan_kg} kg`" />
          <DataRow label="Lingkar Perut" :value="`${empData.lingkar_perut_cm} cm`" />
          <DataRow label="Nadi" :value="`${empData.nadi} bpm`" />
          <DataRow label="SpO2" :value="`${empData.SpO2}%`" />
          <DataRow label="Status EKG" :value="empData.status_EKG" />
          <DataRow label="Spirometri" :value="empData.status_spirometri" />
        </template>
        <template v-else-if="activeTab === 'Lab Darah'">
          <DataRow label="Gula Darah Puasa" :value="`${empData.gula_darah_puasa} mg/dL`" />
          <DataRow label="HbA1c" :value="`${empData.HbA1c}%`" />
          <DataRow label="Kolesterol Total" :value="`${empData.kolesterol_total} mg/dL`" />
          <DataRow label="HDL" :value="`${empData.HDL} mg/dL`" />
          <DataRow label="LDL" :value="`${empData.LDL} mg/dL`" />
          <DataRow label="Trigliserida" :value="`${empData.trigliserida} mg/dL`" />
          <DataRow label="SGOT" :value="`${empData.SGOT} U/L`" />
          <DataRow label="SGPT" :value="`${empData.SGPT} U/L`" />
          <DataRow label="Kreatinin" :value="`${empData.kreatinin} mg/dL`" />
          <DataRow label="eGFR" :value="`${empData.eGFR} mL/min`" />
          <DataRow label="Asam Urat" :value="`${empData.asam_urat} mg/dL`" />
        </template>
        <template v-else>
          <DataRow label="Riwayat Pribadi" :value="empData.riwayat_penyakit_pribadi" />
          <DataRow label="Riwayat Keluarga" :value="empData.riwayat_penyakit_keluarga" />
          <DataRow label="Obat Rutin" :value="empData.obat_rutin" />
          <DataRow label="Alergi" :value="empData.alergi_makanan" />
          <DataRow label="Status Merokok" :value="empData.status_merokok" />
        </template>
      </div>

      <!-- Tombol rekomendasi -->
      <div class="rec-trigger">
        <button
          class="btn btn--primary"
          :disabled="loadingRec"
          @click="generateRec"
        >
          {{ loadingRec ? 'Menyusun rekomendasi…' : '✦ Buat Rekomendasi AI' }}
        </button>
        <p v-if="error" class="alert alert--error">{{ error }}</p>
      </div>

      <!-- Hasil rekomendasi -->
      <RecommendationPanel v-if="recData" :data="recData" />
    </template>

    <div v-else-if="error" class="alert alert--error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useApi } from '../composables/useApi'
import MetricCard from '../components/MetricCard.vue'
import DataRow from '../components/DataRow.vue'
import RecommendationPanel from '../components/RecommendationPanel.vue'

const route = useRoute()
const { loading: loadingEmp, error, fetchEmployee } = useApi()
const { loading: loadingRec, fetchRecommendationById } = useApi()

const empData = ref(null)
const recData = ref(null)
const activeTab = ref('Vital Sign')

function initials(name) {
  return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

function bmiTone(bmi) {
  if (bmi < 18.5 || (bmi >= 25 && bmi < 30)) return 'warning'
  if (bmi >= 30) return 'danger'
  return 'success'
}

function tdTone(sistolik) {
  if (sistolik >= 140) return 'danger'
  if (sistolik >= 130) return 'warning'
  return 'success'
}

async function generateRec() {
  const res = await fetchRecommendationById(route.params.id)
  if (res) recData.value = res
}

onMounted(async () => {
  const res = await fetchEmployee(route.params.id)
  if (res) empData.value = res.data
})
</script>
