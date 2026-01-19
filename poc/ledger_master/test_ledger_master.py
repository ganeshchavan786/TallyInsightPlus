"""
POC: Ledger Master Data from Tally Prime
=========================================
This script tests fetching complete ledger master data from Tally Prime
including all 30 fields: Contact, Statutory, Bank details, etc.

Author: Cascade
Date: 19-Jan-2026
Reference: Katara Dental TDL Project
"""

import requests
import xml.etree.ElementTree as ET
import json

# Tally Prime Configuration
TALLY_HOST = "localhost"
TALLY_PORT = 9000
TALLY_URL = f"http://{TALLY_HOST}:{TALLY_PORT}"

# XML Request to get Ledger Master with ALL 30 fields from Tally
LEDGER_MASTER_XML = """
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
                        <FIELDS>FldGuid, FldName, FldParent, FldAlias, FldDescription, FldNotes, FldIsRevenue, FldIsDeemedPositive, FldOpeningBalance, FldClosingBalance, FldMailingName, FldMailingAddress, FldMailingState, FldMailingCountry, FldMailingPincode, FldEmail, FldMobile, FldITPAN, FldGSTN, FldGSTRegistrationType, FldGSTSupplyType, FldGSTDutyHead, FldTaxRate, FldBankAccountHolder, FldBankAccountNumber, FldBankIFSC, FldBankSWIFT, FldBankName, FldBankBranch, FldBillCreditPeriod</FIELDS>
                    </LINE>
                    
                    <!-- Basic Info -->
                    <FIELD NAME="FldGuid">
                        <SET>$Guid</SET>
                    </FIELD>
                    <FIELD NAME="FldName">
                        <SET>$Name</SET>
                    </FIELD>
                    <FIELD NAME="FldParent">
                        <SET>if $$IsEqual:$Parent:$$SysName:Primary then "" else $Parent</SET>
                    </FIELD>
                    <FIELD NAME="FldAlias">
                        <SET>$OnlyAlias</SET>
                    </FIELD>
                    <FIELD NAME="FldDescription">
                        <SET>$Description</SET>
                    </FIELD>
                    <FIELD NAME="FldNotes">
                        <SET>$Notes</SET>
                    </FIELD>
                    <FIELD NAME="FldIsRevenue">
                        <SET>$IsRevenue</SET>
                    </FIELD>
                    <FIELD NAME="FldIsDeemedPositive">
                        <SET>$IsDeemedPositive</SET>
                    </FIELD>
                    <FIELD NAME="FldOpeningBalance">
                        <SET>$OpeningBalance</SET>
                    </FIELD>
                    <FIELD NAME="FldClosingBalance">
                        <SET>$ClosingBalance</SET>
                    </FIELD>
                    
                    <!-- Contact Info -->
                    <FIELD NAME="FldMailingName">
                        <SET>$MailingName</SET>
                    </FIELD>
                    <FIELD NAME="FldMailingAddress">
                        <SET>$Address</SET>
                    </FIELD>
                    <FIELD NAME="FldMailingState">
                        <SET>$LedgerStateName</SET>
                    </FIELD>
                    <FIELD NAME="FldMailingCountry">
                        <SET>$LedgerCountryName</SET>
                    </FIELD>
                    <FIELD NAME="FldMailingPincode">
                        <SET>$Pincode</SET>
                    </FIELD>
                    <FIELD NAME="FldEmail">
                        <SET>$Email</SET>
                    </FIELD>
                    <FIELD NAME="FldMobile">
                        <SET>$LedgerMobile</SET>
                    </FIELD>
                    
                    <!-- Statutory Info -->
                    <FIELD NAME="FldITPAN">
                        <SET>$IncomeTaxNumber</SET>
                    </FIELD>
                    <FIELD NAME="FldGSTN">
                        <SET>$PartyGSTIN</SET>
                    </FIELD>
                    <FIELD NAME="FldGSTRegistrationType">
                        <SET>$GSTRegistrationType</SET>
                    </FIELD>
                    <FIELD NAME="FldGSTSupplyType">
                        <SET>$TypeOfSupply</SET>
                    </FIELD>
                    <FIELD NAME="FldGSTDutyHead">
                        <SET>$GSTDutyHead</SET>
                    </FIELD>
                    <FIELD NAME="FldTaxRate">
                        <SET>$TaxRate</SET>
                    </FIELD>
                    
                    <!-- Bank Details -->
                    <FIELD NAME="FldBankAccountHolder">
                        <SET>$BankAccountHolderName</SET>
                    </FIELD>
                    <FIELD NAME="FldBankAccountNumber">
                        <SET>$BankAccountNumber</SET>
                    </FIELD>
                    <FIELD NAME="FldBankIFSC">
                        <SET>$BankIFSCCode</SET>
                    </FIELD>
                    <FIELD NAME="FldBankSWIFT">
                        <SET>$BankSWIFTCode</SET>
                    </FIELD>
                    <FIELD NAME="FldBankName">
                        <SET>$BankName</SET>
                    </FIELD>
                    <FIELD NAME="FldBankBranch">
                        <SET>$BankBranch</SET>
                    </FIELD>
                    
                    <!-- Settings -->
                    <FIELD NAME="FldBillCreditPeriod">
                        <SET>$BillCreditPeriod</SET>
                    </FIELD>
                    
                    <COLLECTION NAME="Ledger">
                        <TYPE>Ledger</TYPE>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>
"""


