#requires -Version 5.1
$ErrorActionPreference = "Stop"
$workspace = "C:\Users\Administrator\.openclaw\workspace"
$statusFile = "$workspace\health\status.json"
Write-Host "=== 健康检查 ===" -ForegroundColor Cyan
$requiredDirs = @("memory\openclaw", "images", "ocr-results", "parsed-data\history", "logs")
$missing = 0
foreach ($dir in $requiredDirs) {
  if (-not (Test-Path "$workspace\$dir")) { $missing++ }
}
if ($missing -eq 0) { Write-Host "[PASS] 目录结构完整" -ForegroundColor Green } else { Write-Host "[FAIL] 缺失: $missing" -ForegroundColor Red }
if (Test-Path $statusFile) {
  $status = Get-Content $statusFile -Raw -Encoding UTF8 | ConvertFrom-Json
  $status.openclaw.status = "running"
  $status.openclaw.lastCheck = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
  $status | ConvertTo-Json | Set-Content $statusFile -Encoding UTF8
}
Write-Host "=== 完成 ===" -ForegroundColor Cyan
