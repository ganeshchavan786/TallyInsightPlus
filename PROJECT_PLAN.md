# TallyBots - Integration Project Plan

**Project Name:** TallyBots  
**Location:** `D:\Microservice\TallyBots`  
**Date Created:** January 16, 2026  
**Status:** In Progress

---

## Project Structure

```
D:\Microservice\TallyBots\
├── TallyBridge/               ← Application Starter Kit (Auth, Users, Companies)
│   └── (Copied from D:\Project\Katara Dental\TDL\Pramit\Ganesh) ✅
├── TallyInsight/              ← Tally ERP Sync Microservice
│   └── (Copy from D:\Microservice\TallyInsight)
├── PROJECT_PLAN.md            ← This file
├── TASK_LIST.md               ← Task tracking
└── DATABASE_SCHEMA.md         ← Combined database schema
```

---

## Phase-wise Integration Plan

---

## PHASE 1: Project Setup & Database Design
**Duration:** 2-3 Days  
**Status:** 🔴 Pending

### 1.1 Folder Structure Setup

| Task ID | Task | Status |
|---------|------|--------|
| P1-01 | Create TallyBots folder | ✅ Done |
| P1-02 | Copy TallyBridge project to TallyBots/TallyBridge | ✅ Done |
| P1-03 | Copy TallyInsight to TallyBots/TallyInsight | ✅ Done |
| P1-04 | Update .env files for both projects | 🔴 Pending |

### 1.2 Database Tables Design

#### TallyBridge Database Tables (Auth & Multi-Tenancy)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `users` | User accounts | id, email, password_hash, role, is_active, is_verified |
| `companies` | Company/Tenant data | id, name, tally_guid, tally_server, tally_port, owner_id |
| `user_companies` | User-Company mapping | id, user_id, company_id, role |
| `permissions` | Permission definitions | id, resource, action, description |
| `role_permissions` | Role-Permission mapping | id, role, permission_id, company_id |
| `audit_trails` | Activity logs | id, user_id, action, resource_type, resource_id, old_values, new_values |
| `logs` | System logs | id, level, message, module, timestamp |
| `password_reset_tokens` | Password reset | id, user_id, token, expires_at |

#### TallyInsight Database Tables (Tally Data)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `company_config` | Tally company config | id, company_name, tally_guid, last_sync_at, last_alter_id |
| `mst_group` | Account Groups | id, company_id, tally_guid, name, parent, alter_id |
| `mst_ledger` | Ledger Accounts | id, company_id, tally_guid, name, parent, opening_balance, alter_id |
| `mst_stock_group` | Stock Groups | id, company_id, tally_guid, name, parent, alter_id |
| `mst_stock_item` | Stock Items | id, company_id, tally_guid, name, parent, opening_qty, alter_id |
| `mst_unit` | Units of Measure | id, company_id, tally_guid, name, alter_id |
| `mst_godown` | Godowns/Warehouses | id, company_id, tally_guid, name, parent, alter_id |
| `mst_cost_centre` | Cost Centres | id, company_id, tally_guid, name, parent, alter_id |
| `mst_cost_category` | Cost Categories | id, company_id, tally_guid, name, alter_id |
| `trn_voucher` | Voucher Headers | id, company_id, tally_guid, voucher_type, voucher_number, date, alter_id |
| `trn_accounting` | Accounting Entries | id, voucher_id, ledger_id, amount, is_debit |
| `trn_inventory` | Inventory Entries | id, voucher_id, stock_item_id, quantity, rate, amount |
| `audit_log` | Sync audit log | id, company_id, action, table_name, record_count, timestamp |

### 1.3 Table Relationships (Foreign Keys)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATABASE RELATIONSHIPS                                │
└─────────────────────────────────────────────────────────────────────────┘

TALLYBRIDGE DATABASE:
================

users (1) ──────────────────┬──────────────────► user_companies (N)
                            │                           │
                            │                           │
companies (1) ──────────────┴──────────────────► user_companies (N)
     │
     │ (owner_id)
     └──────────────────────────────────────────► users (1)

permissions (1) ────────────────────────────────► role_permissions (N)
                                                        │
                                                        │ (company_id)
companies (1) ──────────────────────────────────► role_permissions (N)

users (1) ──────────────────────────────────────► audit_trails (N)

users (1) ──────────────────────────────────────► password_reset_tokens (N)


TALLYINSIGHT DATABASE:
======================

company_config (1) ─────────────────────────────► mst_group (N)
       │
       ├───────────────────────────────────────► mst_ledger (N)
       │
       ├───────────────────────────────────────► mst_stock_group (N)
       │
       ├───────────────────────────────────────► mst_stock_item (N)
       │
       ├───────────────────────────────────────► trn_voucher (N)
       │
       └───────────────────────────────────────► audit_log (N)

trn_voucher (1) ────────────────────────────────► trn_accounting (N)
       │
       └───────────────────────────────────────► trn_inventory (N)

