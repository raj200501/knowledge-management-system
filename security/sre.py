import os
import time

def check_system_health():
    uptime = os.popen('uptime').read()
    return uptime

def monitor_system():
    while True:
        health = check_system_health()
        print(f"System Health: {health}")
        time.sleep(60)

# Example usage
monitor_system()
