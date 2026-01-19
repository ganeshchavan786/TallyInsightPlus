# SRS: Ledger List UI Feature
**Date:** 19-Jan-2026 12:31 PM  
**Module:** Reports > Ledger

---

## Overview

Add a **Ledger List** view in the existing Ledger Report page. Users can:
1. See all ledgers in a searchable table
2. Click on any ledger to view its transactions (existing functionality)

---

## Current Flow (As-Is)
```
Ledger Report Page
    └── Search dropdown → Select ledger → Show transactions
```

## New Flow (To-Be)
```
Ledger Report Page
    ├── [TAB] Ledger List → Shows all ledgers with search
    │       └── Click row → Switch to Transactions tab with selected ledger
    │
    └── [TAB] Transactions → Existing ledger transactions view
```

---

## UI Design

### Tab Structure
| Tab | Description |
|-----|-------------|
| **Ledger List** | DataTable with all ledgers (default tab) |
| **Transactions** | Existing ledger transactions view |

### Ledger List Table Columns
| # | Column | Field | Width |
|---|--------|-------|-------|
| 1 | Name | `basic.name` | 25% |
| 2 | Parent Group | `basic.parent` | 15% |
| 3 | GSTIN | `statutory.gstin` | 15% |
| 4 | Mobile | `contact.mobile` | 12% |
| 5 | Email | `contact.email` | 18% |
| 6 | Opening Bal | `balance.opening` | 10% |
| 7 | Closing Bal | `balance.closing` | 10% |

### Features
- **Search:** Filter by name, parent, GSTIN, mobile, email
- **Sorting:** Click column headers to sort
- **Pagination:** Show 25/50/100 rows per page
- **Click Action:** Click row → Switch to Transactions tab with that ledger selected

---

## API Endpoint
```
GET /api/v1/tally/ledger/master
Response: { total: 3811, ledgers: [...] }
```

---

## Files to Modify

| # | File | Action |
|---|------|--------|
| 1 | `frontend/reports/ledger.html` | Add Ledger List tab and table |
| 2 | `frontend/js/reports/ledger.js` | Add fetchLedgerList(), renderLedgerTable(), search/filter logic |

---

## Acceptance Criteria
- [ ] Ledger List tab shows all ledgers from API
- [ ] Search filters work across all columns
- [ ] Clicking a row switches to Transactions tab with ledger selected
- [ ] Table follows existing DataTable styling (sort icons, font sizes)
- [ ] Loading state while fetching data
