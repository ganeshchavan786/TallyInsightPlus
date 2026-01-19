# SRS: Company Details POC

**Document Version:** 1.0  
**Date:** 19 January 2026  
**Status:** Draft - Pending Approval

---

## 1. Overview

### 1.1 Purpose
Tally Prime कडून company ची संपूर्ण माहिती (Complete Company Details) fetch करण्यासाठी Proof of Concept (POC) तयार करणे.

### 1.2 Background
सध्या TallyInsight मध्ये company sync करताना फक्त basic details मिळतात:
- Company Name
- Folder Number  
- Alter ID
- Financial Year Start/End Date

Tally Prime मध्ये company साठी जास्त data available आहे जसे Email, Phone, Address, GSTIN इत्यादी. हा POC त्या सर्व fields fetch करण्यासाठी आहे.

---

## 2. Current vs Expected

### 2.1 Current Response (Basic)
```json
{
  "name": "Vrushali Infotech Pvt Ltd",
  "folder_number": 25,
  "alter_id": 12345,
  "starting_from": "01-Apr-2025",
  "ending_at": "31-Mar-2026"
}
```

### 2.2 Expected Response (Complete)
```json
{
  "name": "Vrushali Infotech Pvt Ltd",
  "folder_number": 25,
  "alter_id": 12345,
  "guid": "abc123-def456-ghi789",
  
  "financial_year": {
    "starting_from": "01-Apr-2025",
    "ending_at": "31-Mar-2026",
    "books_beginning_from": "01-Apr-2025"
  },
  
  "contact": {
    "email": "info@vrushaliinfotech.com",
    "phone": "020-12345678",
    "mobile": "9876543210",
    "fax": "",
    "website": "www.vrushaliinfotech.com"
  },
  
  "address": {
    "line1": "123, ABC Complex",
    "line2": "MG Road",
    "city": "Pune",
    "state": "Maharashtra",
    "pincode": "411001",
    "country": "India"
  },
  
  "statutory": {
    "gstin": "27AABCV1234A1Z5",
    "pan": "AABCV1234A",
    "tan": "PNEV12345A",
    "cin": "U72200MH2020PTC123456",
    "gst_registration_type": "Regular"
  },
  
  "settings": {
    "currency_symbol": "₹",
    "currency_name": "INR",
    "decimal_places": 2,
    "maintain_accounts_only": false,
    "maintain_inventory": true
  }
}
```

---

## 3. Technical Approach

### 3.1 Tally XML Request
Tally Prime ला TDL/XML request पाठवून company details घ्यायचे:

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
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <REPORT NAME="Company Details">
            <FORMS>Company Details Form</FORMS>
          </REPORT>
          <FORM NAME="Company Details Form">
            <PARTS>Company Details Part</PARTS>
          </FORM>
          <PART NAME="Company Details Part">
            <LINES>Company Details Line</LINES>
            <REPEAT>Company Details Line : Company</REPEAT>
            <SCROLLED>Vertical</SCROLLED>
          </PART>
          <LINE NAME="Company Details Line">
            <FIELDS>FldName, FldEmail, FldPhone, FldMobile, FldAddress, FldState, FldPincode, FldGSTIN, FldPAN, FldStartDate, FldEndDate</FIELDS>
          </LINE>
          <FIELD NAME="FldName">
            <SET>$Name</SET>
          </FIELD>
          <FIELD NAME="FldEmail">
            <SET>$Email</SET>
          </FIELD>
          <FIELD NAME="FldPhone">
            <SET>$PhoneNumber</SET>
          </FIELD>
          <FIELD NAME="FldMobile">
            <SET>$MobileNumber</SET>
          </FIELD>
          <FIELD NAME="FldAddress">
            <SET>$Address</SET>
          </FIELD>
          <FIELD NAME="FldState">
            <SET>$State</SET>
          </FIELD>
          <FIELD NAME="FldPincode">
            <SET>$Pincode</SET>
          </FIELD>
          <FIELD NAME="FldGSTIN">
            <SET>$GSTIN</SET>
          </FIELD>
          <FIELD NAME="FldPAN">
            <SET>$IncomeTaxNumber</SET>
          </FIELD>
          <FIELD NAME="FldStartDate">
            <SET>$StartingFrom</SET>
          </FIELD>
          <FIELD NAME="FldEndDate">
            <SET>$EndingAt</SET>
          </FIELD>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>
