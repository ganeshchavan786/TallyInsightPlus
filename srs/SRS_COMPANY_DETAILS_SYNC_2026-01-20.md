# SRS: Company Details Sync to Database

**Document ID:** SRS_COMPANY_DETAILS_SYNC_2026-01-20  
**Created:** 20-Jan-2026  
**Author:** Cascade AI  
**Status:** Draft  

---

## 1. Objective

Company details (Address, Email, CIN, GSTIN, PAN, etc.) सध्या Tally Prime मधून live fetch होतात. जर Tally बंद असेल तर हा data available नाही.

**Goal:** Company details database मध्ये sync करा जेणेकरून:
- PDF export Tally बंद असतानाही काम करेल
- UI faster load होईल (no live API call)
- Offline access possible

---

## 2. Current State (AS-IS)

### Data Flow (Current):
```
UI clicks "View Company Details"
    ↓
TallyBridge: GET /api/v1/tally/company/details?company=...
    ↓
TallyInsight: GET /api/sync/company/details
    ↓
Tally Prime (Live XML Request)
    ↓
Response with company data
```

### Current Tables:
| Table | Fields | Purpose |
|-------|--------|---------|
| `company_config` | company_name, company_guid, last_sync_at, books_from, books_to | Sync tracking only |

### Problem:
- Company details (address, email, CIN, etc.) **NOT stored** in database
- If Tally is offline → Company details unavailable
- PDF export cannot show company header info

---

## 3. Proposed Solution (TO-BE)

### New Table: `mst_company`

```sql
CREATE TABLE mst_company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    _company TEXT NOT NULL,           -- Company name (FK to company_config)
    guid TEXT,
    alter_id INTEGER,
    
    -- Basic Info
    name TEXT,
    formal_name TEXT,
    
    -- Address
    address TEXT,
    state TEXT,
    country TEXT,
    pincode TEXT,
    
    -- Contact
    email TEXT,
    mobile TEXT,
    telephone TEXT,
    website TEXT,
    
    -- Statutory
    gstin TEXT,
    pan TEXT,
    tan TEXT,
    cin TEXT,
    
    -- Financial Year
    books_from DATE,
    books_to DATE,
    starting_from DATE,
    
    -- Settings
    currency TEXT,
    decimal_places INTEGER,
    maintain_inventory INTEGER,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(_company)
);
```

### Data Flow (New):
```
Tally Sync Process
    ↓
Fetch Company Details (XML Request)
    ↓
Save to mst_company table
    ↓
UI/PDF reads from database (no live API needed)
```

---

## 4. Implementation Steps

### Step 1: Database Schema
**File:** `TallyInsight/app/services/database_service.py`

**Changes:**
- Add `mst_company` table definition in `_create_tables()` method

### Step 2: XML Request for Company Details
**File:** `TallyInsight/app/services/tally_service.py`

