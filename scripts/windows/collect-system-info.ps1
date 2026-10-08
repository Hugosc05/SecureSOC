# SecureSOC - collect-system-info.ps1
# READ-ONLY: queries versions and resources. Installs, downloads or changes nothing.
# Usage: powershell -ExecutionPolicy Bypass -File .\scripts\windows\collect-system-info.ps1
# Output: scripts\windows\system-info.txt (contains no secrets; review before sharing)

$ErrorActionPreference = 'SilentlyContinue'
$out = Join-Path $PSScriptRoot 'system-info.txt'
$lines = New-Object System.Collections.Generic.List[string]
function Add($t) { $lines.Add([string]$t) }
function Section($t) { Add ''; Add "=== $t ===" }
function Ver($name, $cmd) {
    $c = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($c) {
        $v = (& $cmd --version 2>&1 | Select-Object -First 1)
        Add ("{0,-10} {1}" -f $name, $v)
    } else {
        Add ("{0,-10} NOT FOUND" -f $name)
    }
}

Add "SecureSOC system report - $(Get-Date -Format s)"
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Add "Run as admin: $isAdmin"

Section 'Windows'
$os = Get-CimInstance Win32_OperatingSystem
Add "Caption: $($os.Caption)"
Add "Version: $($os.Version)  Build: $($os.BuildNumber)"
$cv = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
Add "EditionID: $($cv.EditionID)  DisplayVersion: $($cv.DisplayVersion)"

Section 'CPU / RAM'
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
Add "CPU: $($cpu.Name.Trim())"
Add "Cores: $($cpu.NumberOfCores)  Logical: $($cpu.NumberOfLogicalProcessors)"
Add "VirtualizationFirmwareEnabled: $($cpu.VirtualizationFirmwareEnabled)"
$ram = (Get-CimInstance Win32_PhysicalMemory | Measure-Object Capacity -Sum).Sum
Add ("RAM installed: {0} GB" -f [math]::Round($ram / 1GB, 1))
Add ("RAM free now: {0} GB" -f [math]::Round($os.FreePhysicalMemory * 1KB / 1GB, 1))

Section 'Disks'
Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -ne $null } | ForEach-Object {
    Add ("{0}:  free {1} GB / total {2} GB" -f $_.Name, [math]::Round($_.Free / 1GB, 1), [math]::Round(($_.Used + $_.Free) / 1GB, 1))
}

Section 'GPU'
Get-CimInstance Win32_VideoController | ForEach-Object { Add "Adapter: $($_.Name)  DriverVersion: $($_.DriverVersion)" }
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used --format=csv 2>&1 | ForEach-Object { Add $_ }
} else { Add 'nvidia-smi NOT FOUND' }

Section 'Virtualization / WSL'
$cs = Get-CimInstance Win32_ComputerSystem
Add "HypervisorPresent: $($cs.HypervisorPresent)"
if ($isAdmin) {
    foreach ($f in 'Microsoft-Hyper-V-All', 'VirtualMachinePlatform', 'Microsoft-Windows-Subsystem-Linux', 'HypervisorPlatform') {
        $s = Get-WindowsOptionalFeature -Online -FeatureName $f
        Add ("Feature {0}: {1}" -f $f, $(if ($s) { $s.State } else { 'n/a' }))
    }
} else { Add 'Optional features: (run as admin to see)' }
if (Get-Command wsl -ErrorAction SilentlyContinue) {
    Add '--- wsl --version'
    (wsl --version 2>&1) -replace "`0", '' | Where-Object { $_.Trim() } | ForEach-Object { Add $_ }
    Add '--- wsl -l -v'
    (wsl -l -v 2>&1) -replace "`0", '' | Where-Object { $_.Trim() } | ForEach-Object { Add $_ }
} else { Add 'wsl NOT FOUND' }
$wslcfg = Join-Path $env:USERPROFILE '.wslconfig'
Add ".wslconfig exists: $(Test-Path $wslcfg)"

Section 'Tool versions'
Ver 'git' 'git'
Ver 'python' 'python'
if (Get-Command py -ErrorAction SilentlyContinue) { Add '--- py -0p'; py -0p 2>&1 | ForEach-Object { Add $_ } }
Ver 'uv' 'uv'
Ver 'node' 'node'
Ver 'npm' 'npm'
Ver 'docker' 'docker'
if (Get-Command docker -ErrorAction SilentlyContinue) { Add ("compose    " + (docker compose version 2>&1 | Select-Object -First 1)) }
Ver 'ollama' 'ollama'
Ver 'code' 'code'

Section 'Relevant installed software'
$keys = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
        'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*'
Get-ItemProperty $keys | Where-Object { $_.DisplayName -match 'VMware|VirtualBox|Docker|Ollama|Python|Node\.js|Git|PostgreSQL|NVIDIA Graphics Driver' } |
    Sort-Object DisplayName -Unique | ForEach-Object { Add ("{0}  {1}" -f $_.DisplayName, $_.DisplayVersion) }

Section 'Ports in use (relevant)'
foreach ($p in 3000, 5432, 8000, 11434) {
    $c = Get-NetTCPConnection -LocalPort $p -State Listen
    Add ("Port {0}: {1}" -f $p, $(if ($c) { "IN USE (PID $($c[0].OwningProcess))" } else { 'free' }))
}

$lines | Set-Content -Path $out -Encoding UTF8
Write-Host "Report written to $out"
