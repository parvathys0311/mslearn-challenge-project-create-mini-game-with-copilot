#!/usr/bin/env python3
"""
Parser for Cisco IOS 'show ip vrf interfaces' command output.
"""

import re
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShowIPVrfInterfacesParser:
    """Parse output from 'show ip vrf interfaces' command."""
    
    @staticmethod
    def parse(output: str) -> List[Dict[str, Any]]:
        """
        Parse 'show ip vrf interfaces' output.
        
        Example output format:
        Interface              IP-Address      VRF                              Protocol
        Gi0/0/0                10.1.1.1        MGMT                             up
        Gi0/0/1                192.168.1.1     CUSTOMER_A                       up
        
        Args:
            output: Raw command output string
            
        Returns:
            List of dictionaries containing parsed interface information
        """
        if not output:
            logger.warning("Empty output provided to parser")
            return []
        
        interfaces = []
        lines = output.strip().split('\n')
        
        # Skip header line(s)
        data_started = False
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Detect and skip header
            if 'Interface' in line and 'VRF' in line:
                data_started = True
                continue
            
            if not data_started:
                continue
            
            # Parse data lines
            # Expected format: Interface IP-Address VRF Protocol
            parts = line.split()
            
            if len(parts) >= 4:
                interface_data = {
                    'interface': parts[0],
                    'ip_address': parts[1],
                    'vrf': parts[2],
                    'protocol': parts[3]
                }
                interfaces.append(interface_data)
                logger.debug(f"Parsed interface: {interface_data}")
            elif len(parts) >= 3:
                # Handle case where IP address might be missing
                interface_data = {
                    'interface': parts[0],
                    'ip_address': None,
                    'vrf': parts[1],
                    'protocol': parts[2]
                }
                interfaces.append(interface_data)
                logger.debug(f"Parsed interface (no IP): {interface_data}")
        
        logger.info(f"Parsed {len(interfaces)} interfaces")
        return interfaces
    
    @staticmethod
    def parse_to_dict(output: str) -> Dict[str, Any]:
        """
        Parse output and return as a dictionary grouped by VRF.
        
        Args:
            output: Raw command output string
            
        Returns:
            Dictionary with VRF names as keys and interface lists as values
        """
        interfaces = ShowIPVrfInterfacesParser.parse(output)
        
        vrf_dict = {}
        for interface in interfaces:
            vrf_name = interface['vrf']
            if vrf_name not in vrf_dict:
                vrf_dict[vrf_name] = []
            vrf_dict[vrf_name].append(interface)
        
        return vrf_dict


def parse_show_ip_vrf_interfaces(output: str) -> List[Dict[str, Any]]:
    """
    Convenience function to parse 'show ip vrf interfaces' output.
    
    Args:
        output: Raw command output string
        
    Returns:
        List of dictionaries containing parsed interface information
    """
    parser = ShowIPVrfInterfacesParser()
    return parser.parse(output)


if __name__ == '__main__':
    # Example usage with sample output
    sample_output = """
Interface              IP-Address      VRF                              Protocol
Gi0/0/0                10.1.1.1        MGMT                             up
Gi0/0/1                192.168.1.1     CUSTOMER_A                       up
Gi0/0/2                172.16.1.1      CUSTOMER_B                       up
Gi0/0/3                unassigned      CUSTOMER_C                       down
    """
    
    print("Parsing sample output...")
    results = parse_show_ip_vrf_interfaces(sample_output)
    
    print("\nParsed Results:")
    for result in results:
        print(f"  {result}")
    
    print("\nGrouped by VRF:")
    parser = ShowIPVrfInterfacesParser()
    vrf_dict = parser.parse_to_dict(sample_output)
    for vrf, interfaces in vrf_dict.items():
        print(f"  VRF {vrf}:")
        for interface in interfaces:
            print(f"    - {interface['interface']} ({interface['ip_address']})")
