# NestJS Monitoring Stack with Grafana Loki

This monitoring stack includes:
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards
- **Grafana Loki**: Log aggregation
- **Promtail**: Log collection agent
- **Token Manager**: JWT token management for Prometheus

## 📊 What's Included

### Dashboards
- `nestjs-server-complete.json`: Complete NestJS application metrics dashboard
- `nestjs-logs.json`: Log analysis and monitoring dashboard
- `mongodb-database-metrics.json`: MongoDB metrics
- `mongodb-exporter.json`: MongoDB exporter dashboard
- `nestjs-application-metrics.json`: Application-specific metrics
- `nestjs-infrastructure-overview.json`: Infrastructure overview

### Alerts
- `alerts.yml`: Comprehensive alerting rules for:
  - High error rates
  - Brute force attacks detection
  - Slow database queries
  - Memory and performance issues
  - Authentication failures
  - Database connection pool exhaustion

### Log Collection
- **Promtail** collects logs from Docker containers
- **Loki** stores and indexes logs
- Automatic parsing of JSON logs
- Log correlation with metrics

## 🚀 Getting Started

1. **Start the monitoring stack:**
   ```bash
   docker-compose up -d
   ```

2. **Access the services:**
   - Grafana: http://localhost:3001 (admin/admin123)
   - Prometheus: http://localhost:9090
   - Loki: http://localhost:3100

3. **Configure your NestJS server for logging:**
   
   Add this label to your NestJS container in docker-compose.yml:
   ```yaml
   services:
     nestjs-server:
       # ... other configuration
       labels:
         - "logging=promtail"
   ```

4. **View logs in Grafana:**
   - Go to Explore section
   - Select Loki datasource
   - Use queries like: `{container_name=~"nestjs.*"}`

## 📝 Log Queries Examples

### Basic log queries for Loki:
```logql
# All logs from NestJS containers
{container_name=~"nestjs.*"}

# Error logs only
{container_name=~"nestjs.*"} |= "ERROR"

# Authentication-related logs
{container_name=~"nestjs.*"} |= "auth"

# Logs with specific log level
{container_name=~"nestjs.*"} | json | level="error"

# Count errors over time
sum by (level) (count_over_time({container_name=~"nestjs.*"} | json [5m]))
```

## 🔧 Configuration Files

- `loki-config.yml`: Loki server configuration
- `promtail-config.yml`: Promtail log collection configuration
- `prometheus.yml`: Prometheus scraping and alerting configuration
- `alerts.yml`: Alerting rules for various scenarios

## 📈 Monitoring Features

### Metrics Collected:
- HTTP request rates and duration
- Authentication attempts and failures
- Database query performance
- Memory and CPU usage
- Cache hit rates
- User registration metrics
- Event loop lag

### Log Analysis:
- Real-time log streaming
- Log level distribution
- Error log filtering
- Authentication log analysis
- Full-text search capabilities

## 🔔 Alerting

The stack includes pre-configured alerts for:
- High error rates (>10 errors/sec)
- Brute force attacks (>5 failed logins/sec)
- Slow database queries (>1 second)
- High memory usage (>90%)
- Event loop lag (>100ms)
- Database connection issues

## 🔍 Troubleshooting

### Check if logs are being collected:
```bash
# Check Promtail logs
docker logs promtail-monitoring

# Check Loki logs
docker logs loki-monitoring

# Verify log ingestion
curl -G -s "http://localhost:3100/loki/api/v1/query" --data-urlencode 'query={container_name=~"nestjs.*"}' | jq
```

### Common issues:
1. **No logs appearing**: Ensure your NestJS container has the `logging=promtail` label
2. **Loki not accessible**: Check if the Loki service is running and accessible on port 3100
3. **Promtail permission issues**: Ensure Promtail has access to Docker socket

## 🔄 Maintenance

### Log retention:
Loki is configured to store logs locally. For production, consider:
- Setting up log retention policies
- Using object storage (S3, GCS) for long-term storage
- Implementing log rotation

### Performance tuning:
- Adjust scrape intervals based on your needs
- Configure appropriate retention periods
- Monitor resource usage of the monitoring stack itself