#!/bin/bash
set -e

echo "Initializing Prometheus configuration..."

# Create prometheus config directory if it doesn't exist
mkdir -p /etc/prometheus

# Copy initial config if it doesn't exist
if [ ! -f /etc/prometheus/prometheus.yml ]; then
    echo "Copying initial prometheus.yml..."
    cp /tmp/prometheus.yml /etc/prometheus/prometheus.yml
    echo "Initial config copied successfully"
else
    echo "Prometheus config already exists, skipping copy"
fi

echo "Prometheus initialization complete"
