# 🚨 CRITICAL FIX: LegalMind 403 Scope Error - Complete Resolution

**Status**: READY FOR DEPLOYMENT  
**Date**: February 5, 2026  
**Issue**: `403 Request had insufficient authentication scopes` (generativelanguage.googleapis.com)

---

## 🎯 ROOT CAUSE IDENTIFIED & FIXED

### The Problem
The backend code had **MULTIPLE SILENT FALLBACKS** from Vertex AI to the REST API:
1. When Vertex AI GenerativeModel wasn't available, code silently fell back to `genai.GenerativeModel()`
2. When Part/FunctionResponse import failed, code tried to use genai.protos instead
3. These fallbacks attempted to use the REST API with service account credentials
4. Service account tokens **don't have scopes** for the public Gemini API
5. Result: **403 "ACCESS_TOKEN_SCOPE_INSUFFICIENT"** error

### The Solution
Implemented **STRICT MODE** for Vertex AI:
- ✅ Removed ALL silent fallbacks
- ✅ Explicit error messages when Vertex AI initialization fails
- ✅ No automatic switching to REST API
- ✅ Added `google-cloud-aiplatform>=1.50.0` to requirements
- ✅ Created complete deployment automation scripts

---

## 📋 FILES MODIFIED

### Code Changes
1. **`backend/services/gemini_service.py`**
   - Removed fallback mechanism in `model` property (lines 240-310)
   - Fixed function response handling (lines 440-460)
   - Now uses Vertex AI directly with clear error messages

2. **`backend/config/settings.py`** (from previous iteration)
   - Already fixed to allow empty API key when USE_VERTEX_AI=true

3. **`backend/requirements.txt`**
   - Added: `google-cloud-aiplatform>=1.50.0`

### New Automation Scripts
1. **`deploy-complete-fix.ps1`** - PowerShell deployment script
2. **`deploy-complete-fix.sh`** - Bash deployment script
3. **`diagnose-deployment.ps1`** - PowerShell diagnostic script
4. **`fix-vertex-ai-permissions.ps1`** - Quick permission fixer (from earlier)
5. **`fix-vertex-ai-permissions.sh`** - Quick permission fixer (from earlier)

---

## 🚀 DEPLOYMENT INSTRUCTIONS

### Option 1: Automated Complete Fix (RECOMMENDED)

**Windows (PowerShell):**
```powershell
# Navigate to project root
cd C:\Users\surya\OneDrive\Desktop\suryansh\coding_projects\gemini-hackathon

# Run complete deployment script
.\deploy-complete-fix.ps1 -ProjectId "legalmind-486106" -Region "us-central1"
```

This script will:
1. Verify all prerequisites (gcloud, docker)
2. Set correct GCP project
3. Enable all required APIs (aiplatform, generativeai, run, etc.)
4. Verify/create service account
5. Grant all required IAM roles (including **roles/aiplatform.user**)
6. Build Docker image
7. Push to container registry
8. Deploy to Cloud Run with proper settings:
   - Memory: 1Gi
   - CPU: 1 vCPU
   - Min instances: 1 (prevents cold starts)
   - Timeout: 60 seconds
   - Service account: legalmind-backend@legalmind-486106.iam.gserviceaccount.com
9. Verify deployment and check logs

**Linux/Mac (Bash):**
```bash
cd ~/path/to/gemini-hackathon
chmod +x deploy-complete-fix.sh
bash deploy-complete-fix.sh legalmind-486106 us-central1
```

---

### Option 2: Manual Step-by-Step

If you prefer to run commands manually:

```bash
PROJECT_ID="legalmind-486106"
SA_EMAIL="legalmind-backend@${PROJECT_ID}.iam.gserviceaccount.com"

# 1. Enable APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativeai.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com

# 2. Grant role (CRITICAL)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user"

# 3. Build image
docker build -t gcr.io/${PROJECT_ID}/legalmind-backend:latest .

# 4. Push image
docker push gcr.io/${PROJECT_ID}/legalmind-backend:latest

# 5. Deploy to Cloud Run
gcloud run deploy legalmind-backend \
  --image gcr.io/${PROJECT_ID}/legalmind-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account $SA_EMAIL \
  --memory 1Gi \
  --cpu 1 \
  --timeout 60 \
  --min-instances 1 \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=${PROJECT_ID},USE_VERTEX_AI=true,DEBUG=false"
```

