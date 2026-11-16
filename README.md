
# Network Monitor

A Python script that checks the availability of TCP ports on a target server every 60 seconds.

## Features

- Checks multiple TCP ports using asyncio.
- Handles connection errors and timeouts.
- Measures connection response time.
- Saves results in a log file.
- Supports stopping with Ctrl+C.

## Configuration

Monitoring settings are stored in `config.json`.

```json
{
    "host": "127.0.0.1",
    "ports": [22, 80, 443, 3306, 8000],
    "interval": 60,
    "timeout": 3
}
```

## Run

```bash
python3 monitor.py
```

## Why asyncio?

Network connections often require waiting for a response. Using asyncio allows the program to check several ports concurrently instead of waiting for each check to finish.

`asyncio.gather()` runs the port checks together, while `asyncio.sleep()` waits between monitoring rounds without blocking the event loop.

This makes asyncio a suitable choice for this I/O-bound task.

## Run as a Systemd Service

Systemd is a service manager in Linux that allows programs to run in the background.

To run this script continuously, a systemd service file can be created with the program's execution path and working directory. The service can then be enabled to start automatically when the system boots.

Systemd can also restart the program if it stops unexpectedly and provides commands to check its status and view its logs.

This allows the Network Monitor to run continuously without requiring a terminal to remain open.
