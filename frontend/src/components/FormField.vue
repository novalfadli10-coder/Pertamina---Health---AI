<!-- FormField.vue -->
<template>
  <div class="field">
    <label class="field-label">{{ label }}</label>
    <input
      class="field-input"
      :type="type"
      :step="step"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', type === 'number' ? +$event.target.value : $event.target.value)"
    />
  </div>
</template>
<script setup>
defineProps({
  label: String,
  modelValue: [String, Number],
  type: { type: String, default: 'text' },
  step: { type: String, default: '1' },
  placeholder: String,
})
defineEmits(['update:modelValue'])
</script>
