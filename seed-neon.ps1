# Заполняет удалённую Postgres (Neon) тем же сидом, что и в manage.py seed_mcu.
# Создай neon_database_url.txt — одна строка: postgresql://... (как в Render / Neon). Файл в .gitignore.

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$urlFile = Join-Path $root "neon_database_url.txt"

if (-not (Test-Path $urlFile)) {
    Write-Host "Создай файл $urlFile с одной строкой DATABASE_URL из Neon/Render, затем запусти снова." -ForegroundColor Yellow
    exit 1
}

$raw = (Get-Content -LiteralPath $urlFile -Raw -Encoding UTF8).Trim()
if ($raw -notmatch "postgres") {
    Write-Host "В файле должна быть строка подключения Postgres (postgresql://...)" -ForegroundColor Red
    exit 1
}

$env:DATABASE_URL = $raw
Set-Location $root
python manage.py migrate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python manage.py seed_mcu
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Готово. Обнови сайт на Render — фильмы должны отображаться." -ForegroundColor Green