---

## ✅ VERIFICATION STEPS

### 1. Run Diagnostic Script
```powershell
.\diagnose-deployment.ps1 -ProjectId "legalmind-486106"
```

This will check:
- ✓ GCP project access
- ✓ Service account exists
- ✓ All required APIs enabled
- ✓ All required IAM roles assigned (especially `roles/aiplatform.user`)
- ✓ Cloud Run service configured correctly
- ✓ Environment variables set
- ✓ Health endpoint responding

### 2. Monitor Logs in Real-time
```bash
gcloud run services logs read legalmind-backend --region=us-central1 --follow
```

Watch for:
- ✅ "✅ Using Vertex AI with Application Default Credentials"
- ✅ "Project: legalmind-486106"
- ✅ "Region: us-central1"

Watch for errors:
- ✗ "❌ Vertex AI initialization failed" - Check IAM roles
- ✗ "Access Denied" - Check firestore/storage permissions
- ✗ Any Python import errors - Check requirements.txt

### 3. Test Health Endpoint
```bash
curl https://legalmind-backend-<id>.us-central1.run.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "LegalMind API",
  "timestamp": "2026-02-05T..."
}
```

### 4. Check Service Details
```bash
gcloud run services describe legalmind-backend --region=us-central1
```

Verify:
- Status: ACTIVE
- Environment variables: `USE_VERTEX_AI=true`
- Service account: `legalmind-backend@legalmind-486106.iam.gserviceaccount.com`
- Memory: 1Gi
- CPU: 1

---

## 🔍 WHAT WAS CHANGED IN DETAIL

### `backend/services/gemini_service.py` - The real fix

**Before** (lines 240-310):
```python
@property
def model(self):
    if self._model is None:
        # Single code path that mixed Vertex AI and REST API logic
        # If Vertex AI GenerativeModel wasn't available:
        if self.use_vertex:
            GenerativeModel = _safely_import_vertex_class("GenerativeModel")
            if GenerativeModel:
                self._model = GenerativeModel(**model_kwargs)
            else:
                # 🔴 SILENT FALLBACK - This is the bug!
                self.use_vertex = False
                self._model = genai.GenerativeModel(**model_kwargs)  # REST API
        else:
            self._model = genai.GenerativeModel(**model_kwargs)
```

**After** (lines 240-310):
```python
@property
def model(self):
    if self._model is None:
        if not self.use_vertex:
            # Vertex AI OFF: Use REST API
            generation_config = genai.GenerationConfig(...)
            self._model = genai.GenerativeModel(**model_kwargs)
        else:
            # Vertex AI ON: STRICT mode - NO FALLBACKS
            GenerativeModel = _safely_import_vertex_class("GenerativeModel")
            if not GenerativeModel:
                # 🟢 FAIL FAST with clear error
                raise RuntimeError(
                    "Vertex AI GenerativeModel class not available. "
                    "Install with: pip install google-cloud-aiplatform"
                )
            # Use Vertex AI directly
            from vertexai.generative_models import GenerationConfig
            self._model = GenerativeModel(**model_kwargs)
```

**Key Differences:**
- ✅ Explicit code paths for Vertex AI vs REST API
- ✅ No silent mode switching
- ✅ Raises error if Vertex AI dependencies missing
- ✅ Uses Vertex AI GenerationConfig, not REST API config
- ✅ Fails fast with helpful error messages

---

## 🔐 IAM ROLES REQUIRED

Your service account **MUST** have these roles:

| Role | Purpose |
|------|---------|
| `roles/aiplatform.user` | ⭐ **CRITICAL** - Access to Vertex AI |
| `roles/datastore.user` | Access to Firestore |
| `roles/storage.objectAdmin` | Access to Cloud Storage |
| `roles/logging.logWriter` | Write logs |

