from db.connection import get_connection

def run():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
    FROM pg_stat_activity
    WHERE state = 'active'
    AND query_start IS NOT NULL
    ORDER BY duration DESC;
""")
    rows = cursor.fetchall() 
    if not rows:
        print("No issues detected.")
        return
    for i in rows:
        pid, duration, query, state = i
        print(f"PID: {pid} | Duration: {duration} | State: {state}")
        print(f"Query: {query.strip()}")
        print("-" * 50)
    
if __name__ == "__main__":
    run()