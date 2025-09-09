# Monitoring Repository

## Features

- Prometheus monitoring with token authentication
- Grafana dashboards for NestJS and MongoDB
- Docker containerization for all environments
- GitHub Actions CI/CD pipeline

## Quick Start

### Local Development

```bash
# Use default local credentials
docker compose -f docker-compose.yml -f docker-compose.local.yml up
```

### Development Environment

```bash
# Pull and run dev images
docker compose -f docker-compose.yml -f docker-compose.dev.pull.yml up
```

### Production Environment

```bash
# Pull and run production images
docker compose -f docker-compose.yml -f docker-compose.prod.pull.yml up
```

## Environment Configuration

### Local Development (localhost:3000)
- **Auth URL**: http://localhost:3000/auth/login
- **Target**: localhost:3000
- **Ports**: Local bind (127.0.0.1)

### Development Environment (localhost:80)
- **Auth URL**: http://localhost:80/auth/login
- **Target**: localhost:80
- **Ports**: Public bind

### Production Environment (schaeferdevelopment.tech)
- **Auth URL**: http://schaeferdevelopment.tech:443/auth/login
- **Target**: schaeferdevelopment.tech:443
- **Ports**: Public bind

## Services

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Token Manager**: Background service for JWT token management

## GitHub Secrets

Set these secrets in your GitHub repository for CI/CD:

```
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
MONGO_DB_METRICS_USERNAME=monitoring@system.com
MONGO_DB_METRICS_PASSWORD=metricspassword
```

## Development Workflow

1. **Local development**: Use local compose files with default credentials
2. **Push to dev branch**: Triggers build with dev images pointing to :80
3. **Push to main branch**: Triggers build with prod images pointing to schaeferdevelopment.tech
4. **Deploy**: Use pull compose files to run pre-built images

## Project Structure

```
.
├── .github/workflows/    # GitHub Actions
├── dockerfiles/          # Custom Dockerfiles
├── grafana/              # Grafana dashboards and config
├── token-manager/        # Python JWT token manager
├── docker-compose.yml    # Base compose file
├── docker-compose.*.yml  # Environment-specific overrides
└── prometheus.yml        # Prometheus configuration
```
