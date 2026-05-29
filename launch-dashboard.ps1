$env:GRAPH_DIR = "D:\AWS\Legal"
$dashboardDir = "C:\Users\Mohammad\.understand-anything-plugin\packages\dashboard"

Write-Host "Starting knowledge graph dashboard..." -ForegroundColor Cyan
Write-Host "Project: $env:GRAPH_DIR" -ForegroundColor Gray
Write-Host ""

Set-Location $dashboardDir
npx vite --host 127.0.0.1
