import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers'
import components from 'unplugin-vue-components/vite'

export function createComponents() {
  return components({
    dirs: ['src/ui/components'],
    resolvers: [AntDesignVueResolver({
      importStyle: 'css-in-js',
    })],
    include: [/\.vue$/, /\.vue\?vue/, /\.tsx$/],
    dts: './src/types/components.d.ts',
  })
}
