# LegalMind Deployment Guide - Google Cloud

This guide walks you through deploying the LegalMind project to Google Cloud infrastructure.

## Prerequisites

1. **Google Cloud Project** - Already created and active
2. **GitHub Repository** - Connected to your GCP project
3. **Gcloud CLI** - Installed locally (for manual deployments)
4. **Firebase CLI** - Installed locally (for Firebase operations)

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Install Firebase CLI
npm install -g firebase-tools
```

## Architecture

```
┌─────────────────────────────────────────────┐
│         Firebase Hosting (Frontend)          │
│              Next.js 15.3 App                │
└─────────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────┐
│         Cloud Load Balancer / CDN            │
└─────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
┌───────────────────┐      ┌───────────────────┐
│   Cloud Run       │      │  Cloud Run        │
│  (API Backend)    │      │ (Future Services) │
└───────────────────┘      └───────────────────┘
        │
        ↓
┌───────────────────────────────────────────────┐
│         Firestore Database                     │
│         Cloud Storage (Documents)              │
│         Secret Manager (Credentials)           │
└───────────────────────────────────────────────┘
```

---

## Step 1: Set Up Google Cloud Project

### 1.1 Enable Required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  firestore.googleapis.com \
  storage-api.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  firebase.googleapis.com \
  artifactregistry.googleapis.com
```

### 1.2 Create Service Accounts

**For Cloud Run:**
```bash
gcloud iam service-accounts create legalmind-backend \
  --display-name="LegalMind Backend Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:legalmind-backend@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/datastore.user"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:legalmind-backend@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
```

**For GitHub Actions (Workload Identity Federation):**
```bash
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Service Account"

# Create Workload Identity Pool
gcloud iam workload-identity-pools create "github-pool" \
  --project="PROJECT_ID" \
  --location="global" \
  --display-name="GitHub Actions Pool"

# Create Workload Identity Provider
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="PROJECT_ID" \
  --location="global" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.environment=assertion.environment" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# Configure service account impersonation
gcloud iam service-accounts add-iam-policy-binding \
  github-actions@PROJECT_ID.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_ID/locations/global/workloadIdentityPools/github-pool/attribute.repository/smirk-dev/gemini-hackathon"
```

---

## Step 2: Configure GitHub Secrets

Add these secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):

```bash
GCP_PROJECT_ID              # Your Google Cloud Project ID
WIF_PROVIDER                # Output from workload identity setup
WIF_SERVICE_ACCOUNT         # github-actions@PROJECT_ID.iam.gserviceaccount.com
CLOUD_RUN_SERVICE_ACCOUNT   # legalmind-backend@PROJECT_ID.iam.gserviceaccount.com
FIREBASE_SERVICE_ACCOUNT    # Service account JSON for Firebase (base64 encoded)
API_URL                     # Cloud Run service URL (update after first deploy)
```

**To encode Firebase service account:**
```bash
gcloud iam service-accounts keys create firebase-key.json \
  --iam-account=legalmind-backend@PROJECT_ID.iam.gserviceaccount.com

cat firebase-key.json | base64 -w 0
# Copy output to FIREBASE_SERVICE_ACCOUNT secret
```

---

## Step 3: Store Environment Variables in Secret Manager

```bash
# Create secrets for sensitive data
echo -n "your-google-cloud-project-id" | gcloud secrets create GOOGLE_CLOUD_PROJECT --data-file=-

echo -n "your-google-api-key" | gcloud secrets create GOOGLE_API_KEY --data-file=-

echo -n "your-bing-api-key" | gcloud secrets create BING_API_KEY --data-file=-

echo -n "your-gemini-api-key" | gcloud secrets create GEMINI_API_KEY --data-file=-

# Grant Cloud Run service account access
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
  --member="serviceAccount:legalmind-backend@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Repeat for other secrets
```

---

## Step 4: Update Environment Configuration

### For Backend (Python)

Create `.env.local` in the `backend/` directory:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
DEBUG=false
API_BASE_URL=https://legalmind-backend-PROJECT_ID.cloudfunctions.net
CORS_ORIGINS=https://your-firebase-hosting-domain.web.app
```

### For Frontend (Next.js)

The GitHub Actions workflow automatically sets:
```bash
NEXT_PUBLIC_API_URL=https://legalmind-backend-PROJECT_ID.cloudfunctions.net
NODE_ENV=production
```

---

## Step 5: Deploy Backend

### Option A: Automatic Deployment (GitHub Actions)

```bash
# Push to main branch
git add .
git commit -m "Deploy to Cloud Run"
git push origin main

