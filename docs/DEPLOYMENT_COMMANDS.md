# Deployment Commands Reference

Copy and paste these commands in order to deploy LegalMind to Google Cloud.

---

## 1️⃣ Run Setup Script (Automatic Configuration)

### Windows (PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-gcp.ps1
```

### macOS/Linux (Bash)
```bash
chmod +x setup-gcp.sh
./setup-gcp.sh
```

---

## 2️⃣ Create Firebase Service Account Key

Run this after the setup script completes:

```bash
# Replace YOUR_PROJECT_ID with your actual project ID
gcloud iam service-accounts keys create firebase-key.json \
  --iam-account=legalmind-backend@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### Encode it to base64

**Windows (PowerShell):**
```powershell
$content = Get-Content firebase-key.json -Raw
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content)) | Set-Clipboard
# Now paste into GitHub secret
```

**macOS/Linux:**
```bash
cat firebase-key.json | base64 -w 0 | pbcopy  # macOS
cat firebase-key.json | base64 -w 0 | xclip   # Linux
```

---

## 3️⃣ Add GitHub Secrets

Go to: **Settings → Secrets and variables → Actions → New repository secret**

Add these secrets:

| Name | Value |
|------|-------|
| `GCP_PROJECT_ID` | (from setup script output) |
| `WIF_PROVIDER` | (from setup script output) |
| `WIF_SERVICE_ACCOUNT` | (from setup script output) |
| `CLOUD_RUN_SERVICE_ACCOUNT` | (from setup script output) |
| `FIREBASE_SERVICE_ACCOUNT` | (base64 encoded JSON from step 2) |
| `API_URL` | (leave empty for now) |

---

## 4️⃣ Deploy to Production

```bash
git add .
git commit -m "Deploy LegalMind to Google Cloud"
git push origin main
```

Watch the deployment in: **Actions → deploy-backend.yml and deploy-frontend.yml**

---

## 5️⃣ Get Your Live URLs

### Backend URL
```bash
gcloud run services describe legalmind-backend \
  --region us-central1 \
  --format='value(status.url)'
```

### Frontend URL
```bash
https://YOUR_PROJECT_ID.web.app
```

---

## 6️⃣ Update API_URL Secret

Once you have your backend URL, add it to GitHub:
```bash
# Copy the Cloud Run URL from step 5 and add as API_URL secret
```

---

## ✅ Verify Deployment

### Test Backend API
```bash
curl https://legalmind-backend-YOUR_PROJECT_ID.cloudfunctions.net/docs
```

### View Backend Logs
```bash
gcloud run logs read legalmind-backend \
  --region us-central1 \
  --follow
```

### View Deployed Services
```bash
gcloud run services list --region us-central1
```

### View Firestore Status
```bash
gcloud firestore databases list
```

---

## 🔄 Redeployment (After Code Changes)

Simply push to main branch:
```bash
git push origin main
```

GitHub Actions will automatically redeploy both frontend and backend.

---

## 🛑 Rollback to Previous Version

### Cloud Run
```bash
# View previous revisions
gcloud run revisions list \
  --service=legalmind-backend \
  --region=us-central1

# Route traffic to previous revision
gcloud run services update-traffic legalmind-backend \
  --to-revisions=REVISION_NAME=100 \
  --region=us-central1
```

### Firebase Hosting
```bash
firebase hosting:channel:list
# Select previous deployment and promote to live
```

---

## 📊 Monitoring & Logs

### Real-time Logs
```bash
gcloud run logs read legalmind-backend \
  --region us-central1 \
  --follow
```

### Last 50 Errors
```bash
gcloud run logs read legalmind-backend \
  --region us-central1 \
  --limit 50
```

### Check Service Status
```bash
gcloud run services describe legalmind-backend \
  --region us-central1
```

### View Metrics
```bash
gcloud monitoring dashboards list
```

---

## 🧹 Cleanup (If Needed)

### Delete Cloud Run Service
```bash
gcloud run services delete legalmind-backend \
  --region us-central1
```

### Delete Storage Bucket
```bash
gsutil -r rm gs://YOUR_PROJECT_ID-documents
gsutil -r rm gs://YOUR_PROJECT_ID-artifacts
```

### Delete Firebase Hosting
```bash
firebase hosting:disable
```

---

## 🔧 Environment Variables

### Update Backend Environment Variables
```bash
gcloud run deploy legalmind-backend \
  --set-env-vars="DEBUG=false,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID" \
  --region us-central1
```

### Update Frontend Environment Variables
Edit `.env` or `next.config.ts` and redeploy:
```bash
git push origin main
```

---

## 💾 Backup & Restore

### Export Firestore Data
```bash
gcloud firestore export gs://YOUR_PROJECT_ID-backups/backup-$(date +%s)
```

### Import Firestore Data
```bash
gcloud firestore import gs://YOUR_PROJECT_ID-backups/backup-TIMESTAMP
```

### Download Cloud Storage Files
```bash
gsutil -r cp gs://YOUR_PROJECT_ID-documents/path/to/file ./local-path
```

---

## 📞 Support

For issues, check:
1. GitHub Actions logs: **Actions → Select workflow → View logs**
2. Cloud Run logs: `gcloud run logs read legalmind-backend --region us-central1`
3. Firebase Hosting logs: `firebase hosting:sites list`
4. Deployment guides: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Last Updated:** February 4, 2026
**Status:** Ready for Deployment ✅
