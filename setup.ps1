<#
.SYNOPSIS
  Fill placeholders and generate local assets for the profile README.

.EXAMPLE
  .\setup.ps1 -Username JPG-Ayu -Name "Ayush Singh" -Image .\me.jpg -Circle
#>
[CmdletBinding()]
param(
  [string]$Username = "JPG-Ayu",
  [string]$Name = "Ayush Singh",
  [string]$Image,
  [int]$Cols = 88,
  [switch]$Circle,
  [switch]$Color
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding $false

function Replace-Text($file,$old,$new) {
  if (Test-Path $file) {
    $text=[System.IO.File]::ReadAllText($file,$utf8)
    [System.IO.File]::WriteAllText($file,$text.Replace($old,$new),$utf8)
  }
}

Replace-Text "$root\README.md" "YOUR_USERNAME" $Username
Replace-Text "$root\README.md" "YOUR NAME" $Name

python "$root\scripts\radar.py" --data "$root\assets\skills.json" -o "$root\assets\radar"
python "$root\scripts\radar.py" --github $Username -o "$root\assets\radar-langs"

if ($Image) {
  $argsList=@("$root\scripts\dotify.py",$Image,"-o","$root\assets\portrait","--cols",$Cols)
  if ($Circle) { $argsList += "--circle" }
  if ($Color)  { $argsList += "--color" }
  python @argsList
}

python "$root\scripts\cards.py" --user $Username --projects "$root\assets\projects.json" --out "$root\assets"

Write-Host "`nDone. Open preview.html, then push the repository to GitHub." -ForegroundColor Green
