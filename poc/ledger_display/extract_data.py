"""
Extract Ledger Data from Database to JSON
POC: Ledger Display with correct Debit/Credit logic
"""
import sqlite3
import json
import os

db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'TallyInsight', 'tally.db')
output_path = os.path.join(os.path.dirname(__file__), 'data.json')

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Configuration - Change these to match Tally.pdf
LEDGER_NAME = "SILICONVEINS PVT LTD"
COMPANY = "Vrushali Infotech Pvt Ltd -21 -25"

print(f"Extracting data for: {LEDGER_NAME}")
print(f"Company: {COMPANY}")

# Get ledger info with group's is_deemedpositive
cur.execute("""
    SELECT l.name, l.parent, l.opening_balance, g.is_deemedpositive
    FROM mst_ledger l
    LEFT JOIN mst_group g ON l.parent = g.name AND l._company = g._company
    WHERE l.name = ? AND l._company = ?
""", (LEDGER_NAME, COMPANY))
ledger = cur.fetchone()

if not ledger:
    print(f"ERROR: Ledger '{LEDGER_NAME}' not found in company '{COMPANY}'")
    conn.close()
    exit(1)

# Get transactions
cur.execute("""
    SELECT 
        v.date,
        v.voucher_type,
        v.voucher_number,
        a.amount,
        v.party_name,
        v.narration
    FROM trn_accounting a
    JOIN trn_voucher v ON a.guid = v.guid
    WHERE a.ledger = ? AND a._company = ?
    ORDER BY v.date, v.voucher_number
""", (LEDGER_NAME, COMPANY))

transactions = cur.fetchall()

# Build output data
data = {
    "ledger_name": ledger['name'],
    "parent_group": ledger['parent'],
    "company": COMPANY,
    "opening_balance": ledger['opening_balance'] or 0,
    "is_deemed_positive": ledger['is_deemedpositive'] or 0,
    "transactions": []
}

for txn in transactions:
    data["transactions"].append({
        "date": txn['date'],
        "voucher_type": txn['voucher_type'],
        "voucher_number": txn['voucher_number'],
        "amount": txn['amount'] or 0,
        "particulars": txn['party_name'] or txn['narration'] or '-'
    })

# Save to JSON
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nData extracted successfully!")
print(f"Output: {output_path}")
print(f"Ledger: {data['ledger_name']}")
print(f"Parent: {data['parent_group']} (IsDeemedPositive: {data['is_deemed_positive']})")
print(f"Opening Balance: {data['opening_balance']}")
print(f"Transactions: {len(data['transactions'])}")

conn.close()
