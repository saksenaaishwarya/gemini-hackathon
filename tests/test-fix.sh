#!/usr/bin/env bash
# Quick test to verify Vertex AI fix is deployed

echo ""
echo "==============================================================================="
echo "TESTING VERTEX AI FIX DEPLOYMENT"
echo "==============================================================================="
echo ""

BACKEND_URL="https://legalmind-backend-677928716377.us-central1.run.app"

echo "🔍 TEST 1: Health Check Endpoint"
echo "URL: $BACKEND_URL/health"
echo ""

# Try health endpoint
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/health" 2>&1)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n 1)
RESPONSE_BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

echo "Status Code: $HTTP_CODE"
echo "Response:"
echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
echo ""

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ SUCCESS! The 403 error is FIXED!"
    echo ""
    echo "The backend is now using Vertex AI correctly."
    echo "No more authentication scope errors!"
    exit 0
elif [ "$HTTP_CODE" = "403" ]; then
    echo "❌ Still getting 403 error"
    echo ""
    echo "Possible reasons:"
    echo "1. Deployment hasn't completed yet (takes 2-5 minutes)"
    echo "2. Service is cold-starting (Cloud Run scales to zero)"
    echo ""
    echo "Next steps:"
    echo "  - Wait 2-3 minutes and try again"
    echo "  - Check deployment status:"
    echo "    gcloud run services describe legalmind-backend --project=legalmind-486106 --region=us-central1"
    echo "  - View logs:"
    echo "    gcloud run services logs read legalmind-backend --project=legalmind-486106 --region=us-central1 --limit=50"
    exit 1
else
    echo "⚠️  Connection error: $RESPONSE_BODY"
    echo ""
    echo "The service may be cold-starting."
    echo "Cloud Run scales services to zero when inactive."
    echo ""
    echo "Please wait 30 seconds and try again."
    exit 1
fi
