#!/bin/bash
export PATH="/home/deployer/google-cloud-sdk/bin:$PATH"
# Set quota project so stitch-mcp proxy includes X-Goog-User-Project header
export GOOGLE_CLOUD_QUOTA_PROJECT="gen-lang-client-0948956364"
ACCESS_TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
if [ -z "$ACCESS_TOKEN" ]; then
  echo "Failed to get gcloud access token" >&2
  exit 1
fi
export STITCH_ACCESS_TOKEN="$ACCESS_TOKEN"
export CI="1"
exec stitch-mcp proxy
