import { createRouter, createWebHistory } from 'vue-router/auto'
import { routes } from 'vue-router/auto-routes'

const history = createWebHistory()

export const router = createRouter({
  history,
  routes,
})

router.afterEach((to) => {
  const items = [import.meta.env.VITE_APP_TITLE]
  to.meta.title != null && items.unshift(to.meta.title)
  document.title = items.join(' · ')
})
