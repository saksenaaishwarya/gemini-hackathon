@echo off
setlocal enabledelayedexpansion

cd /d "c:\Users\surya\OneDrive\Desktop\suryansh\coding_projects\gemini-hackathon"

echo Organizing root directory...
echo.

:: Move documentation files to docs/
echo Moving documentation files to docs/...
for %%f in (
    FIX_SUMMARY.md
    VERTEX_AI_FIX_STATUS.md
    IMPLEMENTATION_CHECKLIST.md
    SOLUTION_COMPLETE.md
    START_HERE.md
    VISUAL_SUMMARY.txt
    QUICK_REFERENCE.md
    DEPLOYMENT_COMPLETE.md
    RALPH_LOOP_COMPLETE.md
) do (
    if exist "%%f" (
        move /Y "%%f" "docs\" >nul 2>&1
        echo   Moved %%f
    )
)

:: Move deployment/setup scripts to scripts/
echo.
echo Moving deployment scripts to scripts/...
for %%f in (
    deploy-complete-fix.ps1
    deploy-complete-fix.sh
    deploy-firestore-rules.bat
    deploy_firestore_rules.py
    diagnose-deployment.ps1
    fix-vertex-ai-permissions.ps1
    fix-vertex-ai-permissions.sh
    setup-gcp.ps1
    setup-gcp.sh
    cloudbuild-backend.yaml
    cloudbuild-frontend.yaml
) do (
    if exist "%%f" (
        move /Y "%%f" "scripts\" >nul 2>&1
        echo   Moved %%f
    )
)

:: Move test scripts to tests/
echo.
echo Moving test scripts to tests/...
for %%f in (
    ralph-validation-loop.ps1
    ralph-final-validation.ps1
    test-fix.sh
    test-vertex-ai-fix.ps1
    check_deployment.py
) do (
    if exist "%%f" (
        move /Y "%%f" "tests\" >nul 2>&1
        echo   Moved %%f
    )
)

:: Remove temporary files
echo.
echo Removing temporary files...
for %%f in (
    ralph-final-validation-report-20260208-234338.txt
    ralph-validation-report-20260208-233658.txt
    build.log
    .Metrics.swp
) do (
    if exist "%%f" (
        del /F /Q "%%f" >nul 2>&1
        echo   Removed %%f
    )
)

echo.
echo Root directory cleanup complete!
echo.

pause
