# Changelog

All notable changes to TallyInsightPlus will be documented in this file.

## [1.0.0] - 2026-01-17

### 🎉 Initial Release

#### Features

##### Authentication & Security
- JWT-based authentication with secure token management
- Role-based access control (Super Admin, Admin, User)
- Multi-tenant architecture with company-level isolation
- Content Security Policy (CSP) headers for XSS protection
- Secure password hashing with bcrypt

##### Reports Module
- **Voucher Report**
  - Support for Sales, Purchase, Payment, Receipt, Journal, Contra vouchers
  - Advanced filtering by date range, voucher type, party name
  - Quick filters: Today, This Week, This Month, This Year
  - Voucher detail modal with Ledger Entries, Items, Bills, Bank tabs
  - Pagination and sorting
  - Export to Excel

- **Outstanding Report**
  - Receivable and Payable reports with visual type indicator
  - Three report tabs: Ledger-wise, Bill-wise, Ageing Analysis
  - Dynamic table titles showing current report type
  - Period selector with From/To date filters
  - Party count and total outstanding summary cards

- **Ledger Report**
  - Searchable ledger dropdown with autocomplete
  - Transaction history with running balance
  - Bill-wise breakdown tab
  - Opening, Debit, Credit, Closing balance summary cards

##### Tally Integration
- Real-time sync with Tally Prime (Port 9000)
- Incremental sync using AlterID tracking
- Multi-company support with company selector
- Automatic company creation on first sync
- Webhook notifications for sync completion

##### User Interface
- Clean, responsive admin dashboard
- Professional sidebar navigation with collapsible menus
- Interactive data tables with hover effects
- Modal dialogs for detailed views
- Toast notifications for user feedback
- Print-friendly layouts

##### API Endpoints
- `/api/v1/tally/health` - Health check
- `/api/v1/tally/companies` - Get Tally companies
- `/api/v1/tally/sync` - Trigger company sync
- `/api/v1/tally/ledgers` - Get ledgers (paginated)
- `/api/v1/tally/vouchers` - Get vouchers (filtered)
- `/api/v1/reports/vouchers` - Voucher report
- `/api/v1/reports/outstanding` - Outstanding report
- `/api/v1/reports/ledger` - Ledger report

#### Technical Stack
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite (app.db for users, tally.db for Tally data)
- **Authentication**: JWT with HS256 algorithm
- **Icons**: Font Awesome 6.5.1
- **Fonts**: Inter (Google Fonts)

#### Architecture
- Microservices: TallyBridge (Port 8451) + TallyInsight (Port 8401)
- Docker support with docker-compose.yml
- Shared JWT secret for inter-service authentication

---

## Tags

- `v1.0.0` - Initial release with full Reports module
