# AutoGPT Azure Deployment - CI/CD Setup

## Overview

This repository is configured for automatic deployment to an Azure VM whenever changes are pushed to the `master` branch.

## Deployment Details

- **Target**: Azure VM (20.11.209.0)
- **Domain**: https://agent.antsa.ai
- **Trigger**: Push to `master` branch in `autogpt_platform/` directory
- **Method**: GitHub Actions + SSH deployment

## What Gets Deployed

The CI/CD pipeline automatically:
1. ✅ Pulls latest changes from GitHub to the Azure VM
2. ✅ Backs up environment configuration files
3. ✅ Rebuilds affected Docker containers
4. ✅ Restarts backend services with zero-downtime
5. ✅ Performs health checks

## Modified Files

### Backend Changes
- `autogpt_platform/backend/backend/blocks/youtube.py`
  - Added **Webshare residential proxy support** for YouTube transcript API
  - Bypasses IP blocking from Azure cloud infrastructure
  - Uses rotating residential proxies automatically
  - Configured via `WEBSHARE_PROXY_USERNAME` and `WEBSHARE_PROXY_PASSWORD` environment variables

### CI/CD Configuration
- `.github/workflows/deploy-azure.yml`
  - Automated deployment workflow
  - Triggers on push to master
  - SSH-based deployment to Azure VM

## GitHub Secrets

The following secrets are configured in the repository:

| Secret Name | Description |
|-------------|-------------|
| `AZURE_VM_HOST` | Azure VM public IP address |
| `AZURE_VM_USERNAME` | SSH username (azureuser) |
| `AZURE_VM_SSH_KEY` | Private SSH key for authentication |

## Environment Configuration on VM

### Backend Environment Variables (~/AutoGPT/autogpt_platform/backend/.env)

```bash
# Webshare Residential Proxy Configuration
WEBSHARE_PROXY_USERNAME=ahlvylid
WEBSHARE_PROXY_PASSWORD=md47d3kbwglo

# Ayrshare Social Media Integration
AYRSHARE_API_KEY=5A0A8184-A9B54D8D-B0892C88-72C151CE
AYRSHARE_JWT_KEY=${AYRSHARE_JWT_KEY:-}
```

**Configuration Details:**
- **Webshare**: Enables the YouTube transcript API to bypass IP blocks from cloud providers by routing requests through Webshare's rotating residential proxy pool
- **Ayrshare**: Enables social media integration for LinkedIn, Facebook, and other platforms. Users link their accounts via OAuth through the AutoGPT UI

## How to Deploy

### Automatic Deployment
Simply push to the `master` branch:

```bash
git add .
git commit -m "feat: your changes"
git push my-fork master
```

The GitHub Actions workflow will automatically:
- Detect changes in `autogpt_platform/`
- Connect to the Azure VM via SSH
- Pull the latest code
- Rebuild and restart affected services

### Manual Deployment
If you need to deploy manually:

```bash
ssh azureuser@20.11.209.0
cd ~/AutoGPT
git pull origin master
cd autogpt_platform
docker compose build executor rest_server websocket_server scheduler_server
docker compose restart executor rest_server websocket_server scheduler_server
```

## Monitoring Deployments

1. **GitHub Actions**: View deployment status at https://github.com/antsa-alec/AutoGPT/actions
2. **Service Logs**: 
   ```bash
   ssh azureuser@20.11.209.0 "docker logs autogpt_platform-executor-1 --tail 50"
   ```
3. **Service Status**: 
   ```bash
   ssh azureuser@20.11.209.0 "cd ~/AutoGPT/autogpt_platform && docker compose ps"
   ```

## Rollback

If a deployment fails, backups are automatically created:

```bash
ssh azureuser@20.11.209.0
ls -la ~/autogpt_backups/
# Restore from a backup:
cp ~/autogpt_backups/YYYYMMDD_HHMMSS/.env ~/AutoGPT/autogpt_platform/backend/.env
cd ~/AutoGPT/autogpt_platform
docker compose restart executor rest_server websocket_server scheduler_server
```

## Services Running

The following Docker services are managed by the deployment:

- **executor**: Runs agent execution tasks
- **rest_server**: REST API server (port 8006)
- **websocket_server**: WebSocket server for real-time updates (port 8001)
- **scheduler_server**: Task scheduling service
- **frontend**: Next.js frontend (port 3000)
- **database (PostgreSQL)**: Data storage
- **redis**: Caching layer
- **rabbitmq**: Message queue
- **kong**: API gateway for Supabase

## SSL/HTTPS

- SSL certificate from Let's Encrypt
- Auto-renewal configured via Certbot
- Certificate expires: January 19, 2026
- Domain: https://agent.antsa.ai

## Cost Tracking

**Current Azure Resources:**
- VM: Standard_B4ms (4 vCPUs, 16GB RAM) - ~$120/month
- Public IP - ~$4/month
- Storage (128GB) - ~$10/month
- **Total**: ~$134/month

## Support & Troubleshooting

### Failed Deployment
Check the GitHub Actions logs for error details. Common issues:
- SSH connection timeout
- Docker build failures
- Service startup errors

### Service Not Starting
```bash
ssh azureuser@20.11.209.0
cd ~/AutoGPT/autogpt_platform
docker compose logs executor --tail 100
```

### Clear Docker Cache
```bash
ssh azureuser@20.11.209.0
cd ~/AutoGPT/autogpt_platform
docker compose down
docker system prune -af
docker compose up -d
```

---

**Last Updated**: October 22, 2025
**Repository**: https://github.com/antsa-alec/AutoGPT
**Live Instance**: https://agent.antsa.ai

