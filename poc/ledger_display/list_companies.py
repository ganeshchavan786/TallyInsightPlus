import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'TallyInsight', 'tally.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("Companies in database:")
cur.execute("SELECT DISTINCT _company FROM mst_ledger LIMIT 10")
for row in cur.fetchall():
    print(f"  - '{row[0]}'")

print("\nLedgers with SILICON:")
cur.execute("SELECT name, _company FROM mst_ledger WHERE name LIKE '%SILICON%'")
for row in cur.fetchall():
    print(f"  - '{row[0]}' in '{row[1]}'")

conn.close()
