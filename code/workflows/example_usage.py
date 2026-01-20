#!/usr/bin/env python3
"""
Example: Complete VRF Inventory Discovery Workflow

This script demonstrates how to:
1. Execute 'show ip vrf interfaces' on a Cisco IOS device
2. Parse the command output
3. Feed the parsed data into Diode

This example can be used as a reference for implementing similar workflows
for other commands.
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ios_command_executor import IOSCommandExecutor
from parsers.vrf_interfaces_parser import parse_show_ip_vrf_interfaces
from scripts.diode_client import DiodeClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_with_mock_data():
    """
    Example workflow using mock data (no actual device connection required).
    """
    print("\n" + "="*80)
    print("Example: VRF Inventory Discovery with Mock Data")
    print("="*80 + "\n")
    
    # Mock command output (as if retrieved from device)
    mock_output = """
Interface              IP-Address      VRF                              Protocol
Gi0/0/0                10.1.1.1        MGMT                             up
Gi0/0/1                192.168.1.1     CUSTOMER_A                       up
Gi0/0/2                172.16.1.1      CUSTOMER_B                       up
Gi0/0/3                unassigned      CUSTOMER_C                       down
    """
    
    # Step 1: Parse the output
    logger.info("Parsing VRF interface data...")
    interfaces = parse_show_ip_vrf_interfaces(mock_output)
    
    logger.info(f"Found {len(interfaces)} VRF interfaces:")
    for interface in interfaces:
        logger.info(f"  - {interface['interface']}: VRF={interface['vrf']}, "
                   f"IP={interface['ip_address']}, Status={interface['protocol']}")
    
    # Step 2: Format for Diode
    logger.info("\nFormatting data for Diode ingestion...")
    diode_data = {
        'device': 'example-router',
        'vrf_interfaces': interfaces,
        'count': len(interfaces)
    }
    
    logger.info(f"Data formatted for Diode:")
    logger.info(f"  - Device: {diode_data['device']}")
    logger.info(f"  - Interface count: {diode_data['count']}")
    
    print("\n" + "="*80)
    print("✓ Example completed successfully!")
    print("="*80)


def example_workflow_structure():
    """
    Example showing the structure of a complete workflow.
    This demonstrates the pattern without requiring actual devices/services.
    """
    print("\n" + "="*80)
    print("Example: Complete Workflow Structure")
    print("="*80 + "\n")
    
    # Configuration (would come from config files or arguments)
    device_config = {
        'host': '192.168.1.1',
        'username': 'admin',
        'password': 'password123',
        'device_type': 'cisco_ios'
    }
    
    diode_config = {
        'url': 'http://localhost:8080',
        'api_key': 'your-api-key-here'
    }
    
    logger.info("Workflow Steps:")
    logger.info("1. Connect to device")
    logger.info(f"   - Host: {device_config['host']}")
    logger.info(f"   - Type: {device_config['device_type']}")
    
    logger.info("\n2. Execute command")
    logger.info("   - Command: show ip vrf interfaces")
    
    logger.info("\n3. Parse output")
    logger.info("   - Extract: interface, IP, VRF, protocol status")
    
    logger.info("\n4. Ingest to Diode")
    logger.info(f"   - URL: {diode_config['url']}")
    logger.info("   - Data source: ios-vrf-interfaces")
    
    logger.info("\n5. Disconnect from device")
    
    print("\n" + "="*80)
    print("Code Structure:")
    print("="*80)
    print("""
# Step 1: Connect to device
executor = IOSCommandExecutor(host, username, password)
executor.connect()

# Step 2: Execute command
output = executor.execute_show_ip_vrf_interfaces()

# Step 3: Parse output
interfaces = parse_show_ip_vrf_interfaces(output)

# Step 4: Ingest to Diode
diode_client = DiodeClient(diode_url, api_key)
diode_client.ingest_vrf_interfaces(interfaces, device_name)

# Step 5: Disconnect
executor.disconnect()
    """)
    
    print("="*80)
    print("✓ Workflow structure example completed!")
    print("="*80)


def example_adding_new_command():
    """
    Example showing how to add support for a different command.
    """
    print("\n" + "="*80)
    print("Example: Adding Support for New Commands")
    print("="*80 + "\n")
    
    logger.info("To add a new command (e.g., 'show interfaces'):")
    logger.info("")
    logger.info("1. Execute the command:")
    logger.info("   executor = IOSCommandExecutor(host, username, password)")
    logger.info("   executor.connect()")
    logger.info("   output = executor.execute_command('show interfaces')")
    logger.info("")
    logger.info("2. Create a parser (if needed):")
    logger.info("   # In parsers/interfaces_parser.py")
    logger.info("   def parse_show_interfaces(output):")
    logger.info("       # Parse logic here")
    logger.info("       return parsed_data")
    logger.info("")
    logger.info("3. Update Diode ingestion:")
    logger.info("   diode_client.ingest_data('ios-interfaces', parsed_data)")
    logger.info("")
    logger.info("4. Create workflow:")
    logger.info("   # In workflows/interfaces_workflow.py")
    logger.info("   # Combine execute, parse, ingest steps")
    
    print("\n" + "="*80)
    print("✓ New command example completed!")
    print("="*80)


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("VRF Inventory Discovery - Usage Examples")
    print("="*80)
    
    # Run examples
    example_with_mock_data()
    example_workflow_structure()
    example_adding_new_command()
    
    print("\n" + "="*80)
    print("All Examples Completed!")
    print("="*80)
    print("\nFor actual usage, see:")
    print("  - code/workflows/vrf_inventory_workflow.py")
    print("  - code/README.md")
    print()


if __name__ == '__main__':
    main()
