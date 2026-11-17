from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "network_activity.log"

def record_event(direction, source, destination, source_port, destination_port, size):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"{timestamp} | {direction} | "
        f"Source={source}:{source_port} | "
        f"Destination={destination}:{destination_port} | "
        f"DataSize={size} bytes\n"
    )
    with LOG_FILE.open("a", encoding="utf-8") as log:
        log.write(line)
    print("[NETWORK MONITOR]", line.strip())
