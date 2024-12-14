import { createApp } from 'vue'
import App from './ui/App.vue'
import { router } from './ui/router'
import pinia from './ui/stores'
import 'virtual:uno.css'

createApp(App)
  .use(pinia)
  .use(router)
  .mount('#app')
