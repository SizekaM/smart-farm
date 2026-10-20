import time
import subprocess
import sys

def ensure_wifi(timeout=60):
    """
    Block until we can reach 8.8.8.8, or until timeout.
    Returns True on success, False on timeout.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            subprocess.check_output(
                ["ping", "-c", "1", "8.8.8.8"],
                stderr=subprocess.DEVNULL, timeout=5
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print("Wi-Fi unreachable, retrying…", file=sys.stderr)
            time.sleep(5)
    print(f"Failed to reach network after {timeout}s", file=sys.stderr)
    return False