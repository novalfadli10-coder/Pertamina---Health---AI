<!-- RecList.vue -->
<template>
  <div v-if="items?.length" class="rec-list">
    <h4 class="rec-list-title">{{ icon }} {{ title }}</h4>
    <div v-for="(item, i) in items" :key="i" class="rec-item" :class="tone ? `rec-item--${tone}` : ''">
      {{ item }}
    </div>
  </div>
</template>
<script setup>
defineProps({ title: String, items: Array, icon: String, tone: String })
</script>
