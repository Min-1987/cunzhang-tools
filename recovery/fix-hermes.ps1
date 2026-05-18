<#
.SYNOPSIS
  修复 Hermes 工作区问题
#>

$workspace = "C:\Users\Administrator\.openclaw\workspace"

Write-Host "🔧 修复 Hermes..." -ForegroundColor Cyan

# 1. 修复目录
$dirs = @("memory\hermes", "memory\shared")
foreach ($dir in $dirs) {
  $path = "$workspace\$dir"
  if (-not (Test-Path $path)) {
    New-Item -ItemType Directory -Path $path -Force | Out-Null
    Write-Host "  已创建: $dir"
  }
}

Write-Host "✅ Hermes 修复完成" -ForegroundColor Green
