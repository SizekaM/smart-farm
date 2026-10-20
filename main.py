import os
import sys
from network_utils import ensure_wifi
from core import run

# Activate virtualenv if needed
VENV = "/home/pi/mawe/.venv"
if os.getenv("VIRTUAL_ENV") is None and os.path.isdir(VENV):
    activate = os.path.join(VENV, "bin", "activate_this.py")
    if os.path.isfile(activate):
        with open(activate) as f:
            exec(f.read(), {"__file__": activate})

def main():
    # 1) Ensure network connectivity
    if not ensure_wifi(timeout=60):
        sys.exit("Network check failed; exiting.")
    
    # 2) Hand off to core logic
    run()


if __name__ == "__main__":
    main()