```

### 3.2 Tally Company Fields Reference

| Field Name | Tally Attribute | Description |
|------------|-----------------|-------------|
| Name | $Name | Company Name |
| Email | $Email | Email Address |
| Phone | $PhoneNumber | Landline Number |
| Mobile | $MobileNumber | Mobile Number |
| Fax | $FaxNumber | Fax Number |
| Website | $Website | Website URL |
| Address | $Address | Full Address (Multi-line) |
| City | $City | City Name |
| State | $State | State Name |
| Pincode | $Pincode | PIN Code |
| Country | $Country | Country Name |
| GSTIN | $GSTIN | GST Number |
| PAN | $IncomeTaxNumber | PAN Number |
| TAN | $TANNumber | TAN Number |
| CIN | $CINNumber | CIN Number |
| Currency | $BaseCurrencySymbol | Currency Symbol |
| Starting From | $StartingFrom | FY Start Date |
| Ending At | $EndingAt | FY End Date |
| Books Beginning | $BooksFrom | Books Start Date |
| Alter ID | $AlterID | Last Alter ID |
| GUID | $GUID | Unique Identifier |

---

## 4. Implementation Tasks

### 4.1 Task List

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | TallyInsight मध्ये current company fetch code review | High | Pending |
| 2 | Tally XML request modify करणे - सर्व fields add | High | Pending |
| 3 | Response parser update करणे | High | Pending |
| 4 | New API endpoint create: `/api/company/details` | Medium | Pending |
| 5 | POC HTML page create करणे | Medium | Pending |
| 6 | Test with Tally Prime | High | Pending |
| 7 | Documentation update | Low | Pending |

### 4.2 Files to Modify/Create

**TallyInsight:**
- `app/services/tally_xml.py` - XML request templates
- `app/services/company_service.py` - Company fetch logic
- `app/controllers/company_controller.py` - API endpoints

**TallyBridge (POC):**
- `poc/company-details.html` - POC UI page
- `poc/js/company-details.js` - POC JavaScript

---

## 5. POC UI Design

### 5.1 Layout
```
┌─────────────────────────────────────────────────────────┐
│  Company Details POC                        [Refresh]   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Company: [Dropdown - Select Company]            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │ 📧 Contact Info │  │ 📍 Address      │              │
│  ├─────────────────┤  ├─────────────────┤              │
│  │ Email: xxx      │  │ Line1: xxx      │              │
│  │ Phone: xxx      │  │ City: xxx       │              │
│  │ Mobile: xxx     │  │ State: xxx      │              │
│  │ Website: xxx    │  │ Pincode: xxx    │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │ 📋 Statutory    │  │ 📅 Financial    │              │
│  ├─────────────────┤  ├─────────────────┤              │
│  │ GSTIN: xxx      │  │ FY Start: xxx   │              │
│  │ PAN: xxx        │  │ FY End: xxx     │              │
│  │ TAN: xxx        │  │ Books From: xxx │              │
│  │ CIN: xxx        │  │ Alter ID: xxx   │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 📄 Raw JSON Response                            │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ { "name": "...", "email": "...", ... }          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Success Criteria

1. ✅ Tally Prime कडून सर्व available company fields fetch होणे
2. ✅ Email, Phone, Mobile, Address fields मिळणे
3. ✅ GSTIN, PAN, TAN statutory fields मिळणे
4. ✅ POC page वर सर्व data display होणे
5. ✅ JSON response structure documented

---

## 7. Dependencies

- Tally Prime running on localhost:9000
- TallyInsight service running on localhost:8401
- Company data with Email/Phone filled in Tally

---

## 8. Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| Research | 1 day | Tally XML fields research |
| Development | 2 days | API + POC page |
| Testing | 1 day | Test with real data |
| **Total** | **4 days** | |

---

## 9. Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Developer | Cascade | 19-Jan-2026 | Draft |
| Reviewer | | | Pending |
| Approver | | | Pending |

---

**Note:** हा POC successful झाल्यावर, हे changes main TallyInsight codebase मध्ये integrate करता येतील.
