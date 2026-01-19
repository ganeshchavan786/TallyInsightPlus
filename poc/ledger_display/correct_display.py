"""
POC: Correct Ledger Display with proper Debit/Credit logic
Matches Tally Prime display format
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'TallyInsight', 'tally.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

ledger_name = "SILICONVEINS PVT LTD"
company = "Vrushali Infotech Pvt Ltd. 25-26"

print(f"\n{'='*100}")
print(f"LEDGER: {ledger_name}")
print(f"{'='*100}\n")

# Get ledger info
cur.execute("""
    SELECT l.name, l.parent, l.opening_balance, g.is_deemedpositive
    FROM mst_ledger l
    LEFT JOIN mst_group g ON l.parent = g.name
    WHERE l.name = ? AND l._company = ?
""", (ledger_name, company))
ledger = cur.fetchone()

if not ledger:
    print("Ledger not found!")
    exit()

opening_balance = ledger['opening_balance'] or 0
is_deemed_positive = ledger['is_deemedpositive'] or 0

print(f"Parent: {ledger['parent']} (IsDeemedPositive: {is_deemed_positive})")
print()

# Get transactions
cur.execute("""
    SELECT 
        v.date,
        v.voucher_type,
        v.voucher_number,
        a.amount,
        v.party_name
    FROM trn_accounting a
    JOIN trn_voucher v ON a.guid = v.guid
    WHERE a.ledger = ? AND a._company = ?
    ORDER BY v.date, v.voucher_number
""", (ledger_name, company))

transactions = cur.fetchall()

# Display header
print(f"{'Date':<12} {'Particulars':<30} {'Vch Type':<12} {'Vch No':<18} {'Debit':>12} {'Credit':>12} {'Balance':>12}")
print("-" * 100)

# Opening balance row
balance = opening_balance
print(f"{'':<12} {'Opening Balance':<30} {'':<12} {'':<18} {'':<12} {'':<12} {balance:>12.2f}")

total_debit = 0
total_credit = 0

for txn in transactions:
    amount = txn['amount'] or 0
    
    # CORRECT LOGIC:
    # For IsDeemedPositive groups (Sundry Debtors, Assets):
    #   - Negative amount in DB = Debit (we receive/asset increases)
    #   - Positive amount in DB = Credit (we pay/liability increases)
    # This is because Tally stores from the perspective of the OTHER side
    
    if is_deemed_positive:
        # Invert the sign for deemed positive groups
        if amount < 0:
            debit = abs(amount)
            credit = 0
        else:
            debit = 0
            credit = amount
    else:
        # For deemed negative groups (Sundry Creditors, Liabilities)
        if amount > 0:
            debit = amount
            credit = 0
        else:
            debit = 0
            credit = abs(amount)
    
    # Running balance: Opening + Debit - Credit
    balance = balance + debit - credit
    total_debit += debit
    total_credit += credit
    
    debit_str = f"{debit:,.2f}" if debit > 0 else "-"
    credit_str = f"{credit:,.2f}" if credit > 0 else "-"
    
    print(f"{txn['date']:<12} {(txn['party_name'] or '-')[:30]:<30} {txn['voucher_type']:<12} {(txn['voucher_number'] or '-'):<18} {debit_str:>12} {credit_str:>12} {balance:>12,.2f}")

print("-" * 100)
print(f"{'':<12} {'Current Total :':<30} {'':<12} {'':<18} {total_debit:>12,.2f} {total_credit:>12,.2f} {'':<12}")
print(f"{'':<12} {'Closing Balance :':<30} {'':<12} {'':<18} {'':<12} {'':<12} {balance:>12,.2f}")
print()

# Verify
print(f"Verification:")
print(f"  Opening: {opening_balance:.2f}")
print(f"  + Debit: {total_debit:.2f}")
print(f"  - Credit: {total_credit:.2f}")
print(f"  = Closing: {opening_balance + total_debit - total_credit:.2f}")

conn.close()
