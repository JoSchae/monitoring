# Grafana Dashboards for NestJS Server

This directory contains custom Grafana dashboards specifically designed for monitoring the NestJS Server with MongoDB integration.

## Dashboard Overview

### 1. NestJS Infrastructure Overview (`nestjs-infrastructure-overview.json`)
**UID:** `nestjs-infrastructure-overview`

A comprehensive overview dashboard that provides:
- **Service Status**: Real-time status of NestJS and MongoDB services
- **Key Metrics**: Active users, request rate, response times, database connections
- **API Traffic**: Breakdown by endpoints and routes
- **HTTP Status Codes**: Distribution of response codes
- **Authentication & Authorization**: Specific metrics for auth, user, role, and permission APIs
- **MongoDB Operations**: Database operation rates and memory usage

**Best for**: Operations teams and daily monitoring

### 2. NestJS Application Metrics (`nestjs-application-metrics.json`)
**UID:** `nestjs-app-metrics`

Detailed application-level metrics including:
- **HTTP Request Rate**: Requests per second by method, route, and status code
- **Request Duration**: 95th and 50th percentile response times
- **Active Users**: Current active user count
- **Database Connections**: Active database connection count
- **HTTP Status Distribution**: Breakdown of all HTTP response codes
- **HTTP Methods**: Distribution by GET, POST, PUT, DELETE, etc.

**Best for**: Developers and application performance monitoring

### 3. MongoDB Database Metrics (`mongodb-database-metrics.json`)
**UID:** `mongodb-database-metrics`

Database-specific monitoring including:
- **MongoDB Status**: Database availability and health
- **Connection Management**: Current and available connections
- **Memory Usage**: Resident memory and WiredTiger cache usage
- **Database Operations**: Insert, update, delete, query rates
- **Document Operations**: Document-level operation metrics
- **Collections & Objects**: Count by database
- **Performance Metrics**: Cache hit rates and operation latencies

**Best for**: Database administrators and performance optimization

## Metrics Sources

### NestJS Application Metrics (`/metrics` endpoint)
- `http_requests_total`: HTTP request counter with labels (method, route, status_code)
- `http_request_duration_seconds`: Request duration histogram
- `active_users_total`: Current active users gauge
- `database_connections_active`: Active database connections gauge

### MongoDB Exporter (port 9216)
- `mongodb_up`: MongoDB availability
- `mongodb_connections`: Connection statistics
- `mongodb_memory`: Memory usage by type
- `mongodb_op_counters_total`: Operation counters
- `mongodb_mongod_*`: Various MongoDB internals

## Authentication Requirements

The NestJS `/metrics` endpoint requires authentication with the `monitoring`, `admin`, or `super_admin` role. The monitoring system uses:
- **User**: metricsuser
- **Password**: metricspassword
- **Role**: monitoring

Authentication is handled automatically by the token-manager service in the monitoring stack.

## Configuration

### Prometheus Scrape Config
```yaml
- job_name: 'nestjs'
  static_configs:
    - targets: ['192.168.2.142:3000']
  metrics_path: /metrics
  scrape_interval: 30s

- job_name: 'mongodb-exporter'
  static_configs:
    - targets: ['192.168.2.142:9216']
  scrape_interval: 30s
```

### Data Sources
All dashboards are configured to use the `Prometheus` data source. Ensure your Grafana instance has:
1. Prometheus data source configured
2. Access to both NestJS metrics endpoint and MongoDB exporter
3. Proper network connectivity to the target applications

## Dashboard Features

- **Auto-refresh**: All dashboards refresh every 5 seconds
- **Time Range**: Default 1-hour window
- **Responsive Design**: Panels optimized for different screen sizes
- **Color Coding**: Thresholds for quick visual assessment
- **Legends**: Detailed legends with calculations (last, max values)
- **Tooltips**: Rich tooltips for detailed metric inspection

## Legacy Dashboards

- `nodejs-nestjs.json` - Generic Node.js dashboard (gnetId: 11074) - Consider replacing with custom dashboards
- `mongodb-exporter.json` - Generic MongoDB dashboard (gnetId: 12006) - Superseded by custom dashboard

## Installation

These dashboards are automatically loaded by Grafana through the provisioning system configured in `dashboard.yml`. No manual import required when using the Docker Compose setup.

## Customization

To modify dashboards:
1. Edit the JSON files directly
2. Restart Grafana container to reload changes
3. Or enable `allowUiUpdates: true` in `dashboard.yml` to edit via UI

## Troubleshooting

### No Data Displayed
1. Check Prometheus targets are UP: http://localhost:9090/targets
2. Verify NestJS `/metrics` endpoint authentication
3. Ensure MongoDB exporter is running on port 9216
4. Check network connectivity between monitoring stack and applications

### Authentication Issues
1. Verify monitoring user exists in NestJS application
2. Check token-manager service logs
3. Ensure monitoring user has correct role assignments

### Missing Metrics
1. Check NestJS application includes MetricsModule
2. Verify Prometheus scrape configuration
3. Check application logs for metrics registration errors
