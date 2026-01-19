"""
POC: Check Ledger Transactions from Database
Compare with Tally display to verify debit/credit logic
"""
import sqlite3
import os

# Connect to database
db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'TallyInsight', 'tally.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get ledger name from user
ledger_name = "SILICONVEINS PVT LTD"
company = "Vrushali Infotech Pvt Ltd -21 -25"

print(f"\n{'='*80}")
print(f"LEDGER: {ledger_name}")
print(f"COMPANY: {company}")
print(f"{'='*80}\n")

# Get opening balance
cur.execute("""
    SELECT name, parent, opening_balance 
    FROM mst_ledger 
    WHERE name = ? AND _company = ?
""", (ledger_name, company))
ledger = cur.fetchone()

if ledger:
    print(f"Parent Group: {ledger['parent']}")
    print(f"Opening Balance (from DB): {ledger['opening_balance']}")
else:
    print("Ledger not found!")
    exit()

# Get group info to check IsDeemedPositive
cur.execute("""
    SELECT name, is_deemedpositive, is_revenue 
    FROM mst_group 
    WHERE name = ?
""", (ledger['parent'],))
group = cur.fetchone()
if group:
    print(f"Group IsDeemedPositive: {group['is_deemedpositive']}")
    print(f"Group IsRevenue: {group['is_revenue']}")

print(f"\n{'='*80}")
print("TRANSACTIONS (Raw from trn_accounting)")
print(f"{'='*80}")
print(f"{'Date':<12} {'Voucher Type':<15} {'Vch No':<15} {'Amount':>12} {'Particulars':<30}")
print("-" * 80)

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
    LIMIT 20
""", (ledger_name, company))

transactions = cur.fetchall()
total_amount = 0
for txn in transactions:
    total_amount += txn['amount'] or 0
    print(f"{txn['date']:<12} {txn['voucher_type']:<15} {txn['voucher_number'] or '-':<15} {txn['amount']:>12.2f} {(txn['party_name'] or '-')[:30]:<30}")

print("-" * 80)
print(f"{'Total Amount (sum of all):':<45} {total_amount:>12.2f}")

opening = ledger['opening_balance'] or 0
closing = opening + total_amount
print(f"{'Opening Balance:':<45} {opening:>12.2f}")
print(f"{'Closing Balance (Opening + Total):':<45} {closing:>12.2f}")

print(f"\n{'='*80}")
print("ANALYSIS")
print(f"{'='*80}")
print("""
In Tally for Sundry Debtors (like SILICONVEINS PVT LTD):
- Sales voucher = Party Account Dr (DEBIT) = Positive for us
- Receipt voucher = Party Account Cr (CREDIT) = Negative for us
- Payment voucher = Party Account Dr (DEBIT) = Positive for us

Current DB shows:
- Sales = Negative amount (should be positive for Debit)
- This means the sign is INVERTED in our database

FIX OPTIONS:
1. Fix at sync level (change how we store amount)
2. Fix at display level (invert sign based on IsDeemedPositive)
""")

conn.close()
