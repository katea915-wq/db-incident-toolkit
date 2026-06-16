import argparse
import sys
import psycopg2
from checks.slow_queries import run as slow_queries
from checks.lock_waits import run as lock_waits
from checks.table_bloat import run as table_bloat
from reports.html_report import generate, get_overall

criticality_label = {
    "OK":       "[ OK ]",
    "WARNING":  "[WARN]",
    "CRITICAL": "[CRIT]",
}

def print_slow_queries(rows):
    print("\n--- Slow Queries ---")
    if not rows:
        print("No issues detected.")
        return
    for r in rows:
        label = criticality_label[r["criticality"]]
        print(f"{label} PID: {r['pid']} | Duration: {r['duration']} | State: {r['state']}")
        print(f" Query: {r['query']}")
        print("-" * 50)

def print_lock_waits(rows):
    print("\n--- Lock Waits ---")
    if not rows:
        print("No issues detected.")
        return
    for r in rows:
        label = criticality_label[r["criticality"]]
        print(f"{label} PID: {r['pid']} | User: {r['usename']} | Blocked by: {r['blocked_by']} | State: {r['state']}")
        print(f" Query: {r['query']}")
        print("-" * 50)

def print_table_bloat(rows):
    print("\n--- Table Bloat ---")
    if not rows:
        print("No issues detected.")
        return
    for r in rows:
        label = criticality_label[r["criticality"]]
        print(f"{label} Table: {r['table_name']} | Dead: {r['dead_rows']} | Live: {r['live_rows']} | Ratio: {r['dead_ratio']}%")
        print("-" * 50)

def parse_arguments():
    parser = argparse.ArgumentParser(description="DB-INCIDENT-TOOLKIT")
    parser.add_argument("--check",default="all",choices=["slow-queries", "lock-waits", "table-bloat", "all"],help="Type of check to run")
    parser.add_argument( "--report",metavar="FILE",help="Save HTML report to file"
    )
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        sections = []

        if args.check in ("slow-queries", "all"):
            rows = slow_queries()
            print_slow_queries(rows)
            sections.append({"name": "Slow Queries", "rows": rows, "overall": get_overall(rows)})

        if args.check in ("lock-waits", "all"):
            rows = lock_waits()
            print_lock_waits(rows)
            sections.append({"name": "Lock Waits", "rows": rows, "overall": get_overall(rows)})

        if args.check in ("table-bloat", "all"):
            rows = table_bloat()
            print_table_bloat(rows)
            sections.append({"name": "Table Bloat", "rows": rows, "overall": get_overall(rows)})

        if args.report:
            command = f"python cli.py --check {args.check} --report {args.report}"
            generate(sections, args.report, command)

    except psycopg2.OperationalError as e:
        print(f"Connection ERROR to DB: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()