import sqlite3

def generate_report():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    print("Patch Summary Report")
    print("--------------------")

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM patch_results
        GROUP BY status
        ORDER BY COUNT(*) DESC
    """)
    for status, count in cursor.fetchall():
        print(f"{status}: {count}")

    print("\nFailures (most recent):")
    cursor.execute("""
        SELECT server, environment, attempts, timestamp, note
        FROM patch_results
        WHERE status = 'FAILURE'
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    if not rows:
        print("None ✅")
    else:
        for server, env, attempts, ts, note in rows:
            print(f"- {server} ({env}) | attempts={attempts} | {ts} | {note}")

    conn.close()

if __name__ == "__main__":
    generate_report()