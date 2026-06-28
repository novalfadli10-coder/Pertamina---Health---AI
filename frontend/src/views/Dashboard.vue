<template>
  <div class="view">
    <!-- Header -->
    <div class="view-header">
      <div>
        <h1 class="view-title">Daftar Karyawan</h1>
        <p class="view-sub">Pilih karyawan untuk melihat profil dan rekomendasi kesehatan.</p>
      </div>
      <div class="header-stats" v-if="employees.length">
        <div class="stat-chip">{{ employees.length }} karyawan</div>
      </div>
    </div>

    <!-- Search -->
    <div class="search-bar">
      <input
        v-model="search"
        type="text"
        placeholder="Cari ID atau nama karyawan…"
        class="search-input"
      />
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert--error">⚠ {{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="loading-grid">
      <div v-for="n in 8" :key="n" class="card card--skeleton"></div>
    </div>

    <!-- Grid -->
    <div v-else class="employee-grid">
      <RouterLink
        v-for="emp in filtered"
        :key="emp.id_karyawan"
        :to="`/karyawan/${emp.id_karyawan}`"
        class="employee-card"
      >
        <div class="emp-avatar">{{ initials(emp.nama_dummy) }}</div>
        <div class="emp-info">
          <div class="emp-id">{{ emp.id_karyawan }}</div>
          <div class="emp-name">{{ emp.nama_dummy }}</div>
          <div class="emp-meta">
            {{ emp.usia }} th · {{ emp.jenis_kelamin }} · {{ emp.unit_kerja }}
          </div>
        </div>
        <div class="emp-arrow">→</div>
      </RouterLink>
    </div>

    <div v-if="!loading && filtered.length === 0 && !error" class="empty-state">
      Tidak ada karyawan yang cocok dengan "{{ search }}"
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useApi } from '../composables/useApi'

const { loading, error, fetchEmployees } = useApi()
const employees = ref([])
const search = ref('')

const filtered = computed(() => {
  if (!search.value) return employees.value
  const q = search.value.toLowerCase()
  return employees.value.filter(
    e =>
      e.id_karyawan.toLowerCase().includes(q) ||
      e.nama_dummy.toLowerCase().includes(q) ||
      e.unit_kerja.toLowerCase().includes(q)
  )
})

function initials(name) {
  return name
    .split(' ')
    .slice(0, 2)
    .map(w => w[0])
    .join('')
    .toUpperCase()
}

onMounted(async () => {
  const res = await fetchEmployees()
  if (res) employees.value = res.data
})
</script>
