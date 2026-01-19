"""
POC: Company Details from Tally Prime
=====================================
This script tests fetching complete company details from Tally Prime
including Email, Phone, Address, GSTIN, PAN, etc.

Author: Cascade
Date: 19-Jan-2026
"""

import requests
import xml.etree.ElementTree as ET
import json

# Tally Prime Configuration
TALLY_HOST = "localhost"
TALLY_PORT = 9000
TALLY_URL = f"http://{TALLY_HOST}:{TALLY_PORT}"

# XML Request to get Company Details with ALL fields from Tally
COMPANY_DETAILS_XML = """
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>Company Details Export</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
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
                        <REPEAT>Company Details Line : Company</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="Company Details Line">
                        <FIELDS>FldName, FldMailingName, FldGUID, FldAlterID, FldEmail, FldTelephone, FldMobile, FldFax, FldWebsite, FldAddress, FldState, FldPincode, FldCountry, FldGSTIN, FldPAN, FldTAN, FldCIN, FldStartingFrom, FldBooksFrom, FldCurrencySymbol, FldCurrencyName, FldDecimalPlaces, FldSuffixSymbol, FldAddSpace, FldShowInMillions, FldAmountWord, FldDecimalWord, FldMaintainInventory</FIELDS>
                    </LINE>
                    
                    <!-- Basic Info -->
                    <FIELD NAME="FldName">
                        <SET>$Name</SET>
                    </FIELD>
                    <FIELD NAME="FldMailingName">
                        <SET>$MailingName</SET>
                    </FIELD>
                    <FIELD NAME="FldGUID">
                        <SET>$GUID</SET>
                    </FIELD>
                    <FIELD NAME="FldAlterID">
                        <SET>$AlterID</SET>
                    </FIELD>
                    
                    <!-- Contact Info -->
                    <FIELD NAME="FldEmail">
                        <SET>$Email</SET>
                    </FIELD>
                    <FIELD NAME="FldTelephone">
                        <SET>$PhoneNumber</SET>
                    </FIELD>
                    <FIELD NAME="FldMobile">
                        <SET>$MobileNo</SET>
                    </FIELD>
                    <FIELD NAME="FldFax">
                        <SET>$FaxNo</SET>
                    </FIELD>
                    <FIELD NAME="FldWebsite">
                        <SET>$Website</SET>
                    </FIELD>
                    
                    <!-- Address -->
                    <FIELD NAME="FldAddress">
                        <SET>$Address</SET>
                    </FIELD>
                    <FIELD NAME="FldState">
                        <SET>$StateName</SET>
                    </FIELD>
                    <FIELD NAME="FldPincode">
                        <SET>$PinCode</SET>
                    </FIELD>
                    <FIELD NAME="FldCountry">
                        <SET>$CountryName</SET>
                    </FIELD>
                    
                    <!-- Statutory -->
                    <FIELD NAME="FldGSTIN">
                        <SET>$GSTIN</SET>
                    </FIELD>
                    <FIELD NAME="FldPAN">
                        <SET>$IncomeTaxNumber</SET>
                    </FIELD>
                    <FIELD NAME="FldTAN">
                        <SET>$TANNumber</SET>
                    </FIELD>
                    <FIELD NAME="FldCIN">
                        <SET>$CINNumber</SET>
                    </FIELD>
                    
                    <!-- Financial Year -->
                    <FIELD NAME="FldStartingFrom">
                        <SET>$StartingFrom</SET>
                    </FIELD>
                    <FIELD NAME="FldBooksFrom">
                        <SET>$BooksFrom</SET>
                    </FIELD>
                    
                    <!-- Currency Settings -->
                    <FIELD NAME="FldCurrencySymbol">
                        <SET>$BaseCurrencySymbol</SET>
                    </FIELD>
                    <FIELD NAME="FldCurrencyName">
                        <SET>$BaseCurrencyName</SET>
                    </FIELD>
                    <FIELD NAME="FldDecimalPlaces">
                        <SET>$DecimalPlaces</SET>
                    </FIELD>
                    <FIELD NAME="FldSuffixSymbol">
                        <SET>$IsSuffixSymbol</SET>
                    </FIELD>
                    <FIELD NAME="FldAddSpace">
                        <SET>$AddSpace</SET>
                    </FIELD>
                    <FIELD NAME="FldShowInMillions">
                        <SET>$IsShowInMillions</SET>
                    </FIELD>
                    <FIELD NAME="FldAmountWord">
                        <SET>$AmountInWords</SET>
                    </FIELD>
                    <FIELD NAME="FldDecimalWord">
                        <SET>$DecimalWord</SET>
                    </FIELD>
                    
                    <!-- Settings -->
                    <FIELD NAME="FldMaintainInventory">
                        <SET>$IsInventoryOn</SET>
                    </FIELD>
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
        response = requests.post(TALLY_URL, data=xml_request, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to Tally at {TALLY_URL}")
        print("   Make sure Tally Prime is running with ODBC Server enabled")
        return None
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def parse_company_response(xml_response: str) -> dict:
    """Parse Tally XML response and extract company details"""
    try:
        root = ET.fromstring(xml_response)
        
        # Find all field values
        company = {}
        
        # Try to find the data in response
        for elem in root.iter():
            tag = elem.tag.upper()
            text = elem.text.strip() if elem.text else ""
            
            # Map Tally fields to our structure
            field_mapping = {
                "FLDNAME": "name",
                "FLDMAILINGNAME": "mailing_name",
                "FLDGUID": "guid",
                "FLDALTERID": "alter_id",
                "FLDEMAIL": "email",
                "FLDTELEPHONE": "telephone",
                "FLDMOBILE": "mobile",
                "FLDFAX": "fax",
                "FLDWEBSITE": "website",
                "FLDADDRESS": "address",
                "FLDSTATE": "state",
                "FLDPINCODE": "pincode",
                "FLDCOUNTRY": "country",
                "FLDGSTIN": "gstin",
                "FLDPAN": "pan",
                "FLDTAN": "tan",
                "FLDCIN": "cin",
                "FLDSTARTINGFROM": "starting_from",
                "FLDBOOKSFROM": "books_from",
                "FLDCURRENCYSYMBOL": "currency_symbol",
                "FLDCURRENCYNAME": "currency_name",
                "FLDDECIMALPLACES": "decimal_places",
                "FLDSUFFIXSYMBOL": "suffix_symbol",
                "FLDADDSPACE": "add_space",
                "FLDSHOWINMILLIONS": "show_in_millions",
                "FLDAMOUNTWORD": "amount_word",
                "FLDDECIMALWORD": "decimal_word",
                "FLDMAINTAININVENTORY": "maintain_inventory"
            }
            
            if tag in field_mapping:
                company[field_mapping[tag]] = text
        
        return company
    except ET.ParseError as e:
        print(f"[ERROR] XML Parse Error: {str(e)}")
        return None


def format_company_details(company: dict) -> dict:
    """Format company details into structured response"""
    return {
        "basic": {
            "name": company.get("name", ""),
            "mailing_name": company.get("mailing_name", ""),
            "guid": company.get("guid", ""),
            "alter_id": company.get("alter_id", "")
        },
        "contact": {
            "email": company.get("email", ""),
            "telephone": company.get("telephone", ""),
            "mobile": company.get("mobile", ""),
            "fax": company.get("fax", ""),
            "website": company.get("website", "")
        },
        "address": {
            "full_address": company.get("address", ""),
            "state": company.get("state", ""),
            "pincode": company.get("pincode", ""),
            "country": company.get("country", "")
        },
        "statutory": {
            "gstin": company.get("gstin", ""),
            "pan": company.get("pan", ""),
            "tan": company.get("tan", ""),
            "cin": company.get("cin", "")
        },
        "financial_year": {
            "starting_from": company.get("starting_from", ""),
            "books_from": company.get("books_from", "")
        },
        "currency": {
            "symbol": company.get("currency_symbol", ""),
            "name": company.get("currency_name", ""),
            "decimal_places": company.get("decimal_places", ""),
            "suffix_symbol": company.get("suffix_symbol", ""),
            "add_space": company.get("add_space", ""),
            "show_in_millions": company.get("show_in_millions", ""),
            "amount_word": company.get("amount_word", ""),
            "decimal_word": company.get("decimal_word", "")
        },
        "settings": {
            "maintain_inventory": company.get("maintain_inventory", "")
        }
    }


def main():
    print("=" * 60)
    print("POC: Company Details from Tally Prime")
    print("=" * 60)
    print(f"\nConnecting to Tally at {TALLY_URL}...")
    
    # Send request
    print("\n[>] Sending XML request to Tally...")
    response = send_tally_request(COMPANY_DETAILS_XML)
    
    if not response:
        return
    
    print("[OK] Response received from Tally")
    
    # Save raw response for debugging
    with open("raw_response.xml", "w", encoding="utf-8") as f:
        f.write(response)
    print("[FILE] Raw response saved to: raw_response.xml")
    
    # Parse response
    print("\n[<] Parsing response...")
    company = parse_company_response(response)
    
    if not company:
        print("[ERROR] Failed to parse company details")
        print("\nRaw Response (first 2000 chars):")
        print(response[:2000])
        return
    
    # Format and display
    formatted = format_company_details(company)
    
    print("\n" + "=" * 60)
    print("COMPANY DETAILS")
    print("=" * 60)
    
    print(json.dumps(formatted, indent=2, ensure_ascii=False))
    
    # Save to JSON file
    with open("company_details.json", "w", encoding="utf-8") as f:
        json.dump(formatted, f, indent=2, ensure_ascii=False)
    print("\n[FILE] Company details saved to: company_details.json")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Company Name: {formatted['basic']['name']}")
    print(f"Mailing Name: {formatted['basic']['mailing_name'] or 'Not set'}")
    print(f"Email: {formatted['contact']['email'] or 'Not set'}")
    print(f"Telephone: {formatted['contact']['telephone'] or 'Not set'}")
    print(f"Mobile: {formatted['contact']['mobile'] or 'Not set'}")
    print(f"Fax: {formatted['contact']['fax'] or 'Not set'}")
    print(f"Website: {formatted['contact']['website'] or 'Not set'}")
    print(f"Address: {formatted['address']['full_address'] or 'Not set'}")
    print(f"State: {formatted['address']['state'] or 'Not set'}")
    print(f"Country: {formatted['address']['country'] or 'Not set'}")
    print(f"Pincode: {formatted['address']['pincode'] or 'Not set'}")
    print(f"GSTIN: {formatted['statutory']['gstin'] or 'Not set'}")
    print(f"PAN: {formatted['statutory']['pan'] or 'Not set'}")
    print(f"Currency: {formatted['currency']['symbol']} ({formatted['currency']['name']})")
    print(f"Decimal Places: {formatted['currency']['decimal_places']}")
    print(f"FY Start: {formatted['financial_year']['starting_from']}")
    print(f"Books From: {formatted['financial_year']['books_from']}")


if __name__ == "__main__":
    main()
