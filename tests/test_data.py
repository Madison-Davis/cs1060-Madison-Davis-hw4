import subprocess
import sqlite3
import os

# Code obtained from ChatGPT site, personal login

# Paths relative to this test file
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(ROOT_DIR, "data.db")
ZIP_CSV = os.path.join(ROOT_DIR, "zip_county.csv")
HEALTH_CSV = os.path.join(ROOT_DIR, "county_health_rankings.csv")
CSV_TO_SQLITE = os.path.join(ROOT_DIR, "csv_to_sqlite.py")

# 1. Remove the old database if it exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("Removed existing data.db")

# 2. Run csv_to_sqlite.py to create tables
subprocess.run(["python3", CSV_TO_SQLITE, DB_PATH, ZIP_CSV], check=True)
subprocess.run(["python3", CSV_TO_SQLITE, DB_PATH, HEALTH_CSV], check=True)
print("Created tables from CSVs")

# 3. Connect to the database and check counts
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check zip_county table
cursor.execute("SELECT count(*) FROM zip_county")
zip_count = cursor.fetchone()[0]
assert zip_count == 54553, f"Expected 54553 rows in zip_county, got {zip_count}"
print("zip_county table OK:", zip_count, "rows")

# Check county_health_rankings table
cursor.execute("SELECT count(*) FROM county_health_rankings")
health_count = cursor.fetchone()[0]
assert health_count == 303864, f"Expected 303864 rows in county_health_rankings, got {health_count}"
print("county_health_rankings table OK:", health_count, "rows")

conn.close()
print("Database setup test PASS!")
