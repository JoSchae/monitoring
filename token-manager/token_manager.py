#!/usr/bin/env python3
"""
Token Manager for Prometheus JWT Authentication

This service automatically:
1. Obtains JWT tokens from NestJS auth endpoint
2. Updates Prometheus configuration with new tokens
3. Reloads Prometheus configuration
4. Schedules token renewal before expiry
"""

import requests
import yaml
import time
import schedule
import logging
import json
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TokenManager:
    def __init__(self):
        self.current_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
    def get_jwt_token(self) -> Optional[str]:
        """Get JWT token from NestJS auth endpoint"""
        try:
            payload = {
                "email": config.MONGO_DB_METRICS_USERNAME,
                "password": config.MONGO_DB_METRICS_PASSWORD
            }
            
            logger.info(f"Requesting JWT token from {config.AUTH_URL}")
            response = requests.post(
                config.AUTH_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                token = data.get('access_token')
                
                if token:
                    # Decode JWT to get expiry time
                    self.token_expires_at = self._get_token_expiry(token)
                    logger.info(f"Successfully obtained JWT token, expires at: {self.token_expires_at}")
                    return token
                else:
                    logger.error("No access_token in response")
                    return None
            else:
                logger.error(f"Failed to get token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting JWT token: {e}")
            return None
    
    def _get_token_expiry(self, token: str) -> Optional[datetime]:
        """Extract expiry time from JWT token"""
        try:
            # JWT tokens have 3 parts separated by dots
            parts = token.split('.')
            if len(parts) != 3:
                return None
                
            # Decode the payload (second part)
            # Add padding if needed
            payload = parts[1]
            payload += '=' * (4 - len(payload) % 4)
            
            decoded = base64.b64decode(payload)
            payload_data = json.loads(decoded)
            
            # Get expiry timestamp
            exp = payload_data.get('exp')
            if exp:
                return datetime.fromtimestamp(exp)
            return None
            
        except Exception as e:
            logger.warning(f"Could not decode token expiry: {e}")
            return None
    
    def update_prometheus_config(self, token: str) -> bool:
        """Update Prometheus configuration with new JWT token"""
        try:
            logger.info(f"Updating Prometheus config at {config.PROMETHEUS_CONFIG_PATH}")
            
            # Read current config
            with open(config.PROMETHEUS_CONFIG_PATH, 'r') as f:
                prometheus_config = yaml.safe_load(f)
            
            # Find and update the nestjs job
            for scrape_config in prometheus_config.get('scrape_configs', []):
                if scrape_config.get('job_name') == 'nestjs':
                    scrape_config['authorization'] = {
                        'type': 'Bearer',
                        'credentials': token
                    }
                    logger.info("Updated nestjs job with new token")
                    break
            else:
                logger.warning("Could not find nestjs job in Prometheus config")
                return False
            
            # Write updated config
            with open(config.PROMETHEUS_CONFIG_PATH, 'w') as f:
                yaml.dump(prometheus_config, f, default_flow_style=False)
            
            logger.info("Prometheus config updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating Prometheus config: {e}")
            return False
    
    def reload_prometheus(self) -> bool:
        """Tell Prometheus to reload its configuration"""
        try:
            logger.info(f"Reloading Prometheus via {config.PROMETHEUS_RELOAD_URL}")
            response = requests.post(config.PROMETHEUS_RELOAD_URL, timeout=10)
            
            if response.status_code == 200:
                logger.info("Prometheus configuration reloaded successfully")
                return True
            else:
                logger.error(f"Failed to reload Prometheus: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error reloading Prometheus: {e}")
            return False
    
    def refresh_token(self) -> bool:
        """Get new token and update Prometheus"""
        logger.info("Starting token refresh process")
        
        # Get new token
        new_token = self.get_jwt_token()
        if not new_token:
            logger.error("Failed to get new JWT token")
            return False
        
        # Update Prometheus config
        if not self.update_prometheus_config(new_token):
            logger.error("Failed to update Prometheus config")
            return False
        
        # Reload Prometheus
        if not self.reload_prometheus():
            logger.error("Failed to reload Prometheus")
            return False
        
        self.current_token = new_token
        logger.info("Token refresh completed successfully")
        return True
    
    def should_refresh_token(self) -> bool:
        """Check if token should be refreshed"""
        if not self.token_expires_at:
            return True
        
        # Refresh if token expires in the next 10 minutes
        refresh_threshold = datetime.now() + timedelta(minutes=10)
        return self.token_expires_at <= refresh_threshold
    
    def run(self):
        """Main loop"""
        logger.info("Token Manager starting up")
        
        # Initial token refresh
        if not self.refresh_token():
            logger.error("Failed initial token refresh, exiting")
            return
        
        # Schedule regular token refresh
        schedule.every(config.TOKEN_REFRESH_INTERVAL_MINUTES).minutes.do(self.refresh_token)
        
        logger.info(f"Token refresh scheduled every {config.TOKEN_REFRESH_INTERVAL_MINUTES} minutes")
        
        # Main loop
        while True:
            try:
                # Check if we need to refresh token
                if self.should_refresh_token():
                    logger.info("Token expiring soon, refreshing now")
                    self.refresh_token()
                
                # Run scheduled jobs
                schedule.run_pending()
                
                # Sleep for a minute
                time.sleep(60)
                
            except KeyboardInterrupt:
                logger.info("Token Manager shutting down")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                time.sleep(60)


if __name__ == "__main__":
    token_manager = TokenManager()
    token_manager.run()
