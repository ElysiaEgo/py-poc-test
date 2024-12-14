import autoImport from 'unplugin-auto-import/vite'
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers'
import { VueRouterAutoImports } from 'unplugin-vue-router'

export function createAutoImport() {
  return autoImport({
    imports: [
      'vue',
      VueRouterAutoImports,
      'pinia',
    ],
    resolvers: [
      AntDesignVueResolver(),
    ],
    dts: './src/types/auto-imports.d.ts',
    dirs: [],
  })
}
