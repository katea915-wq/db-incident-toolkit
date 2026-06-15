from db.connection import get_connection

def run():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT relname AS table_name, n_dead_tup AS dead_rows, n_live_tup AS live_rows
    FROM pg_stat_user_tables
    ORDER BY n_dead_tup DESC
    LIMIT 10;
    """)
    rows = cursor.fetchall() 
    if not rows:
        print("No issues detected.")
        return
    for i in rows:
        relname, dead_rows,live_rows= i
        print(f"Relname: {relname}")
        print(f"Dead_rows: {dead_rows}")
        print(f"Live_rows: {live_rows}")
        print("-" * 50)
    
if __name__ == "__main__":
    run()