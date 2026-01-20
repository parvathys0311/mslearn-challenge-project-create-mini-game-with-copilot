# AutoCon4 Workshop - IOS VRF Inventory Discovery

## Summary

This implementation provides a complete solution for running arbitrary commands on Cisco IOS devices, parsing the output, and feeding the results into NetBox via Diode. The focus is on the "show ip vrf interfaces" command.

## What Was Implemented

### 1. Directory Structure
```
code/
├── config/           # Configuration files
├── scripts/          # Command execution and API clients
├── parsers/          # Output parsers
└── workflows/        # Main workflows and tests
```

### 2. Core Components

#### IOS Command Executor (`scripts/ios_command_executor.py`)
- Connects to Cisco IOS devices using SSH (Netmiko library)
- Executes arbitrary commands on network devices
- Provides dedicated method for "show ip vrf interfaces"
- Includes comprehensive error handling:
  - Connection timeouts
  - Authentication failures
  - Command execution errors
- Logging throughout for debugging

#### VRF Interfaces Parser (`parsers/vrf_interfaces_parser.py`)
- Parses "show ip vrf interfaces" command output
- Extracts structured data:
  - Interface name (e.g., Gi0/0/0)
  - IP address
  - VRF name
  - Protocol status (up/down)
- Returns data as Python dictionaries for easy consumption

#### Diode Client (`scripts/diode_client.py`)
- REST API client for Diode ingestion service
- Ingests parsed network data into NetBox
- Features:
  - Health check endpoint
  - Authentication support (API key)
  - Error handling and retry logic
  - Formatted JSON payloads

#### VRF Inventory Workflow (`workflows/vrf_inventory_workflow.py`)
Complete end-to-end workflow that:
1. Connects to Cisco IOS device
2. Executes "show ip vrf interfaces" command
3. Parses the command output
4. Formats data for Diode
5. Ingests data into NetBox via Diode
6. Disconnects from device

### 3. Configuration

#### Device Configuration (`config/devices.yml`)
- YAML-based device inventory
- Stores connection details for multiple devices
- Easy to extend with new devices

#### Diode Configuration (`config/diode.yml`)
- Diode service URL
- API authentication settings
- Data source configuration

### 4. Testing & Examples

#### Integration Tests (`workflows/test_integration.py`)
- Parser validation
- Data formatting tests
- End-to-end workflow simulation with mocked components
- All tests passing ✓

#### Usage Examples (`workflows/example_usage.py`)
- Mock data examples
- Workflow structure demonstration
- Guide for adding new commands

### 5. Documentation

#### Main README (`code/README.md`)
- Complete installation instructions
- Configuration guide
- Usage examples
- Troubleshooting section
- Security notes

## Usage

### Quick Start

1. **Install dependencies:**
```bash
cd code
pip install -r requirements.txt
```

2. **Configure devices:**
Edit `code/config/devices.yml` with your device details.

3. **Configure Diode:**
Edit `code/config/diode.yml` with your Diode service URL.

4. **Run the workflow:**
```bash
python code/workflows/vrf_inventory_workflow.py \
  --device-host 192.168.1.1 \
  --device-username admin \
  --device-password password \
  --diode-url http://localhost:8080
```

## Extending for New Commands

The framework is designed to be extensible. To add support for new commands:

1. **Execute any command:**
```python
executor = IOSCommandExecutor(host, username, password)
executor.connect()
output = executor.execute_command('show interfaces')
```

2. **Create a parser (if needed):**
```python
# In parsers/interfaces_parser.py
def parse_show_interfaces(output):
    # Custom parsing logic
    return parsed_data
```

3. **Update workflow:**
```python
# Combine execute, parse, and ingest steps
output = executor.execute_command('show interfaces')
parsed = parse_show_interfaces(output)
diode_client.ingest_data('ios-interfaces', parsed)
```

## Key Features

✓ **Modular Design** - Separate concerns (execute, parse, ingest)
✓ **Error Handling** - Comprehensive error handling at every step
✓ **Logging** - Detailed logging for debugging
✓ **Extensible** - Easy to add new commands and parsers
✓ **Tested** - Integration tests with mock data
✓ **Documented** - Complete documentation and examples
✓ **Secure** - No hardcoded credentials, secure by design

## Dependencies

- **netmiko** - SSH connection to network devices
- **requests** - HTTP client for Diode API
- **pyyaml** - Configuration file parsing
- **textfsm** - Advanced text parsing (optional)

## Security Notes

- Credentials are passed via command-line arguments or config files
- Use environment variables for production deployments
- Support for SSH keys instead of passwords
- API key authentication for Diode
- No vulnerabilities detected by CodeQL scanner ✓

## Testing Results

All integration tests pass successfully:
- ✓ Parser test
- ✓ Diode client formatting test
- ✓ End-to-end workflow test (mocked)

## Files Created

```
code/
├── README.md                           # Main documentation
├── requirements.txt                    # Python dependencies
├── config/
│   ├── devices.yml                     # Device inventory
│   └── diode.yml                       # Diode configuration
├── scripts/
│   ├── __init__.py
│   ├── ios_command_executor.py         # IOS command execution
│   └── diode_client.py                 # Diode API client
├── parsers/
│   ├── __init__.py
│   └── vrf_interfaces_parser.py        # VRF interfaces parser
└── workflows/
    ├── __init__.py
    ├── vrf_inventory_workflow.py       # Main workflow
    ├── test_integration.py             # Integration tests
    └── example_usage.py                # Usage examples
```

## Next Steps

1. Configure with actual device credentials
2. Set up Diode service connection
3. Run workflow against real devices
4. Add additional commands as needed
5. Integrate into automation pipeline

## Support

See `code/README.md` for detailed documentation, troubleshooting, and examples.
