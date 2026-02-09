#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Ralph Loop Final Verification - Complete Deployment Validation
    Final validation iteration confirming LegalMind is live and accessible
    with both frontend and backend services fully operational.
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$ProjectId = "legalmind-486106"
)

$BackendUrl = "https://legalmind-backend-677928716377.us-central1.run.app"
$FrontendUrl = "https://legalmind-frontend-677928716377.us-central1.run.app"
$reportDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "RALPH LOOP - FINAL VERIFICATION (ITERATION 8/8)" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

$report = @"
================================================================================
                LEGALMIND DEPLOYMENT - FINAL VALIDATION REPORT
                           Ralph Loop Iteration 8/8
================================================================================

Generated: $reportDate
Project ID: $ProjectId

================================================================================
DEPLOYMENT VERIFICATION
================================================================================

Testing Frontend: $FrontendUrl
Testing Backend: $BackendUrl

"@

# Test Frontend
Write-Host "Testing Frontend..." -ForegroundColor Yellow
$frontendStatus = "UNKNOWN"
try {
    $response = curl.exe -s -w "%{http_code}" -o /dev/null "$FrontendUrl" -m 10
    if ($response -eq "200") {
        Write-Host "[OK] Frontend is accessible - HTTP 200" -ForegroundColor Green
        $report += "[OK] Frontend HTTP Status: 200`n"
        $frontendStatus = "OK"
    } else {
        Write-Host "[!] Frontend returned HTTP $response" -ForegroundColor Yellow
        $report += "[!] Frontend HTTP Status: $response`n"
    }
} catch {
    Write-Host "[FAIL] Frontend connection failed" -ForegroundColor Red
    $report += "[FAIL] Frontend connection error`n"
}

# Test Backend Health
Write-Host "Testing Backend Health Endpoint..." -ForegroundColor Yellow
$backendHealthStatus = "UNKNOWN"
try {
    $response = curl.exe -s "$BackendUrl/health" -m 10
    if ($response) {
        Write-Host "[OK] Backend health check successful" -ForegroundColor Green
        $report += "[OK] Backend Health Check: $response`n"
        $backendHealthStatus = "OK"
    }
} catch {
    Write-Host "[FAIL] Backend health check failed" -ForegroundColor Red
    $report += "[FAIL] Backend health check error`n"
}

# Test Backend API Docs
Write-Host "Testing Backend API Documentation..." -ForegroundColor Yellow
$apiDocsStatus = "UNKNOWN"
try {
    $response = curl.exe -s -w "%{http_code}" -o /dev/null "$BackendUrl/docs" -m 10
    if ($response -eq "200") {
        Write-Host "[OK] API documentation is accessible - HTTP 200" -ForegroundColor Green
        $report += "[OK] API Docs HTTP Status: 200`n"
        $apiDocsStatus = "OK"
    } else {
        Write-Host "[!] API docs returned HTTP $response" -ForegroundColor Yellow
        $report += "[!] API Docs HTTP Status: $response`n"
    }
} catch {
    Write-Host "[!] API docs connection failed" -ForegroundColor Yellow
    $report += "[!] API Docs connection error`n"
}

$report += @"

================================================================================
PUBLIC URLS
================================================================================

Frontend (Next.js):
  $FrontendUrl

Backend API (FastAPI):
  $BackendUrl
  
API Documentation:
  $BackendUrl/docs

Health Check:
  $BackendUrl/health

================================================================================
DEPLOYMENT STATUS
================================================================================

Frontend:     $frontendStatus
Backend:      $backendHealthStatus
API Docs:     $apiDocsStatus

"@

if ($frontendStatus -eq "OK" -and $backendHealthStatus -eq "OK") {
    $report += @"
[SUCCESS] DEPLOYMENT COMPLETE!

Your LegalMind application is fully deployed and live on public URLs:

1. USERS ACCESS THE APPLICATION AT:
   $FrontendUrl

2. BACKEND API ACCESSIBLE AT:
   $BackendUrl

3. API DOCUMENTATION AVAILABLE AT:
   $BackendUrl/docs

4. FEATURES AVAILABLE:
   - AI-powered legal contract analysis
   - Risk assessment and scoring
   - Compliance verification (GDPR, HIPAA, CCPA, SOX)
   - Legal research and precedent analysis
   - Document generation
   - Real-time AI reasoning logs

5. TECHNOLOGY STACK:
   - Frontend:      Next.js 15.3 (TypeScript/React)
   - Backend:       FastAPI (Python 3.11+)
   - AI Model:      Google Gemini 2.0 Flash via Vertex AI
   - Database:      Firestore (real-time)
   - Storage:       Google Cloud Storage
   - Hosting:       Google Cloud Run (auto-scaling)

================================================================================
NEXT STEPS FOR USERS
================================================================================

1. Share the Frontend URL with users:
   $FrontendUrl

2. Users can immediately:
   - Upload contracts for analysis
   - Get AI-powered legal insights
   - View compliance reports
   - Export analysis results

3. For development/technical users:
   - API documentation at: $BackendUrl/docs
   - Swagger UI interactive testing available
   - OpenAPI spec at: $BackendUrl/openapi.json

================================================================================
TROUBLESHOOTING & MONITORING
================================================================================

Monitor Frontend Logs:
  gcloud run services logs read legalmind-frontend --project=$ProjectId --limit=50

Monitor Backend Logs:
  gcloud run services logs read legalmind-backend --project=$ProjectId --limit=50

View Service Status:
  gcloud run services describe legalmind-frontend --project=$ProjectId --region=us-central1
  gcloud run services describe legalmind-backend --project=$ProjectId --region=us-central1

"@

    Write-Host ""
    Write-Host "[SUCCESS] DEPLOYMENT VERIFIED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Frontend URL: $FrontendUrl" -ForegroundColor Cyan
    Write-Host "Backend URL:  $BackendUrl" -ForegroundColor Cyan
    Write-Host ""
}
else {
    $report += @"
[WARNING] Some services may not be fully responsive.

Please wait 30-60 seconds for services to fully initialize (cold start),
then re-run this validation script.

If problems persist, check logs:
  gcloud run services logs read legalmind-frontend --project=$ProjectId
  gcloud run services logs read legalmind-backend --project=$ProjectId

"@
    Write-Host "[WARNING] Some services may not be fully responsive" -ForegroundColor Yellow
}

Write-Host $report

# Save report
$reportPath = "ralph-final-validation-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
$report | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Report saved to: $reportPath" -ForegroundColor Green
Write-Host ""
