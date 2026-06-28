<template>
  <div class="app">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-brand">
        <div class="brand-icon">⚕</div>
        <div>
          <div class="brand-name">Health AI</div>
          <div class="brand-sub">Pertamina</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <RouterLink to="/" class="nav-item" active-class="nav-item--active">
          <span class="nav-icon">◫</span> Dashboard
        </RouterLink>
        <RouterLink to="/input-manual" class="nav-item" active-class="nav-item--active">
          <span class="nav-icon">✎</span> Input Manual
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="api-badge" :class="apiStatus.ok ? 'api-badge--ok' : 'api-badge--off'">
          <span class="api-dot"></span>
          {{ apiStatus.ok ? 'API Terhubung' : 'API Offline' }}
        </div>
      </div>
    </aside>

    <!-- Main -->
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const apiStatus = ref({ ok: false })

onMounted(async () => {
  try {
    const res = await fetch(
      (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/'
    )
    apiStatus.value.ok = res.ok
  } catch {
    apiStatus.value.ok = false
  }
})
</script>
