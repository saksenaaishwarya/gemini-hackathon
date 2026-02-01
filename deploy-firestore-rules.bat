@echo off
REM Deploy Firestore Security Rules for LegalMind
REM Requires: Firebase CLI installed (npm install -g firebase-tools)

echo.
echo ============================================================
echo LegalMind Firestore Rules Deployment
echo ============================================================
echo.

REM Check if Firebase CLI is installed
firebase --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Firebase CLI is not installed
    echo Install it with: npm install -g firebase-tools
    exit /b 1
)

echo Firebase CLI found. Proceeding with deployment...
echo.

REM Deploy rules
echo Deploying Firestore security rules to legalmind-486106...
firebase deploy --only firestore:rules --project=legalmind-486106

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo SUCCESS! Firestore rules deployed.
    echo ============================================================
    echo.
    echo Your LegalMind app is now ready to use:
    echo - Frontend: http://localhost:3000
    echo - Backend:  http://localhost:8000
    echo - API Docs: http://localhost:8000/docs
    echo.
) else (
    echo.
    echo ERROR: Failed to deploy Firestore rules
    echo Check your Firebase CLI configuration and try again
    exit /b 1
)
