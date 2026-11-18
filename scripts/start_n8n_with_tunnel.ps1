# Starts a free Cloudflare quick tunnel and then n8n with WEBHOOK_URL pointing at it,
# so Telegram (Workflow C trigger) and email approval links can reach your local n8n.
# Usage: right-click > Run with PowerShell   (or: powershell -ExecutionPolicy Bypass -File start_n8n_with_tunnel.ps1)
# Note: a quick tunnel gets a NEW https address every time it starts; n8n re-registers the
# Telegram webhook automatically when it starts with the new WEBHOOK_URL.

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)  # repo root
$cf   = Join-Path $here 'tools\cloudflared.exe'
$log  = Join-Path $here 'tools\cloudflared.log'

# Stop an older tunnel / n8n if they are still running
Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force
Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
  Where-Object { $_.CommandLine -match 'n8n' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Start-Sleep -Seconds 2

if (Test-Path $log) { Remove-Item $log -Force }
Start-Process -FilePath $cf -ArgumentList "tunnel --no-autoupdate --url http://localhost:5678 --logfile `"$log`"" -WindowStyle Minimized

Write-Host 'Waiting for the tunnel address...'
$url = $null
for ($i = 0; $i -lt 60 -and -not $url; $i++) {
  Start-Sleep -Seconds 1
  if (Test-Path $log) {
    $m = Select-String -Path $log -Pattern 'https://[a-z0-9-]+\.trycloudflare\.com' | Select-Object -First 1
    if ($m) { $url = $m.Matches[0].Value }
  }
}
if (-not $url) { throw 'Tunnel did not start. See tools\cloudflared.log' }

Set-Content -Path (Join-Path $here 'tools\current_tunnel_url.txt') -Value $url
Write-Host "Public n8n address: $url"

$env:WEBHOOK_URL = "$url/"
$env:N8N_EDITOR_BASE_URL = 'http://localhost:5678'
Write-Host 'Starting n8n (keep this window open)...'
n8n start
