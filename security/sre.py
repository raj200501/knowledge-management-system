import argparse
import json
import os
import time


def check_system_health():
    uptime = os.popen("uptime").read().strip()
    return {
        "uptime": uptime,
        "timestamp": time.time(),
    }


def report():
    health = check_system_health()
    print(json.dumps(health, indent=2))


def monitor(iterations=3, interval=1):
    for _ in range(iterations):
        report()
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="SRE utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    report_parser = subparsers.add_parser("report", help="Print a health report")

    monitor_parser = subparsers.add_parser("monitor", help="Monitor health")
    monitor_parser.add_argument("--iterations", type=int, default=3)
    monitor_parser.add_argument("--interval", type=int, default=1)

    args = parser.parse_args()

    if args.command == "report":
        report()
        return 0
    if args.command == "monitor":
        monitor(args.iterations, args.interval)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
