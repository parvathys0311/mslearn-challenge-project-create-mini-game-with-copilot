#!/usr/bin/env python3
"""
Script to execute commands on Cisco IOS devices.
Supports running arbitrary commands for inventory discovery.
"""

import logging
from typing import Dict, Optional
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IOSCommandExecutor:
    """Execute commands on Cisco IOS devices."""
    
    def __init__(self, host: str, username: str, password: str, 
                 device_type: str = 'cisco_ios', port: int = 22):
        """
        Initialize the iOS command executor.
        
        Args:
            host: Device hostname or IP address
            username: Username for authentication
            password: Password for authentication
            device_type: Netmiko device type (default: cisco_ios)
            port: SSH port (default: 22)
        """
        self.device_params = {
            'device_type': device_type,
            'host': host,
            'username': username,
            'password': password,
            'port': port,
        }
        self.connection = None
        
    def connect(self) -> bool:
        """
        Establish connection to the device.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info(f"Connecting to device {self.device_params['host']}")
            self.connection = ConnectHandler(**self.device_params)
            logger.info(f"Successfully connected to {self.device_params['host']}")
            return True
        except NetmikoTimeoutException:
            logger.error(f"Timeout connecting to {self.device_params['host']}")
            return False
        except NetmikoAuthenticationException:
            logger.error(f"Authentication failed for {self.device_params['host']}")
            return False
        except Exception as e:
            logger.error(f"Error connecting to {self.device_params['host']}: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from the device."""
        if self.connection:
            logger.info(f"Disconnecting from {self.device_params['host']}")
            self.connection.disconnect()
            self.connection = None
    
    def execute_command(self, command: str) -> Optional[str]:
        """
        Execute a command on the device.
        
        Args:
            command: The command to execute
            
        Returns:
            str: Command output or None if error
        """
        if not self.connection:
            logger.error("Not connected to device. Call connect() first.")
            return None
        
        try:
            logger.info(f"Executing command: {command}")
            output = self.connection.send_command(command)
            logger.info(f"Command executed successfully")
            return output
        except Exception as e:
            logger.error(f"Error executing command '{command}': {str(e)}")
            return None
    
    def execute_show_ip_vrf_interfaces(self) -> Optional[str]:
        """
        Execute 'show ip vrf interfaces' command.
        
        Returns:
            str: Command output or None if error
        """
        return self.execute_command('show ip vrf interfaces')


def run_command_on_device(host: str, username: str, password: str, 
                          command: str = 'show ip vrf interfaces') -> Optional[str]:
    """
    Convenience function to run a command on a device.
    
    Args:
        host: Device hostname or IP address
        username: Username for authentication
        password: Password for authentication
        command: Command to execute (default: 'show ip vrf interfaces')
        
    Returns:
        str: Command output or None if error
    """
    executor = IOSCommandExecutor(host, username, password)
    
    if not executor.connect():
        return None
    
    try:
        output = executor.execute_command(command)
        return output
    finally:
        executor.disconnect()


if __name__ == '__main__':
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Execute commands on Cisco IOS devices')
    parser.add_argument('--host', required=True, help='Device hostname or IP')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', required=True, help='Password')
    parser.add_argument('--command', default='show ip vrf interfaces', 
                       help='Command to execute (default: show ip vrf interfaces)')
    
    args = parser.parse_args()
    
    output = run_command_on_device(
        args.host, 
        args.username, 
        args.password, 
        args.command
    )
    
    if output:
        print("\n" + "="*80)
        print("Command Output:")
        print("="*80)
        print(output)
    else:
        print("Failed to execute command")
