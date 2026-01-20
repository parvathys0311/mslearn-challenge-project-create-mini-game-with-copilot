#!/usr/bin/env python3
"""
Workflow to execute 'show ip vrf interfaces' on Cisco IOS devices,
parse the output, and feed it into Diode.
"""

import sys
import logging
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ios_command_executor import IOSCommandExecutor, run_command_on_device
from parsers.vrf_interfaces_parser import parse_show_ip_vrf_interfaces
from scripts.diode_client import DiodeClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VRFInventoryWorkflow:
    """Workflow for VRF interface inventory discovery."""
    
    def __init__(self, device_host: str, device_username: str, device_password: str,
                 diode_url: str, diode_api_key: str = None):
        """
        Initialize the workflow.
        
        Args:
            device_host: Device hostname or IP
            device_username: Device username
            device_password: Device password
            diode_url: Diode service URL
            diode_api_key: Optional Diode API key
        """
        self.device_host = device_host
        self.device_username = device_username
        self.device_password = device_password
        self.diode_url = diode_url
        self.diode_api_key = diode_api_key
        
        self.executor = None
        self.diode_client = None
    
    def setup(self) -> bool:
        """
        Setup the workflow components.
        
        Returns:
            bool: True if setup successful
        """
        logger.info("Setting up workflow...")
        
        # Initialize IOS command executor
        self.executor = IOSCommandExecutor(
            self.device_host,
            self.device_username,
            self.device_password
        )
        
        # Initialize Diode client
        self.diode_client = DiodeClient(self.diode_url, self.diode_api_key)
        
        # Check Diode health
        if not self.diode_client.health_check():
            logger.error("Diode service is not healthy")
            return False
        
        logger.info("Workflow setup complete")
        return True
    
    def execute(self) -> bool:
        """
        Execute the workflow.
        
        Returns:
            bool: True if workflow executed successfully
        """
        logger.info("="*80)
        logger.info("Starting VRF Inventory Discovery Workflow")
        logger.info("="*80)
        
        # Step 1: Connect to device
        logger.info("Step 1: Connecting to device...")
        if not self.executor.connect():
            logger.error("Failed to connect to device")
            return False
        
        try:
            # Step 2: Execute command
            logger.info("Step 2: Executing 'show ip vrf interfaces'...")
            output = self.executor.execute_show_ip_vrf_interfaces()
            
            if not output:
                logger.error("Failed to execute command")
                return False
            
            logger.info(f"Command output received ({len(output)} bytes)")
            
            # Step 3: Parse output
            logger.info("Step 3: Parsing command output...")
            parsed_data = parse_show_ip_vrf_interfaces(output)
            
            if not parsed_data:
                logger.warning("No VRF interfaces found in output")
                return False
            
            logger.info(f"Parsed {len(parsed_data)} VRF interfaces")
            
            # Log parsed data
            for interface in parsed_data:
                logger.info(f"  - {interface['interface']}: VRF={interface['vrf']}, "
                          f"IP={interface['ip_address']}, Status={interface['protocol']}")
            
            # Step 4: Ingest into Diode
            logger.info("Step 4: Ingesting data into Diode...")
            success = self.diode_client.ingest_vrf_interfaces(parsed_data, self.device_host)
            
            if success:
                logger.info("✓ Workflow completed successfully")
                return True
            else:
                logger.error("✗ Failed to ingest data into Diode")
                return False
                
        finally:
            # Cleanup
            self.executor.disconnect()
    
    def run(self) -> bool:
        """
        Run the complete workflow.
        
        Returns:
            bool: True if successful
        """
        if not self.setup():
            return False
        
        return self.execute()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='VRF Interface Inventory Discovery Workflow'
    )
    
    # Device arguments
    parser.add_argument('--device-host', required=True,
                       help='Device hostname or IP address')
    parser.add_argument('--device-username', required=True,
                       help='Device username')
    parser.add_argument('--device-password', required=True,
                       help='Device password')
    
    # Diode arguments
    parser.add_argument('--diode-url', required=True,
                       help='Diode service URL')
    parser.add_argument('--diode-api-key',
                       help='Diode API key (optional)')
    
    args = parser.parse_args()
    
    # Create and run workflow
    workflow = VRFInventoryWorkflow(
        device_host=args.device_host,
        device_username=args.device_username,
        device_password=args.device_password,
        diode_url=args.diode_url,
        diode_api_key=args.diode_api_key
    )
    
    success = workflow.run()
    
    if success:
        logger.info("="*80)
        logger.info("Workflow completed successfully!")
        logger.info("="*80)
        sys.exit(0)
    else:
        logger.error("="*80)
        logger.error("Workflow failed!")
        logger.error("="*80)
        sys.exit(1)


if __name__ == '__main__':
    main()
