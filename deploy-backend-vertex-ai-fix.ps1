#!/usr/bin/env pwsh
# =============================================================================
# Deploy Backend with Vertex AI Configuration
# =============================================================================

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "DEPLOYING BACKEND WITH VERTEX AI FIX" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

Write-Host "🔧 Configuration:" -ForegroundColor Yellow
Write-Host "   - USE_VERTEX_AI=true (enforced)" -ForegroundColor Green
Write-Host "   - Default in settings.py changed to True" -ForegroundColor Green
Write-Host "   - Dockerfile sets USE_VERTEX_AI=true" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Starting deployment..." -ForegroundColor Yellow
Write-Host ""

try {
    $deployCmd = "gcloud run deploy legalmind-backend " +
                "--source=backend " +
                "--project=legalmind-486106 " +
                "--region=us-central1 " +
                "--allow-unauthenticated " +
                "--set-env-vars=USE_VERTEX_AI=true " +
                "--platform=managed " +
                "--quiet"
    
    Write-Host "Command: $deployCmd" -ForegroundColor Gray
    Write-Host ""
    
    Invoke-Expression $deployCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=" * 80 -ForegroundColor Green
        Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
        Write-Host "=" * 80 -ForegroundColor Green
        Write-Host ""
        Write-Host "🧪 Test the fix:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "   curl https://legalmind-backend-677928716377.us-central1.run.app/health" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Expected: HTTP 200 with Vertex AI configured" -ForegroundColor Gray
        Write-Host "No more 403 errors about 'generativelanguage.googleapis.com'" -ForegroundColor Gray
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "❌ Deployment failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        Write-Host ""
    }
}
catch {
    Write-Host ""
    Write-Host "❌ Error during deployment:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "📋 What Was Fixed:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Changed default use_vertex_ai from False → True" -ForegroundColor White
Write-Host "2. Changed USE_VERTEX_AI env var default from 'false' → 'true'" -ForegroundColor White
Write-Host "3. Added USE_VERTEX_AI=true to Dockerfile" -ForegroundColor White
Write-Host "4. Explicitly set USE_VERTEX_AI=true in Cloud Run deployment" -ForegroundColor White
Write-Host ""
Write-Host "This ensures the backend ALWAYS uses Vertex AI (aiplatform.googleapis.com)" -ForegroundColor White
Write-Host "instead of the public Gemini API (generativelanguage.googleapis.com)" -ForegroundColor White
Write-Host ""
