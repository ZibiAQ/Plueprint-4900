Param(
  [string]$AppName = "PluePrint",
  [string]$Entry = "main.py"
)

$ErrorActionPreference = "Stop"

Write-Host "Building $AppName..."

python -m pip install --upgrade pip | Out-Null
python -m pip install -r "requirements.txt"

if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

python -m PyInstaller `
  --name "$AppName" `
  --onefile `
  --windowed `
  --clean `
  "$Entry"

Write-Host ""
Write-Host "Done. EXE is at: dist\$AppName.exe"

