FROM grafana/grafana:latest

# Copy provisioning configuration
COPY grafana/provisioning /etc/grafana/provisioning

# Set default admin credentials
ENV GF_SECURITY_ADMIN_USER=admin
ENV GF_SECURITY_ADMIN_PASSWORD=admin123
ENV GF_USERS_ALLOW_SIGN_UP=false

# Expose the default Grafana port
EXPOSE 3000

# Use the default Grafana entrypoint
USER grafana
