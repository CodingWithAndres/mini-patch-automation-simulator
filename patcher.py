import csv
import random
import sqlite3
from datetime import datetime

def run_patch(server):
    # simulate patch success/failure
    return random.choice(["SUCCESS", "FAILURE"])

def main():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patch_results (
            server TEXT,
            environment TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)

    with open("servers.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            result = run_patch(row["server_name"])
            timestamp = datetime.now().isoformat()

            cursor.execute(
                "INSERT INTO patch_results VALUES (?, ?, ?, ?)",
                (row["server_name"], row["environment"], result, timestamp)
            )

            print(f"Patching {row['server_name']} → {result}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
