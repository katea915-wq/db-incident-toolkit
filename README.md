# DB-INCIDENT-TOOLKIT

A command-line CLI tool for PostgreSQL incident diagnostics:
detects slow queries, lock waits, and table bloat

## Features
- Connects to the specified database using data in .env
- Allows to perform only certain types of checks, or all at once

- **slow_queries** — `select pid, duration, query, state`
- **lock_waits** — `select pid, usename, blocked_by, query, state`
- **table_bloat** — `select table_name, dead_rows, live_rows`

## Requirements
**External libraries (pip install):**
- `psycopg2-binary` — PostgreSQL connection
- `python-dotenv` — loading environment variables from `.env`

**Standard library:**
- `argparse` — CLI arguments parsing
- `sys` — exit on errors
- `os` — environment variables access

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
Copy `.env.example` and fill in your credentials:
```bash
cp .env.example .env
```
`.env.example`:
```
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
```
## Usage

```bash
# Run only slow queries check
python cli.py --check slow-queries

# Run only lock waits check
python cli.py --check lock-waits

# Run only table bloat check
python cli.py --check table-bloat

# Run all checks
python cli.py --check all
```

## Output
```
python cli.py --check all

--- All checks ---

--- Slow Queries ---
PID: 13656 | Duration: -1 day, 23:59:59.999375 | State: active
Query: SELECT * FROM clients
--------------------------------------------------

--- Lock Waits ---
No issues detected.

--- Table Bloat ---
Relname: clients
Dead_rows: 1560
Live_rows: 328745
--------------------------------------------------
Relname: medtech_type
Dead_rows: 162
Live_rows: 5720
..

```
## Project structure

```
DB-INCIDENT-TOOLKIT/
├── db/
│   ├── __init__.py
│   └── connection.py       # database connection
├── checks/
│   ├── __init__.py
│   ├── slow_queries.py     # detects long-running queries
│   ├── lock_waits.py       # detects blocked processes
│   └── table_bloat.py      # detects tables with high dead row count
├── cli.py                  # entry point, CLI arguments
├── .env.example            # environment variables template
├── requirements.txt        # what needs to be installed before run
└── README.md
	
```