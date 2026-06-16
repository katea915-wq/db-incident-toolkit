#Поиск дедлоков. 
#возвращает список PID процессов, которые блокируют данный процесс

from db.connection import get_connection

def get_criticality(blocked_by):   #если есть 1 lock то уже предупреждение
    if len(blocked_by) > 1:
        return "CRITICAL"
    return "WARNING" 

def run():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT pid, usename, pg_blocking_pids(pid) AS blocked_by, query, state
    FROM pg_stat_activity
    WHERE cardinality(pg_blocking_pids(pid)) > 0;
    """)
    rows = cursor.fetchall() 
    cursor.close()
    conn.close()

    result = []
    for pid, usename, blocked_by, query, state in rows:
        result.append({
            "pid": pid,
            "usename": usename,
            "blocked_by": blocked_by,
            "query": query.strip(),
            "state": state,
            "criticality": get_criticality(blocked_by),
        })
    return result