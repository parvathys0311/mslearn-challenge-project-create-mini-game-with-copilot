#!/usr/bin/env python3
"""
Diode client for ingesting parsed data into NetBox via Diode.
"""

import json
import logging
from typing import Dict, List, Any, Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiodeClient:
    """Client for interacting with Diode ingestion service."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the Diode client.
        
        Args:
            base_url: Base URL of the Diode service (e.g., http://localhost:8080)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
        
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def ingest_data(self, data_source: str, data: Any) -> bool:
        """
        Ingest data into Diode.
        
        Args:
            data_source: Name of the data source
            data: Data to ingest (will be JSON serialized)
            
        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{self.base_url}/api/diode/data-sources/{data_source}/"
        
        payload = {
            'data': data
        }
        
        try:
            logger.info(f"Ingesting data to Diode data source: {data_source}")
            logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            
            logger.info(f"Successfully ingested data to {data_source}")
            logger.debug(f"Response: {response.text}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error ingesting data to Diode: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            return False
    
    def ingest_vrf_interfaces(self, interfaces: List[Dict[str, Any]], 
                              device_name: str) -> bool:
        """
        Ingest VRF interface data into Diode.
        
        Args:
            interfaces: List of parsed VRF interface data
            device_name: Name of the device
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Format data for Diode ingestion
        formatted_data = {
            'device': device_name,
            'vrf_interfaces': interfaces,
            'count': len(interfaces)
        }
        
        return self.ingest_data('ios-vrf-interfaces', formatted_data)
    
    def health_check(self) -> bool:
        """
        Check if Diode service is healthy.
        
        Returns:
            bool: True if service is healthy, False otherwise
        """
        url = f"{self.base_url}/health"
        
        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            logger.info("Diode service is healthy")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Diode health check failed: {str(e)}")
            return False


def ingest_to_diode(diode_url: str, data_source: str, data: Any, 
                   api_key: Optional[str] = None) -> bool:
    """
    Convenience function to ingest data to Diode.
    
    Args:
        diode_url: Base URL of the Diode service
        data_source: Name of the data source
        data: Data to ingest
        api_key: Optional API key for authentication
        
    Returns:
        bool: True if successful, False otherwise
    """
    client = DiodeClient(diode_url, api_key)
    return client.ingest_data(data_source, data)


if __name__ == '__main__':
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Ingest data to Diode')
    parser.add_argument('--url', required=True, help='Diode base URL')
    parser.add_argument('--api-key', help='API key for authentication')
    parser.add_argument('--data-source', default='ios-vrf-interfaces', 
                       help='Data source name')
    parser.add_argument('--test', action='store_true', 
                       help='Run with test data')
    
    args = parser.parse_args()
    
    client = DiodeClient(args.url, args.api_key)
    
    # Health check
    if client.health_check():
        print("✓ Diode service is healthy")
    else:
        print("✗ Diode service health check failed")
        exit(1)
    
    # Test ingestion if requested
    if args.test:
        test_data = {
            'device': 'test-router',
            'vrf_interfaces': [
                {
                    'interface': 'Gi0/0/0',
                    'ip_address': '10.1.1.1',
                    'vrf': 'MGMT',
                    'protocol': 'up'
                }
            ]
        }
        
        if client.ingest_data(args.data_source, test_data):
            print("✓ Test data ingested successfully")
        else:
            print("✗ Failed to ingest test data")
            exit(1)
