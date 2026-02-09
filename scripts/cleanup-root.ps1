#!/usr/bin/env pwsh
# Root Directory Cleanup Script

$root = "c:\Users\surya\OneDrive\Desktop\suryansh\coding_projects\gemini-hackathon"
cd $root

Write-Host "Organizing root directory..." -ForegroundColor Cyan
Write-Host ""

# Move documentation files to docs/
Write-Host "Moving documentation files to docs/..." -ForegroundColor Yellow
$docFiles = @(
    "FIX_SUMMARY.md",
    "VERTEX_AI_FIX_STATUS.md",
    "IMPLEMENTATION_CHECKLIST.md",
    "SOLUTION_COMPLETE.md",
    "START_HERE.md",
    "VISUAL_SUMMARY.txt",
    "QUICK_REFERENCE.md",
    "DEPLOYMENT_COMPLETE.md",
    "RALPH_LOOP_COMPLETE.md"
)

foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs\" -Force
        Write-Host "  ✓ Moved $file" -ForegroundColor Green
    }
}

# Move deployment/setup scripts to scripts/
Write-Host ""
Write-Host "Moving deployment scripts to scripts/..." -ForegroundColor Yellow
$scriptFiles = @(
    "deploy-complete-fix.ps1",
    "deploy-complete-fix.sh",
    "deploy-firestore-rules.bat",
    "deploy_firestore_rules.py",
    "diagnose-deployment.ps1",
    "fix-vertex-ai-permissions.ps1",
    "fix-vertex-ai-permissions.sh",
    "setup-gcp.ps1",
    "setup-gcp.sh",
    "cloudbuild-backend.yaml",
    "cloudbuild-frontend.yaml"
)

foreach ($file in $scriptFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "scripts\" -Force
        Write-Host "  ✓ Moved $file" -ForegroundColor Green
    }
}

# Move test scripts to tests/
Write-Host ""
Write-Host "Moving test scripts to tests/..." -ForegroundColor Yellow
$testFiles = @(
    "ralph-validation-loop.ps1",
    "ralph-final-validation.ps1",
    "test-fix.sh",
    "test-vertex-ai-fix.ps1",
    "check_deployment.py"
)

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "tests\" -Force
        Write-Host "  ✓ Moved $file" -ForegroundColor Green
    }
}

# Remove temporary files
Write-Host ""
Write-Host "Removing temporary files..." -ForegroundColor Yellow
$tempFiles = @(
    "ralph-final-validation-report-20260208-234338.txt",
    "ralph-validation-report-20260208-233658.txt",
    "build.log",
    ".Metrics.swp",
    ".DS_Store"
)

foreach ($file in $tempFiles) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force
        Write-Host "  ✓ Removed $file" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "✅ Root directory cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Organized structure:" -ForegroundColor Cyan
Write-Host "  📁 docs/       - All documentation" -ForegroundColor Gray
Write-Host "  📁 scripts/    - Deployment and setup scripts" -ForegroundColor Gray
Write-Host "  📁 tests/      - Testing and validation scripts" -ForegroundColor Gray
Write-Host "  📁 backend/    - Backend code" -ForegroundColor Gray
Write-Host "  📁 frontend/   - Frontend code" -ForegroundColor Gray
Write-Host "  📄 README.md   - Main documentation" -ForegroundColor Gray
Write-Host "  📄 LICENSE.md  - License" -ForegroundColor Gray
Write-Host ""