# GitHub Actions will automatically:
# 1. Build Docker image
# 2. Push to Container Registry
# 3. Deploy to Cloud Run
```

### Option B: Manual Deployment

```bash
# Build Docker image
docker build -t gcr.io/PROJECT_ID/legalmind-backend:latest .

# Push to Container Registry
docker push gcr.io/PROJECT_ID/legalmind-backend:latest

# Deploy to Cloud Run
gcloud run deploy legalmind-backend \
  --image gcr.io/PROJECT_ID/legalmind-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=PROJECT_ID,DEBUG=false" \
  --service-account=legalmind-backend@PROJECT_ID.iam.gserviceaccount.com

# Get the service URL
gcloud run services describe legalmind-backend \
  --region us-central1 \
  --format='value(status.url)'
```

---

## Step 6: Deploy Frontend

### Option A: Automatic Deployment (GitHub Actions)

```bash
# Push to main branch - same as backend
# GitHub Actions will:
# 1. Install dependencies
# 2. Build Next.js app
# 3. Deploy to Firebase Hosting
```

### Option B: Manual Deployment

```bash
cd frontend

# Install dependencies
npm install

# Build
npm run build

# Deploy to Firebase Hosting
firebase deploy --project=PROJECT_ID
```

---

## Step 7: Verify Deployment

### Check Cloud Run Deployment

```bash
# List deployed services
gcloud run services list --region us-central1

# View service details
gcloud run services describe legalmind-backend --region us-central1

# View logs
gcloud run logs read legalmind-backend --region us-central1 --limit 50

# Test API endpoint
curl https://legalmind-backend-PROJECT_ID.cloudfunctions.net/docs
```

### Check Firebase Hosting

```bash
# View deployment history
firebase hosting:channel:list --project=PROJECT_ID

# View hosting site
# https://PROJECT_ID.web.app
```

---

## Step 8: Configure Custom Domain (Optional)

### For Backend (Cloud Run)

```bash
gcloud run domain-mappings create \
  --service=legalmind-backend \
  --domain=api.yourdomain.com \
  --region=us-central1

# You'll need to update DNS to point to Cloud Run's DNS address
```

### For Frontend (Firebase Hosting)

```bash
firebase hosting:domain:add yourdomain.com --project=PROJECT_ID
# Follow the DNS configuration prompts
```

---

## Monitoring & Troubleshooting

### View Cloud Run Metrics

```bash
# CPU, memory, request count
gcloud run services describe legalmind-backend \
  --region us-central1 \
  --format="value(status.conditions[0])"

# Real-time logs
gcloud run logs read legalmind-backend \
  --region us-central1 \
  --follow
```

### Check Firestore Status

```bash
gcloud firestore databases list
gcloud firestore backups describe --database=default
```

### Debug Deployment Issues

```bash
# Check service account permissions
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:legalmind-backend@"

# Check API quotas
gcloud compute project-info describe --project=PROJECT_ID
```

---

## Cost Optimization

1. **Cloud Run**: Set up auto-scaling limits:
   ```bash
   gcloud run deploy legalmind-backend \
     --max-instances=10 \
     --min-instances=1
   ```

2. **Firestore**: Enable automatic scaling and set budget alerts

3. **Cloud Storage**: Set up lifecycle policies to delete old logs:
   ```bash
   gsutil lifecycle set - gs://PROJECT_ID-documents << 'EOF'
   {
     "lifecycle": {
       "rule": [
         {
           "action": {"type": "Delete"},
           "condition": {"age": 90}
         }
       ]
     }
   }
   EOF
   ```

---

## Rollback Procedures

### Rollback Cloud Run Deployment

```bash
# View revision history
gcloud run revisions list --service=legalmind-backend --region=us-central1

# Route traffic to previous revision
gcloud run services update-traffic legalmind-backend \
  --to-revisions=REVISION_NAME=100 \
  --region=us-central1
```

### Rollback Firebase Hosting

```bash
# View deployment history
firebase hosting:channel:list --project=PROJECT_ID

# Rollback to previous version
firebase hosting:clone PROJECT_ID:live PROJECT_ID:live
```

---

## Next Steps

1. ✅ Deploy backend to Cloud Run
2. ✅ Deploy frontend to Firebase Hosting
3. ✅ Set up monitoring and alerts
4. ✅ Configure custom domain
5. ✅ Set up CI/CD pipeline
6. ✅ Implement analytics tracking
7. ✅ Set up error logging (Cloud Error Reporting)

For support: Check cloud logs and GitHub Actions run history.