mst_ledger (1) ─────────────────────────────────► trn_accounting (N)

mst_stock_item (1) ─────────────────────────────► trn_inventory (N)


CROSS-DATABASE LINK (Integration):
==================================

TallyBridge.companies.tally_guid ◄─────────────────► TallyInsight.company_config.tally_guid
```

---

## PHASE 2: Authentication Integration
**Duration:** 2-3 Days  
**Status:** 🔴 Pending

### 2.1 Tasks

| Task ID | Task | Status | Details |
|---------|------|--------|---------|
| P2-01 | Add JWT middleware to TallyInsight | 🔴 Pending | Validate TallyBridge JWT tokens |
| P2-02 | Share SECRET_KEY between projects | 🔴 Pending | Same key in both .env files |
| P2-03 | Add user_id extraction from token | 🔴 Pending | Get current user in TallyInsight |
| P2-04 | Add company_id filter to all TallyInsight APIs | 🔴 Pending | Multi-tenant data isolation |

### 2.2 Database Tables Involved

| Table | Project | Purpose in this Phase |
|-------|---------|----------------------|
| `users` | TallyBridge | Source of user data |
| `companies` | TallyBridge | Company with tally_guid |
| `company_config` | TallyInsight | Match via tally_guid |

### 2.3 API Changes

```
TallyInsight APIs - Add JWT Auth Header:
----------------------------------------
Authorization: Bearer <jwt_token_from_tallybridge>

All APIs will:
1. Validate JWT token
2. Extract user_id
3. Get user's companies from TallyBridge
4. Filter data by company_id
```

---

## PHASE 3: Company Sync Integration
**Duration:** 3-5 Days  
**Status:** 🔴 Pending

### 3.1 Tasks

| Task ID | Task | Status | Details |
|---------|------|--------|---------|
| P3-01 | Create Tally proxy service in TallyBridge | 🔴 Pending | `app/services/tally_service.py` |
| P3-02 | Create Tally routes in TallyBridge | 🔴 Pending | `app/routes/tally.py` |
| P3-03 | Add company auto-create on sync | 🔴 Pending | Create in TallyBridge when synced |
| P3-04 | Add tally_guid to companies table | 🔴 Pending | Migration script |
| P3-05 | Link user to synced company | 🔴 Pending | Create user_companies record |

### 3.2 Database Tables Involved

| Table | Project | Operation | Purpose |
|-------|---------|-----------|---------|
| `companies` | TallyBridge | INSERT/UPDATE | Auto-create company on sync |
| `user_companies` | TallyBridge | INSERT | Link user to new company |
| `company_config` | TallyInsight | READ | Get synced company info |
| `mst_*` | TallyInsight | INSERT | Store Tally masters |
| `trn_*` | TallyInsight | INSERT | Store Tally transactions |
| `audit_log` | TallyInsight | INSERT | Log sync activity |
| `audit_trails` | TallyBridge | INSERT | Log company creation |

### 3.3 Sync Flow with Tables

```
User clicks [Sync] on Company "ABC"
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: TallyInsight fetches data from Tally ERP               │
│                                                                 │
│ Tables Updated:                                                 │
│ • company_config  → INSERT/UPDATE (company info)               │
│ • mst_group       → INSERT/UPDATE (account groups)             │
│ • mst_ledger      → INSERT/UPDATE (ledgers)                    │
│ • mst_stock_item  → INSERT/UPDATE (stock items)                │
│ • trn_voucher     → INSERT/UPDATE (vouchers)                   │
│ • trn_accounting  → INSERT/UPDATE (accounting entries)         │
│ • trn_inventory   → INSERT/UPDATE (inventory entries)          │
│ • audit_log       → INSERT (sync log)                          │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: TallyBridge receives sync complete notification             │
│                                                                 │
│ Tables Updated:                                                 │
│ • companies       → INSERT (new company with tally_guid)       │
│                   → UPDATE (last_sync_at if exists)            │
│ • user_companies  → INSERT (link user to company, role=admin)  │
│ • audit_trails    → INSERT (log company creation)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## PHASE 4: Data Access APIs
**Duration:** 3-5 Days  
**Status:** 🔴 Pending

### 4.1 Tasks

| Task ID | Task | Status | Details |
|---------|------|--------|---------|
| P4-01 | Create Ledgers API in TallyBridge | 🔴 Pending | Proxy to TallyInsight |
| P4-02 | Create Vouchers API in TallyBridge | 🔴 Pending | Proxy to TallyInsight |
| P4-03 | Create Stock Items API in TallyBridge | 🔴 Pending | Proxy to TallyInsight |
| P4-04 | Create Reports API in TallyBridge | 🔴 Pending | Trial Balance, P&L, Balance Sheet |
| P4-05 | Add pagination to all APIs | 🔴 Pending | Limit, offset, total_count |
| P4-06 | Add search/filter to APIs | 🔴 Pending | Search by name, date range |

### 4.2 Database Tables Involved

