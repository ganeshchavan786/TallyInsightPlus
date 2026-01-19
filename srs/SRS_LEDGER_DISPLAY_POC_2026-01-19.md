# SRS: Ledger Display POC - Tally Style Report with PDF Export

## Document Info
- **Date:** 2026-01-19
- **Version:** 1.0
- **Status:** Draft - Pending Approval

---

## 1. Objective

Create a POC (Proof of Concept) HTML page that:
1. Displays ledger transactions **exactly like Tally Prime**
2. Uses **correct accounting debit/credit logic**
3. Exports to **PDF matching Tally.pdf format**

---

## 2. Reference Document

- **File:** `D:\Microservice\TallyBots\Tally.pdf`
- **Company:** Vrushali Infotech Pvt Ltd -21 -25
- **Ledger:** SILICONVEINS PVT LTD

---

## 3. Current Problem

| Issue | Current State | Expected (Tally) |
|-------|---------------|------------------|
| Sales Voucher | Shows in Credit column | Should show in Debit column |
| Payment Voucher | Shows in Credit column | Should show in Debit column |
| Sign Logic | amount > 0 = Debit | For Sundry Debtors: negative amount = Debit |

**Root Cause:** Database stores amount with inverted sign for IsDeemedPositive groups.

---

## 4. Correct Accounting Logic

### For Sundry Debtors (IsDeemedPositive = 1):
| Voucher Type | Tally Entry | DB Amount | Display |
|--------------|-------------|-----------|---------|
| Sales | Party Dr | Negative | **Debit** |
| Receipt | Party Cr | Positive | **Credit** |
| Payment | Party Dr | Negative | **Debit** |
| Journal (Cr) | Party Cr | Positive | **Credit** |

### For Sundry Creditors (IsDeemedPositive = 0):
| Voucher Type | Tally Entry | DB Amount | Display |
|--------------|-------------|-----------|---------|
| Purchase | Party Cr | Positive | **Credit** |
| Payment | Party Dr | Negative | **Debit** |
| Receipt | Party Cr | Positive | **Credit** |

### Formula:
```
For IsDeemedPositive = 1:
  - Negative amount → Debit column
  - Positive amount → Credit column

For IsDeemedPositive = 0:
  - Positive amount → Debit column  
  - Negative amount → Credit column

Running Balance = Opening + Debit - Credit
```

---

## 5. POC Deliverables

### 5.1 HTML Page (`poc/ledger_display/ledger_report.html`)

**Features:**
- Standalone HTML file (no server required)
- Hardcoded data from database for testing
- Tally-style table layout

**Table Structure:**
| Column | Width | Alignment |
|--------|-------|-----------|
| Date | 10% | Left |
| Particulars | 30% | Left |
| Vch Type | 10% | Center |
| Vch No. | 15% | Left |
| Debit | 12% | Right |
| Credit | 12% | Right |
| Balance | 11% | Right |

**Rows:**
1. **Opening Balance Row** - First row with opening balance in Balance column
2. **Transaction Rows** - Each transaction with correct Debit/Credit
3. **Current Total Row** - Sum of Debit and Credit columns
4. **Closing Balance Row** - Final balance

**Styling (Tally-like):**
- Header: Dark blue background (#1e3a5f), white text
- Rows: Alternating light gray (#f8f9fa) and white
- Footer rows: Light gray background
- Font: Arial/Sans-serif, 11px for data
- Borders: 1px solid #dee2e6

### 5.2 PDF Export

**Method:** Browser Print to PDF (Ctrl+P)

**Print Styles:**
- A4 Landscape orientation
- No margins/minimal margins
- Header with Company Name, Ledger Name, Date Range
- Footer with page numbers
- Clean borders for printing

---

## 6. Data Source

**Database:** `TallyInsight/tally.db`

**Tables Used:**
- `mst_ledger` - Ledger master (opening_balance, parent)
- `mst_group` - Group master (is_deemedpositive)
- `trn_accounting` - Transaction entries (ledger, amount, guid)
- `trn_voucher` - Voucher headers (date, voucher_type, voucher_number)

**Query:**
```sql
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
```

---

## 7. Implementation Steps

1. **Extract Data** - Run Python script to get JSON data from database
2. **Create HTML** - Build static HTML with hardcoded JSON data
3. **Apply Logic** - Implement correct Debit/Credit display based on IsDeemedPositive
4. **Style Table** - Match Tally.pdf appearance
5. **Add Print CSS** - Optimize for PDF export
6. **Test** - Compare with Tally.pdf side-by-side
7. **Verify** - Ensure all amounts and balance match exactly

---

## 8. Success Criteria

| Criteria | Verification |
|----------|--------------|
| Sales voucher shows in Debit column | ✓ Match Tally.pdf |
| Payment voucher shows in Debit column | ✓ Match Tally.pdf |
| Opening Balance correct | ✓ Match Tally.pdf |
| Closing Balance correct | ✓ Match Tally.pdf |
| Current Total (Debit/Credit) correct | ✓ Match Tally.pdf |
| PDF export looks like Tally.pdf | ✓ Visual comparison |

---

## 9. Files to Create

| File | Purpose |
|------|---------|
| `poc/ledger_display/extract_data.py` | Extract data from DB to JSON |
| `poc/ledger_display/ledger_report.html` | Main HTML report |
| `poc/ledger_display/data.json` | Extracted ledger data |

---

## 10. Timeline

| Task | Duration |
|------|----------|
| Data extraction script | 10 min |
| HTML structure | 15 min |
| Debit/Credit logic | 10 min |
| Styling (Tally-like) | 15 min |
| Print CSS | 10 min |
| Testing & verification | 10 min |
| **Total** | **~1 hour** |

---

## 11. After POC Approval

If POC matches Tally.pdf exactly:
1. User will review and approve POC
2. **Only then** implement same logic in original project files
3. Original project files will NOT be touched during POC phase

---

## Approval

- [ ] SRS Approved
- [ ] Ready to implement POC

---

**Note:** POC uses hardcoded data. After verification, same logic will be applied to live API.
