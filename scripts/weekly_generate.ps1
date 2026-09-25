# UC Work Search Report Generator - Windows Version
# Usage: powershell -ExecutionPolicy Bypass -File scripts\weekly_generate.ps1 [-LastWeek]
# =============================================================================

param(
    [switch]$LastWeek,
    [string]$OutputPath = $CUSTOM_OUTPUT_PATH,
    [string]$DbPath = "data/raw/job_tracker.db"
)

# Set error handling
$ErrorActionPreference = "Stop"

# Calculate paths from script location
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "PA UC Work Search Report Generator" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Project Root: $PROJECT_ROOT"

# Change to project root
Set-Location $PROJECT_ROOT

# =============================================================================
# 1. Determine Week Start Date
# =============================================================================
if ($LastWeek) {
    $CurrentDate = Get-Date
    $DaysSinceMonday = $CurrentDate.DayOfWeek.value__
    $WeekStart = $CurrentDate.AddDays(-7 - $DaysSinceMonday).ToString('yyyy-MM-dd')
    Write-Host "Last Week Start: $WeekStart" -ForegroundColor Yellow
} else {
    $CurrentDate = Get-Date
    $DaysSinceMonday = $CurrentDate.DayOfWeek.value__
    $WeekStart = $CurrentDate.AddDays(-$DaysSinceMonday).ToString('yyyy-MM-dd')
    Write-Host "Current Week Start: $WeekStart" -ForegroundColor Green
}

$WeekEnd = (Get-Date $WeekStart).AddDays(6).ToString('yyyy-MM-dd')
Write-Host "Week End: $WeekEnd"

# =============================================================================
# 2. Activate Virtual Environment
# =============================================================================
$vEnvActivatePath = Join-Path $PROJECT_ROOT ".venv\Scripts\Activate.ps1"

if (Test-Path $vEnvActivatePath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Gray
    & $vEnvActivatePath
} else {
    Write-Host "[X] Virtual environment not found at: $vEnvActivatePath" -ForegroundColor Red
    Write-Host "Run: python -m venv .venv && pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# =============================================================================
# 3. Validate Prerequisites
# =============================================================================
$RequiredPaths = @(
    "src/generate_weekly_report.py",
    "templates/html/work_search_template.html",
    $DbPath
)

foreach ($path in $RequiredPaths) {
    if (-not (Test-Path $path)) {
        Write-Host "[X] Required file missing: $path" -ForegroundColor Red
        exit 1
    }
}

Write-Host "[+] All prerequisites validated" -ForegroundColor Green

# =============================================================================
# 4. Generate Output Path
# =============================================================================
if ([string]::IsNullOrEmpty($OutputPath)) {
    $OutputDir = Join-Path $PROJECT_ROOT "outputs"
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    }
    $PdfOutput = Join-Path $OutputDir "work_search_report_$WeekStart.pdf"
} else {
    $PdfOutput = Join-Path $PROJECT_ROOT $OutputPath
}

Write-Host "Output PDF: $PdfOutput"

# =============================================================================
# 5. Run Python Generator
# =============================================================================
try {
    Write-Host "Generating report..." -ForegroundColor Cyan
    
    # Build argument list
    $arguments = @(
        "src/generate_weekly_report.py",
        "--week-start", $WeekStart,
        "--db-path", $DbPath
    )
    
    if ([string]::IsNullOrEmpty($OutputPath)) {
        $arguments += "--output"
        $arguments += "outputs/work_search_report_$WeekStart.pdf"
    }
    
    # Execute
    & python $arguments
    
    # Verify output was created
    if (Test-Path $PdfOutput) {
        $FileSize = (Get-Item $PdfOutput).Length
        Write-Host "[+] Success! Generated: $PdfOutput" -ForegroundColor Green
        Write-Host "   File Size: $('{0:N0}' -f $FileSize) bytes" -ForegroundColor Gray
        
        # Open file automatically (optional)
        $openFile = Read-Host "`nOpen PDF preview? (Y/N)"
        if ($openFile -eq 'Y' -or $openFile -eq 'y') {
            Start-Process $PdfOutput
        }
    } else {
        Write-Host "[X]  PDF generation may have failed - file not found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[X] Error occurred during generation:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host "`nStack Trace:" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace
    exit 1
}

# =============================================================================
# 6. Cleanup Summary
# =============================================================================
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Report generation complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick Links:" -ForegroundColor Gray
Write-Host "  • View PDF: $PdfOutput" -ForegroundColor White
Write-Host "  • Submit at: www.uc.pa.gov" -ForegroundColor White
Write-Host "  • View database: sqlite3 $DbPath" -ForegroundColor White
Write-Host ""
