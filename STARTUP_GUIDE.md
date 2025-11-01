# Monitoring Stack - Startup Guide

## Quick Start

### Local Development Mode
```bash
sudo docker compose --env-file .env.local -f docker-compose.yml -f docker-compose.local.yml up -d --build
```

### Production Mode
```bash
# First, copy and configure the production env file
cp .env.prod.template .env.prod
# Edit .env.prod with your production values

# Then start in production mode
sudo docker compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## Optional: Shell Function

Add this to your `~/.bashrc` or `~/.zshrc` for easier management:

```bash
monitoringup() {
    cd /path/to/monitoring  # Update this path
    
    sudo docker compose down --remove-orphans
    
    if [ "$1" = "local" ]; then
        echo "Starting monitoring stack in LOCAL mode..."
        sudo docker compose --env-file .env.local -f docker-compose.yml -f docker-compose.local.yml up -d --build
    elif [ "$1" = "prod" ]; then
        echo "Starting monitoring stack in PRODUCTION mode..."
        sudo docker compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d --build
    else
        echo "Usage: monitoringup {local|prod}"
        return 1
    fi
    
    echo "Monitoring stack started in $1 mode"
    sudo docker compose logs -f
}
```

Then use it like:
```bash
monitoringup local   # Start in local mode
monitoringup prod    # Start in production mode
```

## Environment Differences

### Local Mode (.env.local)
- **Port binding**: All services bound to `127.0.0.1` (localhost only)
  - Prometheus: `127.0.0.1:9090`
  - Grafana: `127.0.0.1:3001`
  - Token Manager: `127.0.0.1:8080`
- **Target**: Monitors NestJS via `nginx:80` in monitoring network
- **Environment label**: `local`
- **Log level**: `INFO`

### Production Mode (.env.prod)
- **Port binding**: Services exposed publicly
  - Prometheus: `9090:9090`
  - Grafana: `3001:3000`
- **Target**: Monitors production NestJS instance
- **Environment label**: `production`
- **Log level**: `WARNING`

## Configuration Files

### Environment Variables
- `.env.local` - Local development settings (safe to commit)
- `.env.prod.template` - Template for production (commit this)
- `.env.prod` - Actual production secrets (DO NOT COMMIT - add to .gitignore)

### Prometheus Configuration
- `prometheus.template.yml` - Template with placeholders
- Environment variables `ENVIRONMENT` and `NESTJS_TARGET` are substituted at startup

## Services Included

1. **Prometheus** - Metrics collection and alerting
2. **Grafana** - Dashboards and visualization
3. **Loki** - Log aggregation
4. **Promtail** - Log collection from Docker containers
5. **Token Manager** - Automatic JWT refresh for authenticated metrics endpoint

## Accessing Services

### Local Mode
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin123)
- Loki: http://localhost:3100

### Production Mode
- Prometheus: http://your-server:9090
- Grafana: http://your-server:3001 (admin/admin123)
- Loki: http://your-server:3100

## Stopping the Stack

```bash
sudo docker compose down
```

To also remove volumes (WARNING: deletes all data):
```bash
sudo docker compose down -v
```

## Logs

View logs for all services:
```bash
sudo docker compose logs -f
```

View logs for a specific service:
```bash
sudo docker compose logs -f grafana
sudo docker compose logs -f prometheus
```

## Troubleshooting

### Prometheus not scraping NestJS
1. Check token-manager logs: `sudo docker compose logs token-manager`
2. Verify NestJS is in the monitoring network: `sudo docker network inspect monitoring`
3. Check Prometheus targets: http://localhost:9090/targets

### Grafana shows "No Data"
1. Verify Prometheus is scraping: Check targets page
2. Check datasource configuration in Grafana
3. Restart Grafana: `sudo docker compose restart grafana`

### Loki not receiving logs
1. Check Promtail logs: `sudo docker compose logs promtail`
2. Verify Docker socket is mounted correctly
3. Check container labels have `logging=promtail`