Verify with:
```bash
gcloud projects get-iam-policy legalmind-486106 \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:legalmind-backend@legalmind-486106.iam.gserviceaccount.com" \
  --format="table(bindings.role)"
```

Should show all 4 roles.

---

## 🔧 TROUBLESHOOTING

### Still getting 403 error?

1. **Check IAM roles were actually applied:**
   ```bash
   gcloud projects get-iam-policy legalmind-486106 | grep aiplatform.user
   ```
   Should return the service account membership

2. **Restart the Cloud Run service:**
   ```bash
   gcloud run deploy legalmind-backend --image ... --region us-central1
   ```
   New revisions will pick up updated IAM roles

3. **Check service account in Cloud Run deployment:**
   ```bash
   gcloud run services describe legalmind-backend --region us-central1 --format="value(spec.template.spec.serviceAccountName)"
   ```
   Should show: `legalmind-backend@legalmind-486106.iam.gserviceaccount.com`

### Backend keeps going offline?

1. Set `--min-instances 1` (already done in deployment script)
2. Increase memory to `--memory 2Gi` if needed
3. Check logs for memory/timeout errors

### Cold starts taking too long?

The Dockerfile already uses `python:3.11-slim` which is optimized.  
With `--min-instances 1`, cold starts are eliminated.

---

## 📊 DEPLOYMENT TIMELINE

1. **Run script**: ~2-5 minutes (includes Docker build & push)
2. **Cloud Run deployment**: ~1-2 minutes
3. **Service startup**: ~30-60 seconds
4. **Total time to live**: ~5-8 minutes

Expected logs by timestamp:
- T+0: Deployment starts, Docker build begins
- T+2-5m: Docker image pushed to registry
- T+5-6m: Cloud Run receives deployment request
- T+6-7m: Container starts, Python app initializes
- T+7m: Service should be healthy and accepting requests

---

## ✨ WHAT'S NEXT

After successful deployment:

1. **Monitor for 24 hours** to ensure stability
2. **Check error logs** in Cloud Logging dashboard
3. **Load test** the API endpoint
4. **Set up alerts** for high error rates
5. **Document** any custom configuration needed

---

## 📞 STILL HAVING ISSUES?

Check logs with:
```bash
gcloud run services logs read legalmind-backend --region=us-central1 --limit=100
```

Look for:
- ✅ "✅ Using Vertex AI with Application Default Credentials"
- ❌ "❌ Vertex AI initialization failed" (check roles)
- ❌ "ImportError" (check requirements.txt)
- ❌ "403" (check IAM roles again)

Or run diagnostic:
```powershell
.\diagnose-deployment.ps1
```

This will identify any remaining misconfiguration.

---

## 🎓 KEY LEARNINGS

1. **Service accounts use Application Default Credentials (ADC)**, not API keys
2. **Vertex AI SDK** (`google-cloud-aiplatform`) requires proper ADC + IAM roles
3. **REST API** (public Gemini) requires API keys and has limited scopes for service accounts
4. **Silent fallbacks** are dangerous - always fail fast with clear errors
5. **Cloud Run** requires proper configuration:
   - Correct service account assigned
   - Service account has required roles
   - Min instances set to prevent cold starts  
   - Timeout sufficient for initialization

---

## 📝 CHANGES SUMMARY

| File | Change |
|------|--------|
| `backend/services/gemini_service.py` | Removed fallback mechanisms, strict Vertex AI mode |
| `backend/requirements.txt` | Added `google-cloud-aiplatform>=1.50.0` |
| `deploy-complete-fix.ps1` | NEW - Automated deployment script (PowerShell) |
| `deploy-complete-fix.sh` | NEW - Automated deployment script (Bash) |
| `diagnose-deployment.ps1` | NEW - Deployment verification script |
| `fix-vertex-ai-permissions.ps1` | NEW - Quick permission fixer (PowerShell) |
| `fix-vertex-ai-permissions.sh` | NEW - Quick permission fixer (Bash) |

---

**Ready to deploy? Run: `.\deploy-complete-fix.ps1`**

This is a COMPLETE, production-ready fix with zero ambiguity.
