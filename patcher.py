import csv
import random
import sqlite3
import time
from datetime import datetime

from logger import log_success, log_failure

MAX_RETRIES = 2  # total attempts = 1 initial + MAX_RETRIES retries


def in_maintenance_window(window_start: str, window_end: str, now: datetime) -> bool:
    """
    window_start/window_end are in HH:MM 24-hr format.
    Handles normal windows and windows that cross midnight.
    """
    start_h, start_m = map(int, window_start.split(":"))
    end_h, end_m = map(int, window_end.split(":"))

    start = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
    end = now.replace(hour=end_h, minute=end_m, second=0, microsecond=0)

    # If the window crosses midnight (e.g., 23:00 -> 02:00)
    if end <= start:
        return now >= start or now <= end
    return start <= now <= end


def run_patch(server_name: str, environment: str) -> str:
    """
    Simulated patching outcome.
    Tweak these weights for prod to be "riskier."
    """
    weights = {
        "production": (0.80, 0.20),
        "test": (0.90, 0.10),
        "development": (0.95, 0.05),
    }
    success_w, fail_w = weights.get(environment.lower(), (0.85, 0.15))
    return random.choices(["SUCCESS", "FAILURE"], weights=[success_w, fail_w], k=1)[0]


def main():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patch_results (
            server TEXT,
            environment TEXT,
            window_start TEXT,
            window_end TEXT,
            status TEXT,
            attempts INTEGER,
            timestamp TEXT,
            note TEXT
        )
    """)

    now = datetime.now()

    with open("servers.csv", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            server = row["server_name"]
            env = row["environment"]
            w_start = row["window_start"]
            w_end = row["window_end"]

            #Maintenance window gate
            if not in_maintenance_window(w_start, w_end, now):
                status = "SKIPPED"
                attempts = 0
                timestamp = datetime.now().isoformat()
                note = "Outside maintenance window"

                cursor.execute(
                    "INSERT INTO patch_results VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (server, env, w_start, w_end, status, attempts, timestamp, note)
                )

                print(f"{server} ({env}) → SKIPPED (outside {w_start}-{w_end})")
                continue

            # Retry logic
            attempts = 0
            status = "FAILURE"
            note = ""

            for attempt in range(1, MAX_RETRIES + 2):
                attempts = attempt
                status = run_patch(server, env)

                print(f"Patching {server} ({env}) attempt {attempt} → {status}")

                if status == "SUCCESS":
                    log_success(server)
                    note = "Patched successfully"
                    break
                else:
                    log_failure(server)
                    note = "Failed patch attempt"
                    # small backoff (simulates waiting / retry delay)
                    if attempt <= MAX_RETRIES:
                        time.sleep(0.5)

            timestamp = datetime.now().isoformat()

            cursor.execute(
                "INSERT INTO patch_results VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (server, env, w_start, w_end, status, attempts, timestamp, note)
            )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
