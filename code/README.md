# AutoCon4 Workshop - IOS VRF Inventory Discovery

This project provides tools and workflows to execute arbitrary commands on Cisco IOS devices, parse the output, and ingest the data into NetBox via Diode.

## Overview

The workflow performs the following steps:
1. **Execute** - Run `show ip vrf interfaces` command on Cisco IOS devices
2. **Parse** - Extract structured data from command output
3. **Ingest** - Feed parsed data into NetBox via Diode ingestion service

## Directory Structure

```
code/
├── config/           # Configuration files
│   ├── devices.yml   # Device inventory
│   └── diode.yml     # Diode connection settings
├── scripts/          # Execution scripts
│   ├── ios_command_executor.py  # IOS command execution
│   └── diode_client.py          # Diode API client
├── parsers/          # Output parsers
│   └── vrf_interfaces_parser.py # VRF interfaces parser
├── workflows/        # Main workflows
│   └── vrf_inventory_workflow.py # Complete workflow
└── requirements.txt  # Python dependencies
```

## Installation

1. Install dependencies:
```bash
cd code
pip install -r requirements.txt
```

## Configuration

### Device Configuration

Edit `code/config/devices.yml` to add your devices:

```yaml
devices:
  - name: router-01
    host: 192.168.1.1
    device_type: cisco_ios
    username: admin
    password: cisco123
```

### Diode Configuration

Edit `code/config/diode.yml` to configure Diode connection:

```yaml
diode:
  base_url: http://localhost:8080
  api_key: your-api-key-here
  data_source: ios-vrf-interfaces
```

## Usage

### Execute Command on Single Device

```bash
python code/scripts/ios_command_executor.py \
  --host 192.168.1.1 \
  --username admin \
  --password cisco123 \
  --command "show ip vrf interfaces"
```

### Parse Command Output

```bash
python code/parsers/vrf_interfaces_parser.py
```

### Ingest Data to Diode

```bash
python code/scripts/diode_client.py \
  --url http://localhost:8080 \
  --api-key your-api-key \
  --test
```

### Run Complete Workflow

Execute the complete workflow (connect, execute, parse, ingest):

```bash
python code/workflows/vrf_inventory_workflow.py \
  --device-host 192.168.1.1 \
  --device-username admin \
  --device-password cisco123 \
  --diode-url http://localhost:8080 \
  --diode-api-key your-api-key
```

## Components

### iOS Command Executor

The `ios_command_executor.py` script provides:
- Connection management for Cisco IOS devices
- Command execution with error handling
- Support for arbitrary commands
- Built-in support for `show ip vrf interfaces`

### VRF Interfaces Parser

The `vrf_interfaces_parser.py` parser extracts:
- Interface name
- IP address
- VRF name
- Protocol status

Example parsed output:
```python
[
    {
        'interface': 'Gi0/0/0',
        'ip_address': '10.1.1.1',
        'vrf': 'MGMT',
        'protocol': 'up'
    }
]
```

### Diode Client

The `diode_client.py` provides:
- REST API client for Diode service
- Data ingestion with retry logic
- Health check capability
- Support for authentication

### VRF Inventory Workflow

The `vrf_inventory_workflow.py` orchestrates:
1. Device connection
2. Command execution
3. Output parsing
4. Diode ingestion
5. Logging and error handling

## Command Support

The framework supports arbitrary Cisco IOS commands. To add new commands:

1. Use `execute_command()` method with any command
2. Create a custom parser if needed
3. Update Diode data source as needed

Example for different command:
```python
executor = IOSCommandExecutor(host, username, password)
executor.connect()
output = executor.execute_command('show interfaces')
executor.disconnect()
```

## Error Handling

The workflow includes comprehensive error handling:
- Connection timeouts
- Authentication failures
- Command execution errors
- Parsing errors
- Diode API errors

All errors are logged with appropriate severity levels.

## Development

### Adding New Commands

1. Add command execution in `ios_command_executor.py`
2. Create parser in `parsers/` directory
3. Update workflow in `workflows/`
4. Update configuration in `config/`

### Testing Parsers

Each parser includes a `__main__` block with sample data for testing:

```bash
python code/parsers/vrf_interfaces_parser.py
```

## Requirements

- Python 3.7+
- Network connectivity to Cisco IOS devices
- SSH access to devices
- Diode service running and accessible
- NetBox instance (connected to Diode)

## Security Notes

- Store credentials securely (use environment variables or secret management)
- Use SSH keys where possible instead of passwords
- Protect API keys for Diode
- Review security groups and firewall rules

## Troubleshooting

### Connection Issues
- Verify network connectivity to device
- Check SSH is enabled on device
- Verify credentials are correct
- Check firewall rules

### Parsing Issues
- Verify command output format matches expected format
- Check for IOS version differences
- Review parser logs for details

### Diode Ingestion Issues
- Verify Diode service is running
- Check Diode URL is correct
- Verify API key is valid
- Review Diode logs for errors

## License

This project is part of the NetBox Labs AutoCon4 workshop materials.
