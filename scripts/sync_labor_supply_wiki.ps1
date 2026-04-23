$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$wikiRoot = Join-Path $repoRoot "projects\labor_supply_wiki"
$buildDir = Join-Path $wikiRoot "site"
$targetDir = Join-Path $repoRoot "static\private\labor-supply-wiki-qv7m4t2x"
$staticRoot = Join-Path $repoRoot "static"

if (-not (Test-Path -LiteralPath $wikiRoot)) {
    throw "Wiki source folder not found at $wikiRoot"
}

$resolvedTargetDir = [System.IO.Path]::GetFullPath($targetDir)
$resolvedStaticRoot = [System.IO.Path]::GetFullPath($staticRoot)
if (-not $resolvedTargetDir.StartsWith($resolvedStaticRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to sync outside the website static directory."
}

Push-Location $wikiRoot
try {
    python build.py
}
finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $buildDir)) {
    throw "Wiki build output not found at $buildDir"
}

if (Test-Path -LiteralPath $targetDir) {
    Remove-Item -LiteralPath $targetDir -Recurse -Force
}

New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
Copy-Item -Path (Join-Path $buildDir "*") -Destination $targetDir -Recurse -Force

Write-Output "Synced labor supply wiki to $targetDir"
