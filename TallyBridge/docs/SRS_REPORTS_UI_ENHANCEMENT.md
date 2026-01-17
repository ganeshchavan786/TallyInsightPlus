# SRS: Reports UI Enhancement
**Date:** 2026-01-17  
**Status:** IN_PROGRESS  
**Priority:** High  
**Reference:** `D:\Project\Katara Dental\TDL\Pramit\tally-fastapi\static\voucher-report\`

---

## Objective

TallyBridge Reports UI ला Reference Implementation (tally-fastapi) सारखे professional बनवायचे आहे.

---

## 3 Reports Summary (Accounting Perspective)

### 1. Voucher Report (व्हाउचर रिपोर्ट)
**Purpose:** सर्व transactions (vouchers) पाहणे

| Voucher Type | Purpose | Color |
|--------------|---------|-------|
| Sales | माल विकला | Green |
| Purchase | माल घेतला | Blue |
| Payment | पैसे दिले | Red |
| Receipt | पैसे आले | Green |
| Journal | Adjustments | Purple |
| Contra | Bank↔Cash | Orange |

**View Modal:** Ledger Entries, Items, Bills, Bank tabs

### 2. Outstanding Report (बाकी रिपोर्ट)
**Purpose:** येणे/देणे बाकी पाहणे

| Type | Meaning |
|------|---------|
| Receivable | Customers कडून येणे (Sundry Debtors) |
| Payable | Suppliers ला देणे (Sundry Creditors) |

**5 Tabs:** Ledger, Bill-wise, Ledger-wise, Ageing, Group

### 3. Ledger Report (खातेवही)
**Purpose:** एका Party/Account चे सर्व transactions

**2 Tabs:** Transactions (running balance), Bill-wise (pending bills)

---

## Reference UI Features (tally-fastapi)

### Common Elements:
1. **Dark Sidebar** - Gradient background, icons, submenu
2. **Company Selector** - Dropdown in sidebar
3. **Top Bar** - Search + Action buttons (Refresh, Export, Print)
4. **Stats Cards** - 4 colored cards with icons
5. **Filters Card** - Collapsible, date range, type filter
6. **Data Table** - Sortable, hover effects
7. **Pagination** - Page numbers, showing info
8. **Modal** - Smooth animation, tabs, detail tables

### CSS Features:
- CSS Variables for colors
- Smooth transitions
- Box shadows
- Border radius
- Responsive design

---

## Current vs Reference Comparison

| Feature | Current TallyBridge | Reference (tally-fastapi) | Action |
|---------|--------------------|-----------------------------|--------|
| Sidebar | Light, basic | Dark gradient, professional | Update |
| Stats Cards | Basic | Colored icons, shadows | Update |
| Filters | Inline | Collapsible card | Update |
| Table | Basic | Hover, shadows | Update |
| Modal | Working but basic | Animated, polished | ✅ Done |
| Export | Missing | Excel export | Add |
| Print | Missing | Print button | Add |

---

## Task List

### Phase 1: CSS Enhancement (Use Reference CSS)
| # | Task | Status |
|---|------|--------|
| 1 | Remove inline styles from vouchers.html, use reports.css | ⏳ |
| 2 | Remove inline styles from outstanding.html, use reports.css | ⏳ |
| 3 | Remove inline styles from ledger.html, use reports.css | ⏳ |
| 4 | Add dark sidebar gradient to reports.css | ⏳ |
| 5 | Test all 3 reports | ⏳ |

### Phase 2: Feature Enhancement
| # | Task | Status |
|---|------|--------|
| 6 | Add Export to Excel functionality | ⏳ |
| 7 | Add Print functionality | ⏳ |
| 8 | Add collapsible filters | ⏳ |

### Phase 3: Polish
| # | Task | Status |
|---|------|--------|
| 9 | Test responsive design | ⏳ |
| 10 | Fix any UI issues | ⏳ |

---

## Files to Modify

### CSS:
- `frontend/css/reports.css` - Replace with reference styles

### HTML:
- `frontend/reports/vouchers.html` - Update classes
- `frontend/reports/outstanding.html` - Update classes
- `frontend/reports/ledger.html` - Update classes

### JS:
- `frontend/js/reports/vouchers.js` - Add export/print
- `frontend/js/reports/outstanding.js` - Add export/print
- `frontend/js/reports/ledger.js` - Add export/print

---

## Acceptance Criteria

1. All 3 reports have consistent, professional UI
2. Dark sidebar with gradient
3. Colored stat cards with icons
4. Collapsible filters
5. Smooth table hover effects
6. Export to Excel works
7. Print works
8. Responsive on mobile
9. Same look as reference implementation

---

## Notes

- Reference CSS is well-structured with CSS variables
- Keep existing functionality, just improve UI
- Modal already enhanced (voucher-modal.css)
