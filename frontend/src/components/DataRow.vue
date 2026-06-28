<!-- DataRow.vue -->
<template>
  <div class="data-row">
    <span class="data-label">{{ label }}</span>
    <span class="data-value">{{ value }}</span>
  </div>
</template>
<script setup>
defineProps({ label: String, value: [String, Number] })
</script>