**XML Request Template:**
```xml
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>Company Details</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="Company Details Export">
                        <FORMS>Company Details Form</FORMS>
                    </REPORT>
                    <FORM NAME="Company Details Form">
                        <PARTS>Company Details Part</PARTS>
                    </FORM>
                    <PART NAME="Company Details Part">
                        <LINES>Company Details Line</LINES>
                        <REPEAT>Company Details Line : Company Collection</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="Company Details Line">
                        <FIELDS>FldName,FldFormalName,FldAddress,FldState,FldCountry,FldPincode,FldEmail,FldMobile,FldPhone,FldWebsite,FldGSTIN,FldPAN,FldTAN,FldCIN,FldBooksFrom,FldStartingFrom</FIELDS>
                    </LINE>
                    <FIELD NAME="FldName"><SET>$Name</SET></FIELD>
                    <FIELD NAME="FldFormalName"><SET>$FormalName</SET></FIELD>
                    <FIELD NAME="FldAddress"><SET>$Address</SET></FIELD>
                    <FIELD NAME="FldState"><SET>$StateName</SET></FIELD>
                    <FIELD NAME="FldCountry"><SET>$CountryName</SET></FIELD>
                    <FIELD NAME="FldPincode"><SET>$Pincode</SET></FIELD>
                    <FIELD NAME="FldEmail"><SET>$Email</SET></FIELD>
                    <FIELD NAME="FldMobile"><SET>$MobileNumber</SET></FIELD>
                    <FIELD NAME="FldPhone"><SET>$PhoneNumber</SET></FIELD>
                    <FIELD NAME="FldWebsite"><SET>$Website</SET></FIELD>
                    <FIELD NAME="FldGSTIN"><SET>$GSTIN</SET></FIELD>
                    <FIELD NAME="FldPAN"><SET>$IncomeTaxNumber</SET></FIELD>
                    <FIELD NAME="FldTAN"><SET>$TANNumber</SET></FIELD>
                    <FIELD NAME="FldCIN"><SET>$CINNumber</SET></FIELD>
                    <FIELD NAME="FldBooksFrom"><SET>$BooksFrom</SET></FIELD>
                    <FIELD NAME="FldStartingFrom"><SET>$StartingFrom</SET></FIELD>
                    <COLLECTION NAME="Company Collection">
                        <TYPE>Company</TYPE>
                        <FETCH>Name,FormalName,Address,StateName,CountryName,Pincode,Email,MobileNumber,PhoneNumber,Website,GSTIN,IncomeTaxNumber,TANNumber,CINNumber,BooksFrom,StartingFrom</FETCH>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>
```

### Step 3: Sync Service Update
**File:** `TallyInsight/app/services/sync_service.py`

**Changes:**
- Add `sync_company_details()` method
- Call this method during company sync process
- Parse XML response and save to `mst_company` table

### Step 4: API Endpoint Update
**File:** `TallyInsight/app/controllers/ledger_controller.py`

**Changes:**
- PDF endpoint: Read company details from `mst_company` table instead of live API

### Step 5: UI Update (Optional)
**File:** `TallyBridge/frontend/companies.html`

**Changes:**
- Company Details popup: Read from database first, fallback to live API

---

## 5. Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `TallyInsight/app/services/database_service.py` | **MODIFY** | Add `mst_company` table schema |
| `TallyInsight/app/services/tally_service.py` | **MODIFY** | Add XML request for company details |
| `TallyInsight/app/services/sync_service.py` | **MODIFY** | Add `sync_company_details()` method |
| `TallyInsight/app/controllers/ledger_controller.py` | **MODIFY** | PDF endpoint reads from `mst_company` |
| `TallyBridge/frontend/companies.html` | **OPTIONAL** | Read from DB first |

---

## 6. Testing Checklist

| Test Case | Expected Result |
|-----------|-----------------|
| Sync company with Tally running | `mst_company` table populated |
| View Company Details (Tally running) | Shows data from DB |
| View Company Details (Tally offline) | Shows data from DB |
| PDF Export (Tally running) | Company header shows correctly |
| PDF Export (Tally offline) | Company header shows correctly |

---

## 7. Future Use Cases

This pattern can be reused for syncing other master data:
- Stock Item details
- Ledger extended details
- Voucher Type configurations
- Cost Centers
- Godowns

---

## 8. Update Mechanism (ALTER_ID Logic)

### Tally ALTER_ID Concept:
Tally मध्ये प्रत्येक record ला `ALTER_ID` असतो. जेव्हा record बदलतो तेव्हा ALTER_ID वाढतो.

### Update Flow:
```
Every Sync:
    ↓
Fetch Company ALTER_ID from Tally
    ↓
Compare with mst_company.alter_id
    ↓
If current_alter_id > stored_alter_id → Record Changed → UPDATE
    ↓
If same → Skip (no API call needed)
```

### When Update Happens:

| Trigger | Action |
|---------|--------|
| Manual Sync button click | Check ALTER_ID & update if changed |
| Auto Sync (scheduled) | Check ALTER_ID & update if changed |
| First time sync | INSERT new company record |
| Company altered in Tally | UPDATE on next sync |

### Important:
Without ALTER_ID check, old data will keep showing even after changes in Tally!

---

## 9. Approval

- [ ] SRS Reviewed
- [ ] Database schema approved
- [ ] XML request tested
- [ ] Implementation started

---

**Next Step:** Review this SRS and approve to start implementation.
