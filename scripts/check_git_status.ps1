# Git Status Checker for Windows

Write-Host "=== Git Repository Status ===" -ForegroundColor Cyan

# Current branch and status
Write-Host "`nCurrent Status:" -ForegroundColor Yellow
git status

# Remote configuration
Write-Host "`nRemote Configuration:" -ForegroundColor Yellow
git remote -v

# Branch tracking
Write-Host "`nBranch Tracking:" -ForegroundColor Yellow
git branch -vv

# Check for divergence
Write-Host "`nRemote Changes Analysis:" -ForegroundColor Yellow

git fetch origin 2>$null

$remoteAhead = git log HEAD..origin/main --oneline 2>$null
$localAhead = git log origin/main..HEAD --oneline 2>$null

if ($remoteAhead -and $localAhead) {
    Write-Host "`n[X] DIVERGENT HISTORY DETECTED" -ForegroundColor Red
    Write-Host "  Remote has commits you don't have:" -ForegroundColor Gray
    $remoteAhead | ForEach-Object { Write-Host "    $_" }
    Write-Host "  You have commits remote doesn't have:" -ForegroundColor Gray
    $localAhead | ForEach-Object { Write-Host "    $_" }
    Write-Host "`n[i] Recommended: git pull --rebase origin main && git push" -ForegroundColor Green
} elseif ($remoteAhead) {
    Write-Host "`n[i] Remote has updates. Run: git pull --rebase origin main" -ForegroundColor Yellow
} elseif ($localAhead) {
    Write-Host "`n[i] You have unpushed commits. Ready to push!" -ForegroundColor Green
} else {
    Write-Host "`n[+] Up to date with remote" -ForegroundColor Green
}

# Check required files
Write-Host "`nProject Structure Check:" -ForegroundColor Yellow
$files = @(".gitignore", "README.md", "requirements.txt", "src/", "templates/")
$missing = $false
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  [+] $file" -ForegroundColor Green
    } else {
        Write-Host "  [X] $file MISSING" -ForegroundColor Red
        $missing = $true
    }
}

if ($missing) {
    Write-Host "`n[i]  Some files are missing. Run initial setup if this is a fresh clone." -ForegroundColor Yellow
} else {
    Write-Host "`n[+] Project structure looks good!" -ForegroundColor Green
}