#определения таблиц, которым нужен VACUUM
#определение процента мертвых строк

from db.connection import get_connection

#WARNING > 10%, CRITICAL > 30%.
def get_criticality(dead_rows, live_rows):   
    if live_rows == 0:
        return "OK"
    ratio = dead_rows / live_rows
    if ratio >= 0.30:
        return "CRITICAL"
    elif ratio >= 0.10:
        return "WARNING"
    return "OK"

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
    cursor.close()
    conn.close()

    result = []
    for table_name, dead_rows, live_rows in rows:
        ratio = round(dead_rows / live_rows * 100, 1) if live_rows > 0 else 0
        result.append({
            "table_name": table_name,
            "dead_rows": dead_rows,
            "live_rows": live_rows,
            "dead_ratio": ratio,       #процент мертвых строк
            "criticality": get_criticality(dead_rows, live_rows),
        })
    return result
