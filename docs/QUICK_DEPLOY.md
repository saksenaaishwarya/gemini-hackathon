# Quick Deployment Guide - LegalMind on Google Cloud

## 5-Minute Setup

### Prerequisites
- ✅ Google Cloud Project created
- ✅ `gcloud` CLI installed
- ✅ Docker installed
- ✅ GitHub repository connected

---

## Step 1: Run GCP Setup Script (5 minutes)

**On Windows (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-gcp.ps1
```

**On macOS/Linux (Bash):**
```bash
chmod +x setup-gcp.sh
./setup-gcp.sh
```

This script will:
- ✅ Enable all required Google Cloud APIs
- ✅ Create service accounts with proper permissions
- ✅ Set up Workload Identity Federation for GitHub Actions
- ✅ Create Cloud Storage buckets
- ✅ Display your Project ID and service account emails

**Save the output** - you'll need it for GitHub secrets!

---

## Step 2: Add GitHub Secrets (2 minutes)

Go to: `Settings > Secrets and variables > Actions`

Add these secrets from the script output:

```
GCP_PROJECT_ID              = your-project-id-123
WIF_PROVIDER                = projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
WIF_SERVICE_ACCOUNT         = github-actions@your-project-id-123.iam.gserviceaccount.com
CLOUD_RUN_SERVICE_ACCOUNT   = legalmind-backend@your-project-id-123.iam.gserviceaccount.com
API_URL                     = (leave empty for now, update after first deploy)
```

**To create FIREBASE_SERVICE_ACCOUNT:**

```bash
# Run this command locally
gcloud iam service-accounts keys create firebase-key.json \
  --iam-account=legalmind-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com

# View the file content and base64 encode it
cat firebase-key.json | base64 -w 0

# Copy the output and add it as FIREBASE_SERVICE_ACCOUNT secret
```

---

## Step 3: Configure Environment Variables (1 minute)

Create `.env.local` in the `backend/` directory:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id-123
DEBUG=false
```

The frontend environment variables are automatically set by GitHub Actions.

---

## Step 4: Deploy! (2 minutes)

Just push to main:

```bash
git add .
git commit -m "Deploy to Google Cloud"
git push origin main
```

GitHub Actions will automatically:
1. Build and push Docker image to Container Registry
2. Deploy to Cloud Run
3. Build and deploy frontend to Firebase Hosting

**Watch the deployment:**
- GitHub: `Actions` tab
- Cloud Run: `gcloud run services list --region us-central1`
- Firebase: `firebase hosting:channel:list`

---

## After Deployment

### Get Your URLs

```bash
# Backend URL
gcloud run services describe legalmind-backend \
  --region us-central1 \
  --format='value(status.url)'

# Frontend URL (automatically deployed)
# https://YOUR_PROJECT_ID.web.app
```

### Update GitHub Secret

After first deploy, add the backend URL to GitHub secrets:

```
API_URL = https://legalmind-backend-YOUR_PROJECT_ID.cloudfunctions.net
```

### Test Your Deployment

```bash
# Test backend
curl https://legalmind-backend-YOUR_PROJECT_ID.cloudfunctions.net/docs

# Frontend should be live at
# https://YOUR_PROJECT_ID.web.app
```

---

## View Logs

```bash
# Backend logs
gcloud run logs read legalmind-backend --region us-central1 --follow

# Firebase hosting logs
firebase hosting:sites list
```

---

## Troubleshooting

### Deployment Failed?

```bash
# Check Cloud Run deployment status
gcloud run services describe legalmind-backend --region us-central1

# View detailed error logs
gcloud run logs read legalmind-backend --region us-central1 --limit 100

# Check GitHub Actions logs
# Go to Settings > Secrets and variables > Actions to see what failed
```

### API Not Accessible?

```bash
# Make sure Cloud Run is allowing unauthenticated access
gcloud run services update legalmind-backend \
  --allow-unauthenticated \
  --region us-central1
```

### Firebase Hosting Issues?

```bash
# Check Firebase project is initialized
firebase projects:list

# Reinitialize if needed
firebase init hosting
```

---

## Cost Estimates

- **Cloud Run**: ~$0.40/million requests + compute
- **Firebase Hosting**: Free tier: 10 GB/month storage, 360 MB/day transfer
- **Firestore**: Free tier: 25k reads, 25k writes, 1 GB storage/day
- **Cloud Storage**: Free tier: 5 GB/month

**Total estimated cost**: ~$5-15/month for moderate usage

---

## Next Steps

1. ✅ Monitor your deployment in Cloud Run
2. ✅ Set up custom domain (optional)
3. ✅ Enable HTTPS (automatic with Cloud Run)
4. ✅ Configure auto-scaling limits
5. ✅ Set up monitoring and alerts

For full deployment guide, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
