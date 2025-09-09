import os

# NestJS Authentication Configuration
AUTH_URL = os.getenv('AUTH_URL', 'http://192.168.2.142:3000/auth/login')
MONGO_DB_METRICS_USERNAME = os.getenv('MONGO_DB_METRICS_USERNAME', 'monitoring@system.com')
MONGO_DB_METRICS_PASSWORD = os.getenv('MONGO_DB_METRICS_PASSWORD', 'MonitoringSystem123!')

# Prometheus Configuration
PROMETHEUS_CONFIG_PATH = os.getenv('PROMETHEUS_CONFIG_PATH', '/etc/prometheus/prometheus.yml')
PROMETHEUS_RELOAD_URL = os.getenv('PROMETHEUS_RELOAD_URL', 'http://prometheus:9090/-/reload')

# Token refresh settings
TOKEN_REFRESH_INTERVAL_MINUTES = int(os.getenv('TOKEN_REFRESH_INTERVAL_MINUTES', '50'))  # Refresh every 50 minutes
TARGET_URL = os.getenv('TARGET_URL', '192.168.2.142:3000')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
