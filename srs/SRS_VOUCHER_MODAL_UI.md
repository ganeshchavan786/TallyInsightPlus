# SRS: Voucher Detail Modal UI Enhancement
**Date:** 2026-01-17  
**Status:** PENDING  
**Priority:** Medium  

---

## Problem Statement

Voucher View Modal दिसतंय पण UI unprofessional आहे:
1. Modal content properly styled नाही
2. Tabs (Ledger Entries, Items, Bills, Bank) दिसत नाहीत
3. Framework CSS (`modals.css`) conflict करतंय custom styles सोबत
4. `!important` overrides वापरावे लागतायत

---

## Current Issues

### 1. CSS Conflicts
- `TallyBridge/frontend/css/components/modals.css` has `.modal` with:
  - `opacity: 0; visibility: hidden;`
  - `transform: translate(-50%, -40%)`
  - Uses `.modal.show` class for visibility
- Custom inline styles conflict with framework

### 2. Missing UI Elements
- Tabs not showing (Ledger Entries, Items, Bills, Bank)
- Tab content tables not visible
- Info grid layout broken

### 3. Reference Implementation
Working modal in: `D:\Project\Katara Dental\TDL\Pramit\tally-fastapi\static\voucher-report\`
- Uses separate `style.css` without framework conflicts
- Clean modal structure with proper tabs

---

## Solution Options

### Option A: Override Framework CSS (Current - Partial)
- Use `#voucherModal` ID selector with `!important`
- Pros: Quick fix
- Cons: Messy, hard to maintain

### Option B: Create Separate Modal Component (Recommended)
- Create `voucher-modal.css` with all modal styles
- Use unique class names like `.voucher-modal`, `.voucher-modal-content`
- Avoid framework class conflicts

### Option C: Modify Framework modals.css
- Add voucher-specific modal styles to framework
- Pros: Consistent with framework
- Cons: May affect other modals

---

## Tasks

| # | Task | Status |
|---|------|--------|
| 1 | Create `voucher-modal.css` with clean styles | ⏳ Pending |
| 2 | Update `vouchers.html` to use new classes | ⏳ Pending |
| 3 | Fix tabs display (Ledger, Items, Bills, Bank) | ⏳ Pending |
| 4 | Style info grid properly | ⏳ Pending |
| 5 | Add tab content tables styling | ⏳ Pending |
| 6 | Test all voucher types | ⏳ Pending |
| 7 | Match reference implementation UI | ⏳ Pending |

---

## Files to Modify

- `TallyBridge/frontend/css/voucher-modal.css` (NEW)
- `TallyBridge/frontend/reports/vouchers.html`
- `TallyBridge/frontend/js/reports/vouchers.js`

---

## Reference UI (from tally-fastapi)

```
┌─────────────────────────────────────────────────────────────────┐
│  [Sales] Voucher #VIPL/25-26/050                            [X] │
├─────────────────────────────────────────────────────────────────┤
│  Date: 06-May-2025    Party: Machining Masters ASW Product      │
│  Ref No: -            Ref Date: -                               │
│  Narration: -                                                   │
├─────────────────────────────────────────────────────────────────┤
│  [Ledger Entries] [Items 1] [Bills 1] [Bank 0]                  │
├─────────────────────────────────────────────────────────────────┤
│  Ledger              │      Debit      │      Credit            │
│  ────────────────────┼─────────────────┼────────────────────    │
│  Party Account       │          -      │     ₹26,550            │
│  Sales Account       │     ₹22,500     │          -             │
│  CGST                │      ₹2,025     │          -             │
│  SGST                │      ₹2,025     │          -             │
│  ────────────────────┼─────────────────┼────────────────────    │
│  TOTAL               │     ₹26,550     │     ₹26,550            │
├─────────────────────────────────────────────────────────────────┤
│                                         [🖨️ Print]  [Close]     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Acceptance Criteria

1. Modal opens with smooth animation
2. All 4 tabs visible and clickable
3. Ledger entries table shows Dr/Cr with totals
4. Items tab shows inventory with qty, rate, amount
5. Bills tab shows bill allocations
6. Bank tab shows bank details (if any)
7. Close button and backdrop click close modal
8. Print button functional
9. Responsive on mobile

---

## Notes

- Current modal is functional but needs UI polish
- Framework CSS conflicts need proper resolution
- Consider creating reusable modal component for future reports
