# AutoGPT AU Azure Deployment

## Overview

This is a separate AutoGPT Platform deployment for the Australian region at `au.agent.antsa.ai`.

## Deployment Details

- **Target**: Azure VM (4.197.242.167)
- **Domain**: https://au.agent.antsa.ai
- **VM Size**: Standard_B2ms (2 vCPUs, 8GB RAM)
- **Location**: Australia East
- **Resource Group**: PRODUCTION
- **Trigger**: Manual deployment or via GitHub Actions

## Services Running

All backend services are running via Docker Compose:

| Service | Port | Status | Description |
|---------|------|--------|-------------|
| REST API Server | 8006 | ✅ Running | Main API endpoint |
| WebSocket Server | 8001 | ✅ Running | Real-time communications |
| Executor | 8002 | ✅ Running | Agent execution engine |
| Scheduler | 8003 | ✅ Running | Task scheduling |
| Database Manager | 8005 | ✅ Running | Database operations |
| Notification Server | 8007 | ✅ Running | Notifications handling |
| Frontend | 3000 | ✅ Running | Next.js frontend |
| PostgreSQL (Supabase) | 5432 | ✅ Running | Main database |
| Redis | 6379 | ✅ Running | Caching & sessions |
| RabbitMQ | 5672, 15672 | ✅ Running | Message queue |
| Kong (API Gateway) | 8000, 8443 | ✅ Running | API gateway |
| Supabase Auth | N/A | ✅ Running | Authentication |
| ClamAV | 3310 | ✅ Running | Virus scanning |

## Accessing the Service

- **Frontend**: http://au.agent.antsa.ai (https after DNS + SSL)
- **API**: http://au.agent.antsa.ai/api
- **WebSocket**: ws://au.agent.antsa.ai/ws
- **RabbitMQ Management**: http://4.197.242.167:15672 (guest/guest)

## SSH Access

```bash
ssh azureuser@4.197.242.167
```

## Manual Deployment

To deploy manually:

```bash
ssh azureuser@4.197.242.167
cd ~/AutoGPT
git pull origin master
cd autogpt_platform
docker compose build
docker compose up -d
```

## Environment Configuration

The environment file is located at:
- `/home/azureuser/AutoGPT/autogpt_platform/.env`

Key environment variables:
```bash
SITE_URL=https://au.agent.antsa.ai
API_EXTERNAL_URL=https://au.agent.antsa.ai
```

## GitHub Actions Setup

To enable automatic deployments via GitHub Actions, add these secrets to your GitHub repository:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_VM_HOST_AU` | `4.197.242.167` | Azure VM public IP |
| `AZURE_VM_USERNAME_AU` | `azureuser` | SSH username |
| `AZURE_VM_SSH_KEY_AU` | [Private SSH Key] | Private SSH key for authentication |

Get the private key with:
```bash
cat ~/.ssh/id_rsa
```

## DNS Configuration

**⚠️ IMPORTANT**: You need to configure DNS before SSL will work:

1. Go to your DNS provider (e.g., Cloudflare, AWS Route53)
2. Add an A record:
   - **Name**: `au.agent.antsa.ai`
   - **Type**: A
   - **Value**: `4.197.242.167`
   - **TTL**: 300 (5 minutes) or Auto

3. Verify DNS is working:
```bash
nslookup au.agent.antsa.ai
```

## SSL Certificate Setup

Once DNS is configured and pointing to the VM, run:

```bash
ssh azureuser@4.197.242.167
sudo certbot --nginx -d au.agent.antsa.ai --non-interactive --agree-tos --email alec@antsa.ai
```

This will:
- Request SSL certificate from Let's Encrypt
- Automatically configure Nginx for HTTPS
- Set up auto-renewal

## Nginx Configuration

Nginx is configured as a reverse proxy at `/etc/nginx/sites-available/autogpt`:

- Frontend: Proxies to `localhost:3000`
- API: Proxies to `localhost:8006`
- WebSocket: Proxies to `localhost:8001`

## Service Management

### View logs:
```bash
ssh azureuser@4.197.242.167
cd ~/AutoGPT/autogpt_platform
docker compose logs -f [service_name]
```

### Restart services:
```bash
docker compose restart [service_name]
```

### Stop all services:
```bash
docker compose down
```

### Start all services:
```bash
docker compose up -d
```

### Check service status:
```bash
docker compose ps
```

## Cost Estimate

**Monthly Azure Costs:**
- VM (Standard_B2ms): ~$60 USD/month
- Public IP: ~$4 USD/month
- Storage (128GB): ~$10 USD/month
- Bandwidth: Minimal (pay-as-you-go)

**Total**: ~$74 USD/month

## Troubleshooting

### Services not starting:
```bash
docker compose logs [service_name]
docker compose down
docker compose up -d --force-recreate
```

### Check VM resources:
```bash
ssh azureuser@4.197.242.167
free -h
df -h
docker stats
```

### RabbitMQ issues:
If RabbitMQ fails to start, try:
```bash
docker compose down
docker volume rm $(docker volume ls -q | grep rabbitmq)
docker compose up -d
```

## Support Resources

- AutoGPT Documentation: https://docs.agpt.co
- AutoGPT GitHub: https://github.com/antsa-alec/AutoGPT
- Main deployment: https://agent.antsa.ai

---

**Deployment Date**: October 26, 2025  
**VM IP**: 4.197.242.167  
**Domain**: au.agent.antsa.ai (pending DNS)

