# Patch Automation Simulator

## Overview
This project is a small automation simulator designed to model how enterprise patching workflows operate in a regulated environment. The goal is not to perform real patching, but to demonstrate automation thinking, reliability, logging, and operational reporting.

## What It Does
- Reads a list of servers from a CSV inventory
- Simulates patch execution across environments
- Logs success and failure outcomes
- Stores results in a relational database (SQLite)
- Generates a post-run summary report

## Why I Built It
I wanted to practice building automation that prioritizes traceability and operational visibility, similar to real-world infrastructure automation systems. In enterprise environments, it’s important not only that automation runs, but that results are documented, auditable, and easy to review.

## Technologies Used
- Python (automation logic)
- SQLite (lightweight relational storage)
- CSV input (server inventory simulation)
- Logging module (persistent operational logs)

## How It Works
1. Server inventory is read from a CSV file
2. Each server is “patched” through a simulated function
3. Results are logged and written to a database
4. A summary report is generated to review outcomes

## Future Improvements
- Retry logic for failed patches
- Maintenance window scheduling
- Alerting or notification hooks
- Rollback simulation for failed changes
