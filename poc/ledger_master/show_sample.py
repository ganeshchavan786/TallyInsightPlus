import json

data = json.load(open('ledgers.json', 'r', encoding='utf-8'))

print("=" * 70)
print("SAMPLE LEDGER DATA FOR VERIFICATION")
print("=" * 70)
print(f"Total Ledgers: {data['total']}")

# Find ledgers with GSTIN or balance
print("\n" + "=" * 70)
print("LEDGERS WITH GSTIN/BALANCE/CONTACT")
print("=" * 70)

count = 0
for l in data['ledgers']:
    has_data = (
        l['statutory']['gstin'] or 
        l['statutory']['pan'] or
        l['contact']['email'] or 
        l['contact']['mobile'] or
        (l['balance']['opening'] and l['balance']['opening'] not in ['0.00', '0', ''])
    )
    
    if has_data and count < 15:
        count += 1
        print(f"\n{count}. {l['basic']['name']}")
        print(f"   Parent: {l['basic']['parent']}")
        print(f"   Opening: {l['balance']['opening']}")
        print(f"   Closing: {l['balance']['closing']}")
        if l['statutory']['gstin']:
            print(f"   GSTIN: {l['statutory']['gstin']}")
        if l['statutory']['pan']:
            print(f"   PAN: {l['statutory']['pan']}")
        if l['contact']['email']:
            print(f"   Email: {l['contact']['email']}")
        if l['contact']['mobile']:
            print(f"   Mobile: {l['contact']['mobile']}")
        if l['contact']['address']:
            print(f"   Address: {l['contact']['address']}")
        if l['bank']['account_number']:
            print(f"   Bank A/c: {l['bank']['account_number']}")
            print(f"   Bank: {l['bank']['bank_name']}")
            print(f"   IFSC: {l['bank']['ifsc']}")

# Show all 30 fields for one ledger
print("\n" + "=" * 70)
print("COMPLETE LEDGER STRUCTURE (First ledger with data)")
print("=" * 70)

for l in data['ledgers']:
    if l['statutory']['gstin'] or l['balance']['opening'] not in ['0.00', '0', '']:
        print(json.dumps(l, indent=2, ensure_ascii=False))
        break
