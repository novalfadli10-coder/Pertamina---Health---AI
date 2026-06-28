import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import EmployeeDetail from './views/EmployeeDetail.vue'
import ManualInput from './views/ManualInput.vue'
import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/karyawan/:id', component: EmployeeDetail },
    { path: '/input-manual', component: ManualInput },
  ],
})

createApp(App).use(router).mount('#app')
