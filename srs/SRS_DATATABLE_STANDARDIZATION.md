# SRS: DataTable Component Standardization

**Version:** 1.0  
**Date:** 19 Jan 2026  
**Author:** Cascade AI  

---

## 1. Overview

### 1.1 Purpose
Standardize the DataTable component usage across all TallyBridge frontend pages to ensure consistent UI/UX.

### 1.2 Current State
VanillaNext provides a reusable `DataTable` component (`js/components/datatable.js`) with built-in features:
- Search
- Sorting (column headers)
- Pagination
- Custom cell renders
- Loading state
- Empty state

---

## 2. DataTable Component Features

### 2.1 Standard Features (from VanillaNext)

| Feature | Description | Implementation |
|---------|-------------|----------------|
| **Search** | Real-time filter | `searchable: true` |
| **Sort** | Click column header | Auto-enabled |
| **Pagination** | Page navigation | `perPage: 10` |
| **Actions** | View/Edit/Delete buttons | Custom render |
| **Loading** | Spinner overlay | `setLoading(true/false)` |
| **Empty State** | No data message | `emptyMessage: 'text'` |

### 2.2 Usage Example

```javascript
const table = new DataTable('#container', {
    columns: [
        { key: 'name', label: 'Name' },
        { key: 'status', label: 'Status', render: (v) => `<span class="badge">${v}</span>` },
        { key: 'actions', label: 'Actions', render: (v, row) => `
            <button onclick="view(${row.id})">👁️</button>
            <button onclick="edit(${row.id})">✏️</button>
            <button onclick="delete(${row.id})">🗑️</button>
        `}
    ],
    perPage: 10,
    searchable: true,
    emptyMessage: 'No records found'
});

table.setData(apiData);
```

---

## 3. Current Page Analysis

### 3.1 Pages Using DataTable ✅

| Page | Status | Notes |
|------|--------|-------|
| `users.html` | ✅ Implemented | Full features |
| `companies.html` | ✅ Implemented | Full features + View Details |
| `audit.html` | ✅ Implemented | Full features + Filters |

### 3.2 Pages NOT Using DataTable ❌

| Page | Current Implementation | Reason | Action Required |
|------|------------------------|--------|-----------------|
| `reports/vouchers.html` | Custom HTML table | Custom filters, stats | Migrate to DataTable |
| `reports/ledger.html` | Custom HTML table | Different design | Migrate to DataTable |
| `reports/outstanding.html` | Partial DataTable | Mixed approach | Complete migration |
| `tally-vouchers.html` | Custom HTML table | Old design | Deprecate or migrate |
| `tally-ledgers.html` | Custom HTML table | Old design | Deprecate or migrate |

### 3.3 Pages Without Tables (No Action)

| Page | UI Type |
|------|---------|
| `dashboard.html` | Stats cards, activity feed |
| `profile.html` | Form-based |
| `permissions.html` | Permission matrix grid |
| `tally-sync.html` | Company cards |

---

## 4. Standardization Tasks

### 4.1 Priority 1: Reports Pages

| Task | Page | Effort |
|------|------|--------|
| 1 | Migrate `reports/vouchers.html` to DataTable | Medium |
| 2 | Migrate `reports/ledger.html` to DataTable | Medium |
| 3 | Complete `reports/outstanding.html` migration | Low |

### 4.2 Priority 2: Legacy Tally Pages

| Task | Page | Effort |
|------|------|--------|
| 4 | Deprecate `tally-vouchers.html` (use reports/vouchers) | Low |
| 5 | Deprecate `tally-ledgers.html` (use reports/ledger) | Low |

---

## 5. DataTable Enhancements (Future)

### 5.1 Proposed Additions

| Feature | Description | Priority |
|---------|-------------|----------|
| **Export CSV** | Download table data | High |
| **Column Visibility** | Show/hide columns | Medium |
| **Row Selection** | Checkbox selection | Medium |
| **Bulk Actions** | Delete/Update multiple | Low |
| **Sticky Header** | Fixed header on scroll | Low |

---

## 6. File References

### 6.1 DataTable Component
- **Path:** `frontend/js/components/datatable.js`
- **Size:** 220 lines
- **Dependencies:** None (Pure Vanilla JS)

### 6.2 Required CSS
- `css/main.css` - Base styles
- `css/admin-layout.css` - Layout styles

### 6.3 Required Scripts
```html
<script src="js/components/datatable.js"></script>
```

---

## 7. Acceptance Criteria

- [ ] All list pages use DataTable component
- [ ] Consistent search, sort, pagination across pages
- [ ] Consistent action buttons (View 👁️, Edit ✏️, Delete 🗑️)
- [ ] Loading states on data fetch
- [ ] Empty states when no data
- [ ] Mobile responsive tables

---

## 8. Timeline

| Phase | Tasks | Duration |
|-------|-------|----------|
| Phase 1 | Reports pages migration | 2 days |
| Phase 2 | Legacy pages cleanup | 1 day |
| Phase 3 | Enhancements | 2 days |

**Total Estimated:** 5 days

---

**Document End**