def send_tally_request(xml_request: str) -> str:
    """Send XML request to Tally Prime and get response"""
    try:
        headers = {"Content-Type": "application/xml"}
        response = requests.post(TALLY_URL, data=xml_request, headers=headers, timeout=60)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to Tally at {TALLY_URL}")
        print("   Make sure Tally Prime is running with ODBC Server enabled")
        return None
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def parse_ledger_response(xml_response: str) -> list:
    """Parse Tally XML response and extract all ledgers"""
    try:
        root = ET.fromstring(xml_response)
        
        ledgers = []
        current_ledger = {}
        
        # Field mapping from TDL field names to our structure
        field_mapping = {
            "FLDGUID": "guid",
            "FLDNAME": "name",
            "FLDPARENT": "parent",
            "FLDALIAS": "alias",
            "FLDDESCRIPTION": "description",
            "FLDNOTES": "notes",
            "FLDISREVENUE": "is_revenue",
            "FLDISDEEMEDPOSITIVE": "is_deemed_positive",
            "FLDOPENINGBALANCE": "opening_balance",
            "FLDCLOSINGBALANCE": "closing_balance",
            "FLDMAILINGNAME": "mailing_name",
            "FLDMAILINGADDRESS": "address",
            "FLDMAILINGSTATE": "state",
            "FLDMAILINGCOUNTRY": "country",
            "FLDMAILINGPINCODE": "pincode",
            "FLDEMAIL": "email",
            "FLDMOBILE": "mobile",
            "FLDITPAN": "pan",
            "FLDGSTN": "gstin",
            "FLDGSTREGISTRATIONTYPE": "gst_registration_type",
            "FLDGSTSUPPLYTYPE": "gst_supply_type",
            "FLDGSTDUTYHEAD": "gst_duty_head",
            "FLDTAXRATE": "tax_rate",
            "FLDBANKACCOUNTHOLDER": "bank_account_holder",
            "FLDBANKACCOUNTNUMBER": "bank_account_number",
            "FLDBANKIFSC": "bank_ifsc",
            "FLDBANKSWIFT": "bank_swift",
            "FLDBANKNAME": "bank_name",
            "FLDBANKBRANCH": "bank_branch",
            "FLDBILLCREDITPERIOD": "credit_period"
        }
        
        # Iterate through all elements
        for elem in root.iter():
            tag = elem.tag.upper()
            text = elem.text.strip() if elem.text else ""
            
            if tag in field_mapping:
                current_ledger[field_mapping[tag]] = text
                
                # When we hit the last field, save the ledger and start new one
                if tag == "FLDBILLCREDITPERIOD":
                    if current_ledger.get("name"):  # Only save if has name
                        ledgers.append(current_ledger.copy())
                    current_ledger = {}
        
        return ledgers
    except ET.ParseError as e:
        print(f"[ERROR] XML Parse Error: {str(e)}")
        return []


