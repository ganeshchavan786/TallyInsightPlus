# SRS: Ledger Master Data POC

**Version:** 1.0  
**Date:** 19 Jan 2026  
**Author:** Cascade AI  
**Reference:** Katara Dental TDL Project (`D:\Project\Katara Dental\TDL\Pramit\TallyBI`)

---

## 1. Overview

### 1.1 Purpose
Create a standalone POC to fetch Ledger Master data directly from Tally Prime using TDL XML request, similar to the Company Details POC.

### 1.2 Scope
- Fetch all ledger fields from Tally
- Parse XML response
- Save to JSON file
- Verify all 30 fields are correctly retrieved

---

## 2. Ledger Fields (30 Fields)

### 2.1 Field Mapping Table

| # | TDL Field Name | Tally Attribute | Description |
|---|----------------|-----------------|-------------|
| 1 | FldGuid | `$Guid` | Unique identifier |
| 2 | FldName | `$Name` | Ledger name |
| 3 | FldParent | `$Parent` | Parent group |
| 4 | FldAlias | `$OnlyAlias` | Alias name |
| 5 | FldDescription | `$Description` | Description |
| 6 | FldNotes | `$Notes` | Notes |
| 7 | FldIsRevenue | `$IsRevenue` | Is revenue ledger |
| 8 | FldIsDeemedPositive | `$IsDeemedPositive` | Deemed positive |
| 9 | FldOpeningBalance | `$OpeningBalance` | Opening balance |
| 10 | FldClosingBalance | `$ClosingBalance` | Closing balance |
| 11 | FldMailingName | `$MailingName` | Mailing name |
| 12 | FldMailingAddress | `$Address` | Address |
| 13 | FldMailingState | `$LedgerStateName` | State |
| 14 | FldMailingCountry | `$LedgerCountryName` | Country |
| 15 | FldMailingPincode | `$Pincode` | Pincode |
| 16 | FldEmail | `$Email` | Email |
| 17 | FldMobile | `$LedgerMobile` | Mobile |
| 18 | FldITPAN | `$IncomeTaxNumber` | PAN number |
| 19 | FldGSTN | `$PartyGSTIN` | GSTIN |
| 20 | FldGSTRegistrationType | `$GSTRegistrationType` | GST registration type |
| 21 | FldGSTSupplyType | `$TypeOfSupply` | Supply type |
| 22 | FldGSTDutyHead | `$GSTDutyHead` | GST duty head |
| 23 | FldTaxRate | `$TaxRate` | Tax rate |
| 24 | FldBankAccountHolder | `$BankAccountHolderName` | Bank account holder |
| 25 | FldBankAccountNumber | `$BankAccountNumber` | Bank account number |
| 26 | FldBankIFSC | `$BankIFSCCode` | IFSC code |
| 27 | FldBankSWIFT | `$BankSWIFTCode` | SWIFT code |
| 28 | FldBankName | `$BankName` | Bank name |
| 29 | FldBankBranch | `$BankBranch` | Bank branch |
| 30 | FldBillCreditPeriod | `$BillCreditPeriod` | Credit period |

---

## 3. TDL XML Request

### 3.1 Request Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>LedgerReport</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="LedgerReport">
                        <FORMS>LedgerForm</FORMS>
                    </REPORT>
                    <FORM NAME="LedgerForm">
                        <PARTS>LedgerPart</PARTS>
                    </FORM>
                    <PART NAME="LedgerPart">
                        <LINES>LedgerLine</LINES>
                        <REPEAT>LedgerLine : Ledger</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="LedgerLine">
                        <FIELDS>FldGuid,FldName,FldParent,...</FIELDS>
                    </LINE>
                    <!-- Field definitions -->
                    <FIELD NAME="FldGuid">
                        <SET>$Guid</SET>
                    </FIELD>
                    <!-- ... more fields ... -->
                    <COLLECTION NAME="Ledger">
                        <TYPE>Ledger</TYPE>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>
```

### 3.2 Key Points
- **Export Format:** `$$SysName:XML` (not CSV to avoid truncation)
- **SCROLLED:** `Vertical` for large data sets
- **REPEAT:** Iterates over all ledgers

---

## 4. Expected Response

### 4.1 XML Response Structure

```xml
<ENVELOPE>
    <LEDGERREPORT>
        <LEDGERFORM>
            <LEDGERPART>
                <LEDGERLINE>
                    <FLDGUID>abc123</FLDGUID>
                    <FLDNAME>Cash</FLDNAME>
                    <FLDPARENT>Cash-in-Hand</FLDPARENT>
                    <FLDOPENINGBALANCE>10000.00</FLDOPENINGBALANCE>
                    <!-- ... more fields ... -->
                </LEDGERLINE>
                <!-- ... more ledgers ... -->
            </LEDGERPART>
        </LEDGERFORM>
    </LEDGERREPORT>
</ENVELOPE>
```

### 4.2 JSON Output Structure

```json
{
    "total": 150,
    "ledgers": [
        {
            "guid": "abc123",
            "name": "Cash",
            "parent": "Cash-in-Hand",
            "alias": "",
            "opening_balance": 10000.00,
            "closing_balance": 15000.00,
            "contact": {
                "mailing_name": "",
                "address": "",
                "state": "",
                "country": "",
                "pincode": "",
                "email": "",
                "mobile": ""
            },
            "statutory": {
                "pan": "",
                "gstin": "",
                "gst_registration_type": "",
                "gst_supply_type": ""
            },
            "bank": {
                "account_holder": "",
                "account_number": "",
                "ifsc": "",
                "swift": "",
                "bank_name": "",
                "branch": ""
            },
            "settings": {
                "is_revenue": false,
                "is_deemed_positive": false,
                "credit_period": 0
            }
        }
    ]
}
```

---

## 5. POC Implementation Plan

### 5.1 Files to Create

| # | File | Purpose |
|---|------|---------|
| 1 | `poc/ledger_master/test_ledger_master.py` | Standalone Python script |
| 2 | `poc/ledger_master/raw_response.xml` | Raw Tally response |
| 3 | `poc/ledger_master/ledgers.json` | Parsed JSON output |

### 5.2 Script Flow

```
1. Connect to Tally (localhost:9000)
2. Send TDL XML request
3. Save raw XML response
4. Parse XML to extract ledger data
5. Convert to structured JSON
6. Save JSON output
7. Print summary
```

### 5.3 Dependencies

```
- httpx (async HTTP client)
- xml.etree.ElementTree (XML parsing)
- json (JSON output)
```

---

## 6. Success Criteria

- [ ] All 30 fields retrieved from Tally
- [ ] XML response saved for debugging
- [ ] JSON output with structured data
- [ ] No data truncation (XML format, not CSV)
- [ ] Handles empty/null fields gracefully

---

## 7. Integration Plan (After POC Success)

### 7.1 TallyInsight Changes
- Add `get_ledger_master()` method to `tally_service.py`
- Add `/api/sync/ledger/master` endpoint

### 7.2 TallyBridge Changes
- Add proxy route `/api/v1/tally/ledger/master`
- Update frontend ledger dropdown

---

## 8. Reference

**Source:** Katara Dental TDL Project
- `app/core/tdl_generator.py` - TDL XML generation
- `app/services/tally_sync_service.py` - Sync logic
- `app/core/tally_parser.py` - XML parsing

---

**Document End**
