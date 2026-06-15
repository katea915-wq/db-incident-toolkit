from db.connection import get_connection

def run():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT pid, usename, pg_blocking_pids(pid) AS blocked_by, query, state
    FROM pg_stat_activity
    WHERE cardinality(pg_blocking_pids(pid)) > 0;
    """)
    rows = cursor.fetchall() 
    if not rows:
        print("No issues detected.")
        return
    for i in rows:
        pid, usename,blocked_by, query, state = i
        print(f"PID: {pid} | Usename: {usename} | Blocked_by: {blocked_by}, State: {state}")
        print(f"Query: {query.strip()}")
        print("-" * 50)
    
if __name__ == "__main__":
    run()