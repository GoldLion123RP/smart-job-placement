import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// Plugin to copy required files for GitHub Pages
function copyGitHubPagesFiles() {
  return {
    name: 'copy-github-pages-files',
    closeBundle() {
      const fs = require('fs')
      const distPath = resolve(__dirname, 'dist')
      
      // Create .nojekyll to prevent Jekyll processing
      fs.writeFileSync(resolve(distPath, '.nojekyll'), '')
      
      // Create custom 404.html for SPA routing
      fs.writeFileSync(resolve(distPath, '404.html'), `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Redirecting...</title>
    <script>
      window.location.href = '/smart-job-placement/'
    </script>
  </head>
  <body>
    <p>Redirecting to <a href="/smart-job-placement/">homepage</a>...</p>
  </body>
</html>`)
    }
  }
}

export default defineConfig({
  plugins: [react(), copyGitHubPagesFiles()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  base: '/smart-job-placement/',
})
