import VueRouter from 'unplugin-vue-router/vite'

export function createVueRouter() {
  return VueRouter({
    routesFolder: './src/ui/pages',
    dts: './src/types/typed-router.d.ts',
  })
}
