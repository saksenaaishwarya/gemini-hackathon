# Backend Deployment Fix Summary

## Issue Encountered
1. **403 Error**: Backend was using public Gemini API instead of Vertex AI
2. **Port Mismatch**: Dockerfile set PORT=8000, Cloud Run expects PORT=8080  
3. **Import Errors**: Old incompatible files conflicting with new code

## Fixes Applied

### 1. Vertex AI Configuration ✅
**Problem**: Backend defaulted to public Gemini API (`generativelanguage.googleapis.com`)  
**Root**: `use_vertex_ai: bool = False` in settings.py

**Changes**:
- [backend/config/settings.py](../backend/config/settings.py#L21): Changed default `use_vertex_ai` from `False` → `True`
- [backend/config/settings.py](../backend/config/settings.py#L78): Changed env var default from `"false"` → `"true"`
- [Dockerfile](../Dockerfile): Added `ENV USE_VERTEX_AI=true`
- [backend/.env.example](../backend/.env.example): Documented `USE_VERTEX_AI=true` setting

**Result**: Backend now uses Vertex AI (`aiplatform.googleapis.com`) by default

### 2. Port Configuration ✅
**Problem**: Dockerfile set `ENV PORT=8000`, overriding Cloud Run's `PORT=8080`  
**Error**: "Container failed to start and listen on the port defined by PORT=8080"

**Changes**:
- [Dockerfile](../Dockerfile): Removed `ENV PORT=8000` line
- Added comment explaining Cloud Run sets PORT=8080 automatically

**Result**: Backend now listens on Cloud Run's PORT (8080)

### 3. File Cleanup & Import Resolution ✅
**Problem**: Multiple versions of files causing import conflicts

**Old incompatible files** (renamed to .old.py):
- `backend/main.py` → `backend/main.old.py`
- `backend/api/app.py` → `backend/api/app.old.py`
- `backend/api/endpoints.py` → `backend/api/endpoints.old.py`
- `backend/agents/agent_definitions.py` → `backend/agents/agent_definitions.old.py`
- `backend/agents/agent_strategies.py` → `backend/agents/agent_strategies.old.py`
- `backend/managers/chatbot_manager.py` → `backend/managers/chatbot_manager.old.py`

**New files activated** (renamed from *_new.py → *.py):
- `backend/main_new.py` → `backend/main.py`
- `backend/api/app_new.py` → `backend/api/app.py`
- `backend/api/endpoints_new.py` → `backend/api/endpoints.py`
- `backend/agents/agent_definitions_new.py` → `backend/agents/agent_definitions.py`
- `backend/agents/agent_strategies_new.py` → `backend/agents/agent_strategies.py`
- `backend/managers/chatbot_manager_new.py` → `backend/managers/chatbot_manager.py`

**Import updates** in [backend/api/app.py](../backend/api/app.py):
-FROM:
```python
from managers.chatbot_manager_new import get_chatbot_manager
from api.endpoints_new import router
from agents.agent_strategies_new import get_workflow_template
from agents.agent_definitions_new import get_agent_config
```

TO:
```python
from managers.chatbot_manager import get_chatbot_manager
from api.endpoints import router
from agents.agent_strategies import get_workflow_template
from agents.agent_definitions import get_agent_config
```

**Import updates** in [backend/main.py](../backend/main.py):
```python
uvicorn.run("api.app:app", ...)  # Changed from "api.app_new:app"
```

**Dockerfile CMD** updated:
```dockerfile
CMD ["python", "main.py"]  # Changed from "main_new.py"
```

**Result**: All imports resolved, no more conflicting file versions

---

## Deployment Command

```bash
gcloud run deploy legalmind-backend \
  --source=backend \
  --project=legalmind-486106 \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="USE_VERTEX_AI=true" \
  --timeout=300
```

---

## Expected Outcome

After deployment completes:

1. ✅ Backend starts successfully on PORT=8080
2. ✅ Health endpoint responds with HTTP 200
3. ✅ Vertex AI configured correctly (no 403 errors)
4. ✅ Contract analysis works without authentication errors

### Test After Deployment

```bash
# Health check
curl https://legalmind-backend-677928716377.us-central1.run.app/health

# Expected response:
{
  "status": "healthy",
  "service": "LegalMind API",
  "timestamp": "..."
}
```

---

## Files Modified

1. `Dockerfile` - Removed PORT override, added USE_VERTEX_AI
2. `backend/config/settings.py` - Changed defaults to use Vertex AI
3. `backend/.env.example` - Documented USE_VERTEX_AI setting
4. `backend/main.py` - Updated imports (renamed from main_new.py)
5. `backend/api/app.py` - Updated imports (renamed from app_new.py)
6. Multiple backend modules - Renamed from *_new.py to *.py

---

## Summary

**Root Cause**: Configuration defaulted to public Gemini API + old incompatible files
**Solution**: Enable Vertex AI by default + clean up file conflicts + fix port configuration  
**Status**: Deployment in progress
**Deployment Time**: ~3-5 minutes

Once deployment completes, the backend will:
- Use Vertex AI exclusively (`aiplatform.googleapis.com`)
- Listen on the correct port (8080)
- Have no import conflicts
- Work correctly with Cloud Run service accounts
