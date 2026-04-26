import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    middlewareMode: false,
    proxy: {
      '/api': {
        target: 'https://ai-talent-scouting-agent-production.up.railway.app',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      }
    }
  }
})
