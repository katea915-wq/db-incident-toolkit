#Анализ нагрузки базы. Поиск самых длительных выполняющихся запросов


from db.connection import get_connection
from datetime import timedelta
import os


warning = timedelta(minutes=int(os.getenv("SLOW_QUERY_WARNING_MIN", 5)))
critical = timedelta(minutes=int(os.getenv("SLOW_QUERY_CRITICAL_MIN", 10)))

def get_сriticality(duration):
    if duration >= critical:
        return "CRITICAL"
    elif duration >= warning:
        return "WARNING"
    return "OK"

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
    cursor.close()
    conn.close() 
    result = []
    result = []
    for pid, duration, query, state in rows:
        criticality = get_сriticality(duration) if duration else "OK"
        result.append({
            "pid": pid,
            "duration": str(duration),
            "query": query.strip(),
            "state": state,
            "criticality": criticality,
        })
    return result
        