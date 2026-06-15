import argparse
import sys
import psycopg2
from checks.slow_queries import run as slow_queries
from checks.lock_waits import run as lock_waits
from checks.table_bloat import run as deadliverows

def parse_arguments():
    parser = argparse.ArgumentParser(description="DB-INCIDENT-TOOLKIT")
    parser.add_argument("--check", default="all", help="checks(slow-queries,lock-waits,table_bloat,all)")
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        if args.check == "slow-queries":
            print("\n--- Slow Queries ---")
            slow_queries()
        elif args.check == "lock-waits":
            print("\n--- Lock Waits ---")
            lock_waits()
        elif args.check == "table_bloat":
            print("\n--- Table Bloat ---")
            deadliverows()
        elif args.check == "all":
            print("\n--- All checks ---")
            print("\n--- Slow Queries ---")
            slow_queries()
            print("\n--- Lock Waits ---")
            lock_waits()
            print("\n--- Table Bloat ---")
            deadliverows()
        else:
            print(f"Unknown check: {args.check}")
            print("Available: slow-queries, lock-waits, table-bloat, all")
            sys.exit(1)
    except psycopg2.OperationalError as e:
        print(f"Connection ERROR to DB: {e}")

if __name__ == "__main__":
    main()