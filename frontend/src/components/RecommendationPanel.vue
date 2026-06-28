<template>
  <div class="rec-panel">
    <!-- Badge sumber -->
    <div class="rec-source">
      <span class="badge" :class="data.source === 'openrouter' ? 'badge--green' : 'badge--blue'">
        {{ data.source === 'openrouter' ? '✦ AI via OpenRouter' : '⚙ Rekomendasi Lokal' }}
      </span>
      <span v-if="data.source === 'openrouter' && data.model" class="badge badge--gray">
        {{ data.model }}
      </span>
    </div>

    <!-- Profil risiko -->
    <div class="risk-bar">
      <div class="risk-item">
        <span class="risk-label">IMT</span>
        <span class="chip" :class="`chip--${bmiTone(data.profile?.bmi_category)}`">
          {{ data.profile?.bmi_category }} ({{ data.profile?.bmi }})
        </span>
      </div>
      <div class="risk-item">
        <span class="risk-label">Risiko</span>
        <span class="chip" :class="`chip--${riskTone(data.profile?.risk_level)}`">
          {{ data.profile?.risk_level }}
        </span>
      </div>
    </div>

    <!-- Segmentasi AI -->
    <div v-if="rec.segmentasi_ai" class="segmentasi">
      <span class="seg-label">Segmentasi AI:</span>
      <strong>{{ rec.segmentasi_ai }}</strong>
    </div>

    <!-- Ringkasan -->
    <div class="rec-summary card">
      <h3 class="rec-card-title">Ringkasan Kondisi</h3>
      <p>{{ rec.ringkasan_kondisi }}</p>
    </div>

    <!-- Tabs rekomendasi -->
    <div class="tabs">
      <button
        v-for="tab in recTabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ 'tab-btn--active': activeTab === tab.key }"
        @click="activeTab = tab.key"
      >{{ tab.label }}</button>
    </div>

    <div class="tab-content card">
      <!-- Prioritas -->
      <template v-if="activeTab === 'prioritas'">
        <RecList title="Faktor Risiko Utama" :items="rec.faktor_risiko_utama" icon="⚠" />
        <RecList title="Prioritas" :items="rec.prioritas" icon="★" />
        <RecList title="Target 4 Minggu" :items="rec.target_4_minggu" icon="◎" />
      </template>

      <!-- Rencana -->
      <template v-else-if="activeTab === 'rencana'">
        <RecList title="Workout" :items="rec.rekomendasi_workout" icon="♜" />
        <RecList title="Makanan" :items="rec.rekomendasi_makanan" icon="✿" />
        <RecList title="Lifestyle" :items="rec.rekomendasi_lifestyle" icon="☀" />
        <!-- Task Harian -->
        <div v-if="rec.task_harian?.length" class="rec-list">
          <h4 class="rec-list-title">✦ Task Harian</h4>
          <div v-for="(task, i) in rec.task_harian" :key="i" class="task-card">
            <div class="task-header">
              <span class="task-name">{{ task.nama }}</span>
              <span class="badge badge--gray">{{ task.durasi }}</span>
              <span class="badge" :class="task.level === 'ringan' ? 'badge--green' : 'badge--blue'">
                {{ task.level }}
              </span>
            </div>
            <p v-if="task.alasan" class="task-reason">{{ task.alasan }}</p>
          </div>
        </div>
      </template>

      <!-- Safety -->
      <template v-else>
        <RecList title="Monitoring" :items="rec.monitoring" icon="◉" />
        <RecList title="Peringatan" :items="rec.peringatan" icon="⚑" tone="danger" />
        <div v-if="data.profile?.constraints?.length" class="rec-list">
          <h4 class="rec-list-title">🛡 Guardrail Keselamatan</h4>
          <div v-for="(c, i) in data.profile.constraints" :key="i" class="constraint-item">{{ c }}</div>
        </div>
      </template>
    </div>

    <!-- Token usage -->
    <div v-if="data.token_usage && data.source === 'openrouter'" class="token-info">
      <span>Input: {{ data.token_usage.prompt_tokens ?? '—' }} token</span>
      <span>Output: {{ data.token_usage.completion_tokens ?? '—' }} token</span>
      <span>Total: {{ data.token_usage.total_tokens ?? '—' }} token</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import RecList from './RecList.vue'

const props = defineProps({ data: Object })
const activeTab = ref('prioritas')

const recTabs = [
  { key: 'prioritas', label: 'Prioritas' },
  { key: 'rencana', label: 'Rencana Harian' },
  { key: 'safety', label: 'Monitoring' },
]

const rec = computed(() => props.data?.recommendation || {})

function bmiTone(cat) {
  if (!cat) return 'gray'
  if (cat === 'Normal') return 'green'
  if (cat === 'Underweight' || cat === 'Overweight') return 'yellow'
  return 'red'
}

function riskTone(level) {
  if (!level) return 'gray'
  if (level === 'Tinggi') return 'red'
  if (level === 'Sedang') return 'yellow'
  return 'green'
}
</script>