| API Endpoint | TallyInsight Tables | Ganesh Tables |
|--------------|---------------------|---------------|
| `/api/v1/tally/ledgers` | `mst_ledger`, `mst_group` | TallyBridge `companies` (for auth) |
| `/api/v1/tally/vouchers` | `trn_voucher`, `trn_accounting` | TallyBridge `companies` (for auth) |
| `/api/v1/tally/stock-items` | `mst_stock_item`, `mst_stock_group` | TallyBridge `companies` (for auth) |
| `/api/v1/tally/reports/trial-balance` | `mst_ledger`, `trn_accounting` | TallyBridge `companies` (for auth) |
| `/api/v1/tally/reports/profit-loss` | `mst_ledger`, `trn_accounting` | TallyBridge `companies` (for auth) |
| `/api/v1/tally/reports/balance-sheet` | `mst_ledger`, `trn_accounting` | TallyBridge `companies` (for auth) |

---

## PHASE 5: Frontend Integration
**Duration:** 3-5 Days  
**Status:** 🔴 Pending

### 5.1 Tasks

| Task ID | Task | Status | Details |
|---------|------|--------|---------|
| P5-01 | Copy sync.html to TallyBridge frontend | 🔴 Pending | From TallyInsight |
| P5-02 | Update sync.html API calls | 🔴 Pending | Point to Ganesh backend |
| P5-03 | Add Tally menu in sidebar | 🔴 Pending | Sync, Ledgers, Vouchers, Reports |
| P5-04 | Create tally-ledgers.html | 🔴 Pending | Ledgers list page |
| P5-05 | Create tally-vouchers.html | 🔴 Pending | Vouchers list page |
| P5-06 | Create tally-reports.html | 🔴 Pending | Reports page |
| P5-07 | Add TallyAPI to js/api.js | 🔴 Pending | Tally-related API calls |
| P5-08 | Update login redirect | 🔴 Pending | Redirect to sync.html if no company |

### 5.2 Frontend Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `TallyBridge/frontend/sync.html` | CREATE | Company sync page (from TallyInsight) |
| `frontend/tally-ledgers.html` | CREATE | Ledgers list view |
| `frontend/tally-vouchers.html` | CREATE | Vouchers list view |
| `frontend/tally-reports.html` | CREATE | Reports dashboard |
| `frontend/js/api.js` | MODIFY | Add TallyAPI object |
| `frontend/js/tally.js` | CREATE | Tally-specific functions |
| `frontend/css/tally.css` | CREATE | Tally pages styling |
| `frontend/index.html` | MODIFY | Update sidebar menu |

---

## PHASE 6: Testing & Deployment
**Duration:** 2-3 Days  
**Status:** 🔴 Pending

### 6.1 Tasks

| Task ID | Task | Status | Details |
|---------|------|--------|---------|
| P6-01 | Write integration tests | 🔴 Pending | Test sync flow end-to-end |
| P6-02 | Test multi-company scenario | 🔴 Pending | Multiple companies, switch |
| P6-03 | Test concurrent sync | 🔴 Pending | Multiple users syncing |
| P6-04 | Performance testing | 🔴 Pending | Large data sync |
| P6-05 | Create deployment scripts | 🔴 Pending | Docker compose |
| P6-06 | Documentation update | 🔴 Pending | API docs, user guide |

---

## Summary: Tables by Phase

| Phase | TallyBridge Tables | TallyInsight Tables |
|-------|---------------|---------------------|
| **Phase 1** | All tables (setup) | All tables (setup) |
| **Phase 2** | `users`, `companies` | `company_config` |
| **Phase 3** | `companies`, `user_companies`, `audit_trails` | `company_config`, `mst_*`, `trn_*`, `audit_log` |
| **Phase 4** | `companies` (auth only) | `mst_*`, `trn_*` |
| **Phase 5** | - | - |
| **Phase 6** | All tables (testing) | All tables (testing) |

---

## Quick Reference: Table Relationships

### Primary Keys & Foreign Keys

```
TALLYBRIDGE:
------------
users.id                    → user_companies.user_id
                           → audit_trails.user_id
                           → password_reset_tokens.user_id
                           → companies.owner_id

companies.id               → user_companies.company_id
                           → role_permissions.company_id

permissions.id             → role_permissions.permission_id


TALLYINSIGHT:
-------------
company_config.id          → mst_group.company_id
                           → mst_ledger.company_id
                           → mst_stock_item.company_id
                           → trn_voucher.company_id
                           → audit_log.company_id

trn_voucher.id             → trn_accounting.voucher_id
                           → trn_inventory.voucher_id

mst_ledger.id              → trn_accounting.ledger_id

mst_stock_item.id          → trn_inventory.stock_item_id


CROSS-PROJECT LINK:
-------------------
TallyBridge.companies.tally_guid = TallyInsight.company_config.tally_guid
```

---

*Document Created: January 16, 2026*  
*Last Updated: January 16, 2026*
