
import asyncio
import json
import logging
import time
from pathlib import Path

Path("logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename="logs/monitor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


async def check_port(host, port, timeout):
    """
    Check whether a TCP port is reachable.

    Args:
        host (str): The target server IP address.
        port (int): The TCP port number.
        timeout (int): Maximum connection waiting time.

    Returns:
        dict: Connection status and related information.
    """
    start_time = time.monotonic()

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )

        writer.close()
        await writer.wait_closed()

        result = {
            "host": host,
            "port": port,
            "status": "OPEN"
        }

    except asyncio.TimeoutError:
        result = {
            "host": host,
            "port": port,
            "status": "TIMEOUT"
        }

    except ConnectionRefusedError:
        result = {
            "host": host,
            "port": port,
            "status": "CLOSED"
        }

    except OSError as error:
        result = {
            "host": host,
            "port": port,
            "status": "ERROR",
            "error": str(error)
        }

    response_time = round(time.monotonic() - start_time, 4)
    result["response_time"] = response_time

    status = result["status"]
    log_message = (
        f"{host}:{port} | {status} | "
        f"response_time={response_time}s"
    )

    if status == "OPEN":
        logging.info(log_message)
    elif status in ("CLOSED", "TIMEOUT"):
        logging.warning(log_message)
    else:
        logging.error(log_message)

    return result


async def main():
    """Run continuous network monitoring."""

    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    host = config["host"]
    ports = config["ports"]
    timeout = config["timeout"]
    interval = config["interval"]

    while True:
        print("\nStarting network monitoring...")

        tasks = [
            check_port(host, port, timeout)
            for port in ports
        ]

        results = await asyncio.gather(*tasks)

        for result in results:
            print(result)

        print(f"Next check in {interval} seconds.")

        await asyncio.sleep(interval)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
