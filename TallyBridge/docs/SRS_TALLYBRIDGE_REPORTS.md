# Software Requirements Specification (SRS)
## TallyBridge Reports Module

**Project:** TallyBridge Dashboard Reports  
**Location:** `D:\Microservice\TallyBots\TallyBridge`  
**Date:** 17 January 2026  
**Status:** 📋 DRAFT - Pending Approval  

---

## 📑 Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [File Structure Options](#3-file-structure-options)
4. [Module 1: Voucher Report](#4-module-1-voucher-report)
5. [Module 2: Outstanding Report](#5-module-2-outstanding-report)
6. [Module 3: Ledger Report](#6-module-3-ledger-report)
7. [API Endpoints](#7-api-endpoints)
8. [Test UI Flow](#8-test-ui-flow)
9. [Test Cases](#9-test-cases)

---

## 1. Overview

### 1.1 Purpose
TallyBridge Dashboard मध्ये professional reports तयार करायचे आहेत जे TallyInsight (FastAPI) मधून data fetch करतील.

### 1.2 Reference Implementation
**Source:** `D:\Project\Katara Dental\TDL\Pramit\tally-fastapi\static\voucher-report\`

### 1.3 Reports to Implement

| # | Report | Sub-Reports | Priority |
|---|--------|-------------|----------|
| 1 | **Voucher Report** | Sales, Purchase, Payment, Receipt, Journal, Contra | High |
| 2 | **Outstanding Report** | Receivable, Payable (with 5 tabs each) | High |
| 3 | **Ledger Report** | Transactions, Bill-wise | Medium |

---

## 2. Architecture

### 2.1 System Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌────────────┐       ┌────────────┐       ┌────────────┐                  │
│   │  BROWSER   │       │ TallyBridge│       │TallyInsight│                  │
│   │            │       │            │       │            │                  │
│   │ reports/   │──────▶│ /api/v1/   │──────▶│ /api/data/ │                  │
│   │ *.html     │       │ reports/*  │       │ *          │                  │
│   │            │◀──────│            │◀──────│            │                  │
│   └────────────┘       └────────────┘       └────────────┘                  │
│        │                     │                    │                          │
│   Port: 8451            Proxy Layer          Port: 8401                     │
│   Frontend              (FastAPI)            Backend + SQLite               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Icons | Font Awesome 6.x |
| Backend Proxy | FastAPI (TallyBridge) |
| Data Source | TallyInsight API → SQLite |
| Authentication | JWT Token (existing) |

---

## 3. File Structure Options

### Option A: Single Page Application (Like Reference)
```
TallyBridge/frontend/
├── reports.html              # Single page with all 3 views
└── js/
    └── reports.js            # All report logic in one file
```

**Pros:** No page reload, shared state  
**Cons:** Large file, harder to maintain

### Option B: Separate Files (Recommended) ✅
```
TallyBridge/frontend/
├── reports/
│   ├── index.html            # Reports landing/dashboard
│   ├── vouchers.html         # Voucher report page
│   ├── outstanding.html      # Outstanding report page
│   └── ledger.html           # Ledger report page
│
├── js/
│   └── reports/
│       ├── common.js         # Shared functions (formatDate, formatCurrency)
│       ├── vouchers.js       # Voucher report logic
│       ├── outstanding.js    # Outstanding report logic
│       └── ledger.js         # Ledger report logic
│
└── css/
    └── reports.css           # Report-specific styles
```

**Pros:** Easy to maintain, team-friendly, individual testing  
**Cons:** Page reload when switching reports

### Option C: Hybrid (Single Page + Lazy Load)
```
TallyBridge/frontend/
├── reports.html              # Main container
└── js/
    └── reports/
        ├── main.js           # Router + common functions
        ├── vouchers.js       # Loaded on demand
        ├── outstanding.js    # Loaded on demand
        └── ledger.js         # Loaded on demand
```

**Pros:** Best of both worlds  
**Cons:** More complex implementation

---

## 4. Module 1: Voucher Report

### 4.1 UI Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SIDEBAR                    │  MAIN CONTENT                                   │
├────────────────────────────┼─────────────────────────────────────────────────┤
│                            │  ┌─────────────────────────────────────────┐   │
│ 🏢 Company Selector        │  │ 🔍 Search Box          [Refresh][Export] │   │
│ ┌──────────────────┐       │  └─────────────────────────────────────────┘   │
│ │ Select Company ▼ │       │                                                 │
│ └──────────────────┘       │  ┌─────────┬─────────┬─────────┬─────────┐    │
│                            │  │ Sales   │Purchase │ Payment │ Receipt │    │
│ 📄 Voucher                 │  │ ₹50,000 │₹30,000  │ ₹20,000 │ ₹15,000 │    │
│   ├── Sales ●              │  └─────────┴─────────┴─────────┴─────────┘    │
│   ├── Purchase             │                                                 │
│   ├── Payment              │  ┌─────────────────────────────────────────┐   │
│   ├── Receipt              │  │ FILTERS                            [▼]  │   │
│   ├── Journal              │  │ From: [____] To: [____] Type: [___▼]   │   │
│   └── Contra               │  │ Party: [____________]                   │   │
│                            │  │ [Today] [Week] [Month] [Year]          │   │
│ ⚖️ Outstanding             │  │ [Apply Filters] [Reset]                │   │
│   ├── Receivable           │  └─────────────────────────────────────────┘   │
│   └── Payable              │                                                 │
│                            │  ┌─────────────────────────────────────────┐   │
│ 📖 Ledger                  │  │ VOUCHER LIST                  50/page ▼│   │
│                            │  ├─────────────────────────────────────────┤   │
│ ─────────────              │  │ Date    │Type   │No.  │Party   │Amount │   │
│ 📊 Dashboard               │  │─────────┼───────┼─────┼────────┼───────│   │
│ 🔄 Sync                    │  │ 15-Jan  │Sales  │S/01 │ABC Ltd │₹5,000 │   │
│                            │  │ 14-Jan  │Sales  │S/02 │XYZ Co  │₹3,000 │   │
│                            │  │ ...     │...    │...  │...     │...    │   │
│ ─────────────              │  └─────────────────────────────────────────┘   │
│ 🏢 Current Company         │                                                 │
│                            │  [◀ 1 2 3 ... 10 ▶]  Showing 1-50 of 500       │
└────────────────────────────┴─────────────────────────────────────────────────┘
```

### 4.2 Voucher Detail Modal

```
┌─────────────────────────────────────────────────────────────────┐
│  [Sales] Voucher #S/001                                    [X]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Date: 15-Jan-2026        Party: ABC Traders                    │
│  Ref No: PO-123           Ref Date: 10-Jan-2026                 │
│  Narration: Sales invoice for goods                             │
│                                                                  │
│  ┌──────────┬──────────┬──────────┬──────────┐                  │
│  │ Ledger   │ Inventory│  Bills   │   Bank   │                  │
│  │ Entries  │  Items   │          │          │                  │
│  └──────────┴──────────┴──────────┴──────────┘                  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Ledger          │      Debit      │      Credit        │    │
│  ├─────────────────┼─────────────────┼────────────────────┤    │
│  │ ABC Traders     │          -      │     ₹15,000        │    │
│  │ Sales Account   │     ₹15,000     │          -         │    │
│  ├─────────────────┼─────────────────┼────────────────────┤    │
│  │ TOTAL           │     ₹15,000     │     ₹15,000        │    │
│  └─────────────────┴─────────────────┴────────────────────┘    │
│                                                                  │
│                                    [🖨️ Print]  [Close]          │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Voucher Types

| Type | Icon | Color | Description |
|------|------|-------|-------------|
| Sales | 🛒 | Green | Sales invoices |
| Purchase | 🚚 | Blue | Purchase bills |
| Payment | 💸 | Red | Payments made |
| Receipt | 💰 | Green | Payments received |
| Journal | 📝 | Purple | Journal entries |
| Contra | 🔄 | Orange | Bank transfers |

---

## 5. Module 2: Outstanding Report

### 5.1 Outstanding Types

| Type | Parent Group | Meaning |
|------|--------------|---------|
| **Receivable** | Sundry Debtors | Customers owe us money |
| **Payable** | Sundry Creditors | We owe suppliers money |

### 5.2 UI Layout - Outstanding View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SIDEBAR                    │  MAIN CONTENT                                   │
├────────────────────────────┼─────────────────────────────────────────────────┤
│                            │                                                 │
│ (Same as Voucher)          │  📅 Period: [01-Apr-2025] to [31-Mar-2026]     │
│                            │             [Apply] [Reset]                     │
│ ⚖️ Outstanding             │                                                 │
│   ├── Receivable ●         │  ┌─────────┬──────────┬──────────┬─────────┐   │
│   └── Payable              │  │ Ledger  │ Bill-wise│Ledger-   │ Ageing  │   │
│                            │  │         │          │wise      │         │   │
│                            │  └─────────┴──────────┴──────────┴─────────┘   │
│                            │                                                 │
│                            │  ┌─────────────────┬─────────────────┐         │
│                            │  │ Total Outstanding│    Parties     │         │
│                            │  │   ₹25,00,000    │      150       │         │
│                            │  └─────────────────┴─────────────────┘         │
│                            │                                                 │
│                            │  ┌─────────────────────────────────────────┐   │
│                            │  │ Party Name │Opening│Debit │Credit│Closing│  │
│                            │  ├────────────┼───────┼──────┼──────┼───────┤  │
│                            │  │ ABC Ltd    │10,000 │5,000 │3,000 │12,000 │  │
│                            │  │ XYZ Co     │ 8,000 │2,000 │1,000 │ 9,000 │  │
│                            │  └─────────────────────────────────────────┘   │
│                            │                                                 │
└────────────────────────────┴─────────────────────────────────────────────────┘
```

### 5.3 Outstanding Report Tabs

#### Tab 1: Ledger (Summary)
| Column | Description |
|--------|-------------|
| Party Name | Ledger/Customer name |
| Opening | Opening balance |
| Debit | Total debit transactions |
| Credit | Total credit transactions |
| Closing | Closing balance (Opening + Debit - Credit) |

#### Tab 2: Bill-wise
| Column | Description |
|--------|-------------|
| Party Name | Customer/Supplier |
| Bill No | Invoice number |
| Bill Date | Invoice date |
| Due Date | Payment due date |
| Bill Amount | Original amount |
| Paid Amount | Amount paid |
| Pending | Remaining amount |
| Overdue Days | Days past due date |

#### Tab 3: Ledger-wise
Bills grouped by party with subtotals

#### Tab 4: Ageing
| Column | Description |
|--------|-------------|
| Party Name | Customer/Supplier |
| 0-30 Days | Amount due within 30 days |
| 30-60 Days | Amount due 30-60 days |
| 60-90 Days | Amount due 60-90 days |
| 90+ Days | Amount overdue > 90 days |
| Total | Total outstanding |

#### Tab 5: Group
Group-level summary (Sundry Debtors / Sundry Creditors total)

---

## 6. Module 3: Ledger Report

### 6.1 UI Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SIDEBAR                    │  MAIN CONTENT                                   │
├────────────────────────────┼─────────────────────────────────────────────────┤
│                            │                                                 │
│ (Same as Voucher)          │  📖 Select Ledger: [Type to search...    ▼]   │
│                            │     From: [01-Apr-2025]  To: [31-Mar-2026]     │
│ 📖 Ledger ●                │                                                 │
│                            │  ┌─────────┬─────────┬─────────┬─────────┐    │
│                            │  │ Opening │  Debit  │ Credit  │ Closing │    │
│                            │  │₹10,000  │₹50,000  │₹40,000  │₹20,000  │    │
│                            │  └─────────┴─────────┴─────────┴─────────┘    │
│                            │                                                 │
│                            │  ┌────────────┬────────────┐                   │
│                            │  │Transactions│ Bill-wise  │                   │
│                            │  └────────────┴────────────┘                   │
│                            │                                                 │
│                            │  ┌─────────────────────────────────────────┐   │
│                            │  │Date │Particulars│Type│No. │Dr  │Cr │Bal│   │
│                            │  ├─────┼───────────┼────┼────┼────┼───┼───┤   │
│                            │  │     │Opening Bal│    │    │    │   │10K│   │
│                            │  │15/01│Sales A/c  │Sale│S/01│5K  │   │15K│   │
│                            │  │16/01│Bank       │Rcpt│R/01│    │3K │12K│   │
│                            │  └─────────────────────────────────────────┘   │
│                            │                                                 │
└────────────────────────────┴─────────────────────────────────────────────────┘
```

### 6.2 Ledger Report Tabs

#### Tab 1: Transactions
| Column | Description |
|--------|-------------|
| Date | Transaction date |
| Particulars | Counter ledger name |
| Voucher Type | Sales, Purchase, etc. |
| Voucher No | Voucher number |
| Debit | Debit amount |
| Credit | Credit amount |
| Balance | Running balance |

#### Tab 2: Bill-wise
| Column | Description |
|--------|-------------|
| Bill No | Invoice number |
| Bill Date | Invoice date |
| Bill Amount | Original amount |
| Paid Amount | Amount paid |
| Pending | Remaining amount |

---

## 7. API Endpoints

### 7.1 TallyBridge Proxy Routes (New)

**File:** `TallyBridge/app/routes/reports.py`

| Method | Endpoint | Description | Proxy To |
|--------|----------|-------------|----------|
| GET | `/api/v1/reports/vouchers` | Get vouchers list | `/api/data/vouchers` |
| GET | `/api/v1/reports/vouchers/{guid}` | Get voucher details | `/api/data/vouchers/{guid}/details` |
| GET | `/api/v1/reports/outstanding` | Get outstanding summary | `/api/data/outstanding` |
| GET | `/api/v1/reports/outstanding/billwise` | Get bill-wise outstanding | `/api/data/outstanding/billwise` |
| GET | `/api/v1/reports/outstanding/ledgerwise` | Get ledger-wise outstanding | `/api/data/outstanding/ledgerwise` |
| GET | `/api/v1/reports/outstanding/ageing` | Get ageing analysis | `/api/data/outstanding/ageing` |
| GET | `/api/v1/reports/outstanding/group` | Get group outstanding | `/api/data/outstanding/group` |
| GET | `/api/v1/reports/ledger/list` | Get all ledgers | `/api/data/ledgers` |
| GET | `/api/v1/reports/ledger/{name}` | Get ledger transactions | `/api/data/ledger/{name}` |

### 7.2 API Request/Response Examples

#### 7.2.1 Get Vouchers
```
GET /api/v1/reports/vouchers?voucher_type=Sales&from_date=2025-04-01&to_date=2026-03-31&company=ABC

Response:
{
  "total": 150,
  "data": [
    {
      "guid": "abc-123",
      "date": "2026-01-15",
      "voucher_type": "Sales",
      "voucher_number": "S/001",
      "party_name": "ABC Traders",
      "amount": 15000.00
    }
  ]
}
```

#### 7.2.2 Get Outstanding
```
GET /api/v1/reports/outstanding?type=receivable&company=ABC

Response:
{
  "type": "receivable",
  "data": [
    {
      "ledger_name": "ABC Traders",
      "opening": 10000.00,
      "debit": 5000.00,
      "credit": 3000.00,
      "closing": 12000.00
    }
  ],
  "count": 150,
  "totals": {
    "opening": 500000,
    "debit": 200000,
    "credit": 150000,
    "closing": 550000
  }
}
```

#### 7.2.3 Get Ageing
```
GET /api/v1/reports/outstanding/ageing?type=receivable&company=ABC

Response:
{
  "type": "receivable",
  "report_type": "ageing",
  "data": [
    {
      "party_name": "ABC Traders",
      "days_0_30": 10000,
      "days_30_60": 5000,
      "days_60_90": 3000,
      "days_90_plus": 2000,
      "total": 20000
    }
  ],
  "totals": {
    "days_0_30": 500000,
    "days_30_60": 200000,
    "days_60_90": 100000,
    "days_90_plus": 50000,
    "total": 850000
  }
}
```

---

## 8. Test UI Flow

### 8.1 Flow 1: View Sales Vouchers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TEST FLOW: VIEW SALES VOUCHERS                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: Login                                                               │
│  ─────────────────                                                           │
│  URL: http://localhost:8451/frontend/login.html                             │
│  Action: Enter credentials → Click "Sign In"                                │
│  Expected: Redirect to dashboard                                            │
│                                                                              │
│  STEP 2: Navigate to Reports                                                │
│  ─────────────────────────────                                              │
│  URL: http://localhost:8451/frontend/reports/vouchers.html                  │
│  Action: Click "Reports" in sidebar OR direct URL                           │
│  Expected: Voucher report page loads with Sales selected                    │
│                                                                              │
│  STEP 3: Select Company                                                     │
│  ─────────────────────                                                      │
│  Action: Select company from dropdown                                       │
│  Expected: Stats cards update, voucher list loads                           │
│                                                                              │
│  STEP 4: Apply Filters                                                      │
│  ───────────────────                                                        │
│  Action: Set date range, click "Apply Filters"                              │
│  Expected: Table shows filtered vouchers                                    │
│                                                                              │
│  STEP 5: View Voucher Details                                               │
│  ───────────────────────────                                                │
│  Action: Click "View" button on any voucher row                             │
│  Expected: Modal opens with voucher details (Ledger, Inventory, Bills tabs) │
│                                                                              │
│  STEP 6: Close Modal                                                        │
│  ─────────────────                                                          │
│  Action: Click "Close" or press ESC                                         │
│  Expected: Modal closes, back to voucher list                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Flow 2: View Receivable Outstanding

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      TEST FLOW: VIEW RECEIVABLE OUTSTANDING                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: Navigate to Outstanding                                            │
│  ─────────────────────────────────                                          │
│  URL: http://localhost:8451/frontend/reports/outstanding.html               │
│  Action: Click "Outstanding" → "Receivable" in sidebar                      │
│  Expected: Outstanding page loads with Receivable selected                  │
│                                                                              │
│  STEP 2: View Ledger Summary (Default Tab)                                  │
│  ─────────────────────────────────────────                                  │
│  Expected: Table shows Party Name, Opening, Debit, Credit, Closing          │
│  Expected: Stats show Total Outstanding and Party count                     │
│                                                                              │
│  STEP 3: Switch to Bill-wise Tab                                            │
│  ─────────────────────────────                                              │
│  Action: Click "Bill-wise" tab                                              │
│  Expected: Table shows individual bills with overdue days                   │
│                                                                              │
│  STEP 4: Switch to Ageing Tab                                               │
│  ──────────────────────────                                                 │
│  Action: Click "Ageing" tab                                                 │
│  Expected: Table shows 0-30, 30-60, 60-90, 90+ day buckets                 │
│                                                                              │
│  STEP 5: Change Period                                                      │
│  ───────────────────                                                        │
│  Action: Change From/To dates, click "Apply"                                │
│  Expected: Data refreshes for new period                                    │
│                                                                              │
│  STEP 6: Switch to Payable                                                  │
│  ─────────────────────                                                      │
│  Action: Click "Payable" in sidebar                                         │
│  Expected: Data changes to show Sundry Creditors                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.3 Flow 3: View Ledger Report

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TEST FLOW: VIEW LEDGER REPORT                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: Navigate to Ledger                                                 │
│  ──────────────────────────                                                 │
│  URL: http://localhost:8451/frontend/reports/ledger.html                    │
│  Action: Click "Ledger" in sidebar                                          │
│  Expected: Ledger page loads with search box                                │
│                                                                              │
│  STEP 2: Search and Select Ledger                                           │
│  ──────────────────────────────                                             │
│  Action: Type "ABC" in search box                                           │
│  Expected: Dropdown shows matching ledgers                                  │
│  Action: Click "ABC Traders"                                                │
│  Expected: Ledger transactions load, stats update                           │
│                                                                              │
│  STEP 3: View Transactions Tab                                              │
│  ─────────────────────────────                                              │
│  Expected: Table shows Date, Particulars, Type, No, Dr, Cr, Balance         │
│  Expected: Running balance calculated correctly                             │
│                                                                              │
│  STEP 4: Switch to Bill-wise Tab                                            │
│  ─────────────────────────────                                              │
│  Action: Click "Bill-wise" tab                                              │
│  Expected: Table shows bills for selected ledger                            │
│                                                                              │
│  STEP 5: Change Date Range                                                  │
│  ─────────────────────                                                      │
│  Action: Change From/To dates                                               │
│  Expected: Transactions filter by date, balances recalculate                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Test Cases

### 9.1 Voucher Report Test Cases

| TC# | Test Case | Steps | Expected Result |
|-----|-----------|-------|-----------------|
| V01 | Load vouchers | Open page, select company | Voucher list loads |
| V02 | Filter by type | Select "Purchase" from sidebar | Only Purchase vouchers shown |
| V03 | Filter by date | Set date range, apply | Vouchers within range shown |
| V04 | Search voucher | Type party name in search | Matching vouchers shown |
| V05 | View details | Click View on voucher | Modal opens with details |
| V06 | Pagination | Click page 2 | Next set of vouchers shown |
| V07 | Quick filter | Click "Today" | Today's vouchers shown |
| V08 | Export | Click Export button | Excel file downloads |

### 9.2 Outstanding Report Test Cases

| TC# | Test Case | Steps | Expected Result |
|-----|-----------|-------|-----------------|
| O01 | Load receivable | Select Receivable | Sundry Debtors data loads |
| O02 | Load payable | Select Payable | Sundry Creditors data loads |
| O03 | Ledger tab | Click Ledger tab | Summary view shown |
| O04 | Bill-wise tab | Click Bill-wise tab | Individual bills shown |
| O05 | Ageing tab | Click Ageing tab | Age buckets shown |
| O06 | Period filter | Change dates, apply | Data for period shown |
| O07 | Totals correct | Check totals | Sum matches individual rows |
| O08 | Overdue days | Check overdue column | Days calculated correctly |

### 9.3 Ledger Report Test Cases

| TC# | Test Case | Steps | Expected Result |
|-----|-----------|-------|-----------------|
| L01 | Search ledger | Type ledger name | Dropdown shows matches |
| L02 | Select ledger | Click ledger in dropdown | Transactions load |
| L03 | Running balance | Check Balance column | Correctly calculated |
| L04 | Opening balance | Check first row | Shows opening balance |
| L05 | Date filter | Change date range | Transactions filter |
| L06 | Bill-wise tab | Click Bill-wise | Bills for ledger shown |
| L07 | Stats correct | Check stats cards | Match transaction totals |

---

## 📋 Approval Checklist

| # | Item | Status |
|---|------|--------|
| 1 | File structure decision (Separate/Single/Hybrid) | ⏳ Pending |
| 2 | UI Layout approved | ⏳ Pending |
| 3 | API endpoints approved | ⏳ Pending |
| 4 | Test flows approved | ⏳ Pending |
| 5 | Ready for development | ⏳ Pending |

---

## 🔄 Next Steps (After Approval)

1. Create file structure in TallyBridge
2. Create proxy routes in `app/routes/reports.py`
3. Add service methods in `tally_service.py`
4. Create HTML pages
5. Create JavaScript files
6. Create CSS styles
7. Test each flow
8. Integration testing

---

*Document Version: 1.0*  
*Created: 17 January 2026*  
*Status: Draft - Pending User Approval*