def format_ledger(ledger: dict) -> dict:
    """Format single ledger into structured response"""
    return {
        "basic": {
            "guid": ledger.get("guid", ""),
            "name": ledger.get("name", ""),
            "parent": ledger.get("parent", ""),
            "alias": ledger.get("alias", ""),
            "description": ledger.get("description", ""),
            "notes": ledger.get("notes", "")
        },
        "balance": {
            "opening": ledger.get("opening_balance", ""),
            "closing": ledger.get("closing_balance", "")
        },
        "contact": {
            "mailing_name": ledger.get("mailing_name", ""),
            "address": ledger.get("address", ""),
            "state": ledger.get("state", ""),
            "country": ledger.get("country", ""),
            "pincode": ledger.get("pincode", ""),
            "email": ledger.get("email", ""),
            "mobile": ledger.get("mobile", "")
        },
        "statutory": {
            "pan": ledger.get("pan", ""),
            "gstin": ledger.get("gstin", ""),
            "gst_registration_type": ledger.get("gst_registration_type", ""),
            "gst_supply_type": ledger.get("gst_supply_type", ""),
            "gst_duty_head": ledger.get("gst_duty_head", ""),
            "tax_rate": ledger.get("tax_rate", "")
        },
        "bank": {
            "account_holder": ledger.get("bank_account_holder", ""),
            "account_number": ledger.get("bank_account_number", ""),
            "ifsc": ledger.get("bank_ifsc", ""),
            "swift": ledger.get("bank_swift", ""),
            "bank_name": ledger.get("bank_name", ""),
            "branch": ledger.get("bank_branch", "")
        },
        "settings": {
            "is_revenue": ledger.get("is_revenue", ""),
            "is_deemed_positive": ledger.get("is_deemed_positive", ""),
            "credit_period": ledger.get("credit_period", "")
        }
    }


def main():
    print("=" * 60)
    print("POC: Ledger Master Data from Tally Prime")
    print("=" * 60)
    print(f"\nConnecting to Tally at {TALLY_URL}...")
    
    # Send request
    print("\n[>] Sending XML request to Tally...")
    response = send_tally_request(LEDGER_MASTER_XML)
    
    if not response:
        return
    
    print(f"[OK] Response received from Tally ({len(response)} bytes)")
    
    # Save raw response for debugging
    with open("raw_response.xml", "w", encoding="utf-8") as f:
        f.write(response)
    print("[FILE] Raw response saved to: raw_response.xml")
    
    # Parse response
    print("\n[<] Parsing response...")
    ledgers = parse_ledger_response(response)
    
    if not ledgers:
        print("[ERROR] Failed to parse ledger data")
        print("\nRaw Response (first 2000 chars):")
        print(response[:2000])
        return
    
    print(f"[OK] Parsed {len(ledgers)} ledgers")
    
    # Format all ledgers
    formatted_ledgers = [format_ledger(l) for l in ledgers]
    
    # Create output structure
    output = {
        "total": len(formatted_ledgers),
        "ledgers": formatted_ledgers
    }
    
    # Save to JSON file
    with open("ledgers.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("[FILE] Ledger data saved to: ledgers.json")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Ledgers: {len(ledgers)}")
    
    # Count by parent group
    groups = {}
    for l in ledgers:
        parent = l.get("parent", "Primary")
        groups[parent] = groups.get(parent, 0) + 1
    
    print(f"\nLedgers by Group (Top 10):")
    for group, count in sorted(groups.items(), key=lambda x: -x[1])[:10]:
        print(f"  {group}: {count}")
    
    # Show sample ledgers
    print(f"\n" + "=" * 60)
    print("SAMPLE LEDGERS (First 5)")
    print("=" * 60)
    
    for i, ledger in enumerate(formatted_ledgers[:5], 1):
        print(f"\n{i}. {ledger['basic']['name']}")
        print(f"   Parent: {ledger['basic']['parent'] or 'Primary'}")
        print(f"   Opening: {ledger['balance']['opening'] or '0'}")
        print(f"   Closing: {ledger['balance']['closing'] or '0'}")
        if ledger['contact']['email']:
            print(f"   Email: {ledger['contact']['email']}")
        if ledger['statutory']['gstin']:
            print(f"   GSTIN: {ledger['statutory']['gstin']}")
    
    # Field verification
    print(f"\n" + "=" * 60)
    print("FIELD VERIFICATION (30 Fields)")
    print("=" * 60)
    
    fields_found = set()
    for l in ledgers:
        fields_found.update(l.keys())
    
    expected_fields = [
        "guid", "name", "parent", "alias", "description", "notes",
        "is_revenue", "is_deemed_positive", "opening_balance", "closing_balance",
        "mailing_name", "address", "state", "country", "pincode", "email", "mobile",
        "pan", "gstin", "gst_registration_type", "gst_supply_type", "gst_duty_head", "tax_rate",
        "bank_account_holder", "bank_account_number", "bank_ifsc", "bank_swift", "bank_name", "bank_branch",
        "credit_period"
    ]
    
    print(f"Expected: {len(expected_fields)} fields")
    print(f"Found: {len(fields_found)} fields")
    
    missing = set(expected_fields) - fields_found
    if missing:
        print(f"Missing: {missing}")
    else:
        print("[OK] All 30 fields retrieved successfully!")


if __name__ == "__main__":
    main()
