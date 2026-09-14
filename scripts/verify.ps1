$ErrorActionPreference = "Stop"

Write-Host "Checking Docker services..." -ForegroundColor Cyan
docker compose ps

Write-Host "`nChecking frontend..." -ForegroundColor Cyan
(Invoke-WebRequest "http://localhost/" -UseBasicParsing).StatusCode

Write-Host "Checking FastAPI..." -ForegroundColor Cyan
(Invoke-WebRequest "http://localhost/api/v1/status/" -UseBasicParsing).Content

Write-Host "Checking AI..." -ForegroundColor Cyan
(Invoke-WebRequest "http://localhost/api/v1/ai/status" -UseBasicParsing).Content

Write-Host "`nPlatform verification complete." -ForegroundColor Green
