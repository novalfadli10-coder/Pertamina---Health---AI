<!-- MetricCard.vue -->
<template>
  <div class="metric-card" :class="`metric-card--${tone}`">
    <div class="metric-label">{{ label }}</div>
    <div class="metric-value">{{ value }}</div>
  </div>
</template>
<script setup>
defineProps({ label: String, value: String, tone: { type: String, default: 'default' } })
</script>
