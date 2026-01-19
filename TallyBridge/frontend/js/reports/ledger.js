// Ledger Report JavaScript
// TallyBridge Reports Module

// State (allLedgers is in common.js)
let selectedLedger = '';
let ledgerTransactions = [];
let currentTab = 'transactions';
let sortColumn = 'date';
let sortDirection = 'desc';
let currentMainTab = 'ledgerlist';
let ledgerMasterData = [];  // Full ledger master data with 30 fields
let filteredLedgerList = [];
let ledgerListSortColumn = 'name';
let ledgerListSortDirection = 'asc';
let currentLedgerCategory = 'all';  // all, sundry_debtors, sundry_creditors

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;
    
    initializeDates();
    
    const loaded = await loadCompanies();
    console.log('Companies loaded:', loaded, 'selectedCompany:', selectedCompany);
    if (loaded && selectedCompany) {
        await loadLedgerMaster();  // Load full ledger master data
        await loadLedgerList();    // Load simple list for dropdown
    } else {
        console.warn('No company selected, cannot load ledgers');
    }
    
    setupLedgerListSorting();
});

// Company change handler
async function onCompanyChange() {
    selectedLedger = '';
    document.getElementById('ledgerSearchInput').value = '';
    document.getElementById('ledgerStats').style.display = 'none';
    document.getElementById('ledgerTabs').style.display = 'none';
    showTableEmpty('tableBody', 'Select a ledger to view transactions', 7);
    document.getElementById('tableTitle').textContent = 'Select a Ledger';
    
    await loadLedgerMaster();
    await loadLedgerList();
    showToast(`Loaded ${ledgerMasterData.length} ledgers for ${selectedCompany}`, 'success');
}

// Switch main tab (Ledger List / Transactions)
function switchMainTab(tab) {
    currentMainTab = tab;
    
    document.querySelectorAll('.report-tab[data-maintab]').forEach(t => {
        t.classList.toggle('active', t.dataset.maintab === tab);
    });
    
    document.getElementById('ledgerListView').style.display = tab === 'ledgerlist' ? 'block' : 'none';
    document.getElementById('transactionsView').style.display = tab === 'transactions' ? 'block' : 'none';
}

// Load ledger master data (30 fields)
async function loadLedgerMaster() {
    const tbody = document.getElementById('ledgerListBody');
    if (tbody) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading-cell"><div class="spinner"></div> Loading ledgers...</td></tr>';
    }
    
    try {
        console.log('Loading ledger master for company:', selectedCompany);
        const response = await apiFetch(`/api/v1/tally/ledger/master?company=${encodeURIComponent(selectedCompany)}`);
        console.log('Ledger master response:', response);
        
        ledgerMasterData = response?.ledgers || [];
        filteredLedgerList = [...ledgerMasterData];
        
        console.log(`Loaded ${ledgerMasterData.length} ledgers with full data`);
        
        renderLedgerListTable();
        
    } catch (error) {
        console.error('Failed to load ledger master:', error);
        ledgerMasterData = [];
        filteredLedgerList = [];
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading-cell">Failed to load ledgers: ' + error.message + '</td></tr>';
        }
    }
}

// Render ledger list table
function renderLedgerListTable() {
    const tbody = document.getElementById('ledgerListBody');
    const countEl = document.getElementById('ledgerListCount');
    
    if (!tbody) return;
    
    if (filteredLedgerList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading-cell">No ledgers found</td></tr>';
        if (countEl) countEl.textContent = '0 ledgers';
        return;
    }
    
    let html = '';
    filteredLedgerList.forEach(ledger => {
        const name = ledger.basic?.name || '';
        const parent = ledger.basic?.parent || '';
        const gstin = ledger.statutory?.gstin || '';
        const mobile = ledger.contact?.mobile || '';
        const email = ledger.contact?.email || '';
        const opening = ledger.balance?.opening || '';
        const closing = ledger.balance?.closing || '';
        
        const escapedName = name.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        
        html += `
            <tr onclick="openLedgerTransactions('${escapedName}')" style="cursor: pointer;">
                <td><strong>${name}</strong></td>
                <td>${parent}</td>
                <td>${gstin}</td>
                <td>${mobile}</td>
                <td>${email}</td>
                <td class="text-right">${opening}</td>
                <td class="text-right">${closing}</td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    if (countEl) countEl.textContent = `${filteredLedgerList.length} ledgers`;
}

// Switch ledger category (All / Sundry Debtors / Sundry Creditors)
function switchLedgerCategory(category) {
    currentLedgerCategory = category;
    
    // Update tab active state
    document.querySelectorAll('.report-tab[data-category]').forEach(t => {
        t.classList.toggle('active', t.dataset.category === category);
    });
    
    // Clear search
    const searchInput = document.getElementById('ledgerListSearch');
    if (searchInput) searchInput.value = '';
    
    // Apply filter
    filterLedgerList();
}

// Filter ledger list by search and category
function filterLedgerList() {
    const searchInput = document.getElementById('ledgerListSearch');
    const search = searchInput ? searchInput.value.toLowerCase() : '';
    
    // First filter by category
    let categoryFiltered = [];
    if (currentLedgerCategory === 'all') {
        categoryFiltered = [...ledgerMasterData];
    } else if (currentLedgerCategory === 'sundry_debtors') {
        categoryFiltered = ledgerMasterData.filter(ledger => {
            const parent = (ledger.basic?.parent || '').toLowerCase();
            return parent === 'sundry debtors';
        });
    } else if (currentLedgerCategory === 'sundry_creditors') {
        categoryFiltered = ledgerMasterData.filter(ledger => {
            const parent = (ledger.basic?.parent || '').toLowerCase();
            return parent === 'sundry creditors';
        });
    }
    
    // Then filter by search
    if (!search) {
        filteredLedgerList = categoryFiltered;
    } else {
        filteredLedgerList = categoryFiltered.filter(ledger => {
            const name = (ledger.basic?.name || '').toLowerCase();
            const parent = (ledger.basic?.parent || '').toLowerCase();
            const gstin = (ledger.statutory?.gstin || '').toLowerCase();
            const mobile = (ledger.contact?.mobile || '').toLowerCase();
            const email = (ledger.contact?.email || '').toLowerCase();
            
            return name.includes(search) || 
                   parent.includes(search) || 
                   gstin.includes(search) || 
                   mobile.includes(search) || 
                   email.includes(search);
        });
    }
    
    renderLedgerListTable();
}

// Open ledger transactions (click on row)
function openLedgerTransactions(ledgerName) {
    selectedLedger = ledgerName;
    document.getElementById('ledgerSearchInput').value = ledgerName;
    
    // Switch to transactions tab
    switchMainTab('transactions');
    
    // Show stats and tabs
    document.getElementById('ledgerStats').style.display = 'grid';
    document.getElementById('ledgerTabs').style.display = 'flex';
    document.getElementById('tableTitle').textContent = ledgerName;
    
    // Load transactions
    loadLedgerTransactions();
}

// Setup ledger list sorting
function setupLedgerListSorting() {
    document.querySelectorAll('#ledgerListTable th[data-sort]').forEach(th => {
        th.addEventListener('click', () => {
            const column = th.dataset.sort;
            if (ledgerListSortColumn === column) {
                ledgerListSortDirection = ledgerListSortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                ledgerListSortColumn = column;
                ledgerListSortDirection = 'asc';
            }
            updateLedgerListSortIcons();
            sortLedgerList();
            renderLedgerListTable();
        });
    });
}

// Update ledger list sort icons
function updateLedgerListSortIcons() {
    document.querySelectorAll('#ledgerListTable th[data-sort]').forEach(th => {
        const icon = th.querySelector('.sort-icon');
        if (!icon) return;
        
        if (th.dataset.sort === ledgerListSortColumn) {
            icon.textContent = ledgerListSortDirection === 'asc' ? '↑' : '↓';
        } else {
            icon.textContent = '↕';
        }
    });
}

// Sort ledger list
function sortLedgerList() {
    filteredLedgerList.sort((a, b) => {
        let aVal, bVal;
        
        switch (ledgerListSortColumn) {
            case 'name':
                aVal = a.basic?.name || '';
                bVal = b.basic?.name || '';
                break;
            case 'parent':
                aVal = a.basic?.parent || '';
                bVal = b.basic?.parent || '';
                break;
            case 'gstin':
                aVal = a.statutory?.gstin || '';
                bVal = b.statutory?.gstin || '';
                break;
            case 'mobile':
                aVal = a.contact?.mobile || '';
                bVal = b.contact?.mobile || '';
                break;
            case 'email':
                aVal = a.contact?.email || '';
                bVal = b.contact?.email || '';
                break;
            case 'opening':
                aVal = parseFloat((a.balance?.opening || '0').replace(/[₹,]/g, '')) || 0;
                bVal = parseFloat((b.balance?.opening || '0').replace(/[₹,]/g, '')) || 0;
                break;
            case 'closing':
                aVal = parseFloat((a.balance?.closing || '0').replace(/[₹,]/g, '')) || 0;
                bVal = parseFloat((b.balance?.closing || '0').replace(/[₹,]/g, '')) || 0;
                break;
            default:
                aVal = '';
                bVal = '';
        }
        
        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
        }
        
        if (aVal < bVal) return ledgerListSortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return ledgerListSortDirection === 'asc' ? 1 : -1;
        return 0;
    });
}

// Load ledger list
async function loadLedgerList() {
    try {
        console.log('Loading ledgers for company:', selectedCompany);
        const response = await apiFetch(`${CONFIG.API_BASE}/ledger/list?company=${encodeURIComponent(selectedCompany)}`);
        console.log('Ledger API response:', response);
        
        // Handle response: TallyInsight returns {total, data, ledgers} directly
        // ledgers array contains just names (strings)
        const ledgerNames = response?.ledgers || response?.data?.ledgers || [];
        allLedgers = Array.isArray(ledgerNames) ? ledgerNames : [];
        
        console.log(`Loaded ${allLedgers.length} ledgers`, allLedgers.slice(0, 5));
        
        // Show dropdown immediately after loading
        if (allLedgers.length > 0) {
            showLedgerDropdown();
        } else {
            console.warn('No ledgers found in response');
        }
    } catch (error) {
        console.error('Failed to load ledgers:', error);
        allLedgers = [];
    }
}

// Show ledger dropdown
function showLedgerDropdown() {
    const dropdown = document.getElementById('ledgerDropdown');
    if (!dropdown) {
        console.error('Dropdown element not found');
        return;
    }
    
    const searchInput = document.getElementById('ledgerSearchInput');
    const search = searchInput ? searchInput.value.toLowerCase() : '';
    
    console.log('showLedgerDropdown called, allLedgers count:', allLedgers.length, 'search:', search);
    
    const filtered = allLedgers.filter(l => {
        // ledgers array contains strings (ledger names)
        const name = typeof l === 'string' ? l : (l.name || l.ledger_name || '');
        return name.toLowerCase().includes(search);
    }).slice(0, 50); // Limit to 50 results
    
    console.log('Filtered ledgers:', filtered.length);
    
    if (filtered.length === 0) {
        dropdown.innerHTML = '<div class="dropdown-item disabled">No ledgers found</div>';
    } else {
        dropdown.innerHTML = filtered.map(l => {
            const name = typeof l === 'string' ? l : (l.name || l.ledger_name);
            const escapedName = name.replace(/'/g, "\\'").replace(/"/g, '&quot;');
            return `<div class="dropdown-item" onclick="selectLedger('${escapedName}')">${name}</div>`;
        }).join('');
    }
    
    dropdown.classList.add('show');
    dropdown.style.display = 'block';
}

// Filter ledger dropdown
function filterLedgerDropdown() {
    showLedgerDropdown();
}

// Select ledger
async function selectLedger(ledgerName) {
    selectedLedger = ledgerName;
    document.getElementById('ledgerSearchInput').value = ledgerName;
    document.getElementById('ledgerDropdown').style.display = 'none';
    
    document.getElementById('ledgerStats').style.display = 'grid';
    document.getElementById('ledgerTabs').style.display = 'flex';
    document.getElementById('tableTitle').textContent = ledgerName;
    
    await loadLedgerTransactions();
}

// Reload ledger if selected
function reloadLedgerIfSelected() {
    if (selectedLedger) {
        loadLedgerTransactions();
    }
}

// Load ledger transactions
async function loadLedgerTransactions() {
    if (!selectedLedger) return;
    
    showTableLoading('tableBody', 7);
    
    try {
        const fromDate = document.getElementById('fromDate').value;
        const toDate = document.getElementById('toDate').value;
        
        const params = new URLSearchParams();
        params.append('company', selectedCompany);
        if (fromDate) params.append('from_date', fromDate);
        if (toDate) params.append('to_date', toDate);
        
        const response = await apiFetch(`${CONFIG.API_BASE}/ledger/${encodeURIComponent(selectedLedger)}?${params}`);
        
        ledgerTransactions = response.transactions || response.data || [];
        
        updateLedgerStats(response);
        renderLedgerTable();
        showToast(`Loaded ${ledgerTransactions.length} transactions`, 'success');
    } catch (error) {
        console.error('Failed to load ledger transactions:', error);
        showToast('Failed to load transactions: ' + error.message, 'error');
        showTableEmpty('tableBody', 'Failed to load transactions', 7);
    }
}

// Update ledger stats
function updateLedgerStats(response) {
    const summary = response.summary || response;
    
    document.getElementById('ledgerOpening').textContent = formatCurrency(summary.opening_balance || 0);
    document.getElementById('ledgerDebit').textContent = formatCurrency(summary.total_debit || 0);
    document.getElementById('ledgerCredit').textContent = formatCurrency(summary.total_credit || 0);
    document.getElementById('ledgerClosing').textContent = formatCurrency(summary.closing_balance || 0);
}

// Switch ledger tab
function switchLedgerTab(tab) {
    currentTab = tab;
    
    document.querySelectorAll('.report-tab[data-tab]').forEach(t => {
        t.classList.toggle('active', t.dataset.tab === tab);
    });
    
    updateTableForTab();
    renderLedgerTable();
}

// Update table header for tab
function updateTableForTab() {
    const thead = document.getElementById('tableHead');
    
    if (currentTab === 'transactions') {
        thead.innerHTML = `
            <tr>
                <th data-sort="date" style="cursor:pointer">DATE <span class="sort-icon">↕</span></th>
                <th data-sort="particulars" style="cursor:pointer">PARTICULARS <span class="sort-icon">↕</span></th>
                <th data-sort="voucher_type" style="cursor:pointer">VOUCHER TYPE <span class="sort-icon">↕</span></th>
                <th>VOUCHER NO.</th>
                <th class="text-right" data-sort="debit" style="cursor:pointer">DEBIT <span class="sort-icon">↕</span></th>
                <th class="text-right" data-sort="credit" style="cursor:pointer">CREDIT <span class="sort-icon">↕</span></th>
                <th class="text-right">BALANCE</th>
            </tr>
        `;
    } else {
        thead.innerHTML = `
            <tr>
                <th data-sort="bill_name" style="cursor:pointer">BILL NO <span class="sort-icon">↕</span></th>
                <th data-sort="bill_date" style="cursor:pointer">BILL DATE <span class="sort-icon">↕</span></th>
                <th class="text-right" data-sort="bill_amount" style="cursor:pointer">BILL AMOUNT <span class="sort-icon">↕</span></th>
                <th class="text-right" data-sort="paid_amount" style="cursor:pointer">PAID AMOUNT <span class="sort-icon">↕</span></th>
                <th class="text-right" data-sort="pending" style="cursor:pointer">PENDING <span class="sort-icon">↕</span></th>
                <th class="text-right" data-sort="overdue_days" style="cursor:pointer">OVERDUE DAYS <span class="sort-icon">↕</span></th>
            </tr>
        `;
    }
    
    // Re-attach sorting event listeners after header update
    setupSorting();
}

// Render ledger table
function renderLedgerTable() {
    const tbody = document.getElementById('tableBody');
    
    if (currentTab === 'transactions') {
        renderTransactionsTable(tbody);
    } else {
        renderBillwiseTable(tbody);
    }
}

// Render transactions table
function renderTransactionsTable(tbody) {
    if (ledgerTransactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading-cell">No transactions found</td></tr>';
        document.getElementById('recordCount').textContent = '0 entries';
        return;
    }
    
    // Calculate running balance
    let balance = 0;
    const openingBalance = parseFloat(document.getElementById('ledgerOpening').textContent.replace(/[₹,]/g, '')) || 0;
    balance = openingBalance;
    
    let html = `
        <tr class="opening-row">
            <td></td>
            <td><strong>Opening Balance</strong></td>
            <td></td>
            <td></td>
            <td class="text-right"></td>
            <td class="text-right"></td>
            <td class="text-right"><strong>${formatAmount(openingBalance)}</strong></td>
        </tr>
    `;
    
    let totalDebit = 0;
    let totalCredit = 0;
    
    ledgerTransactions.forEach(txn => {
        const debit = parseFloat(txn.debit) || 0;
        const credit = parseFloat(txn.credit) || 0;
        // Running Balance: Previous - Debit + Credit (for Sundry Debtors)
        balance = balance - debit + credit;
        totalDebit += debit;
        totalCredit += credit;
        
        html += `
            <tr>
                <td>${formatDate(txn.date)}</td>
                <td>${txn.particulars || txn.counter_ledger || '-'}</td>
                <td>${txn.voucher_type || '-'}</td>
                <td>${txn.voucher_number || '-'}</td>
                <td class="text-right">${debit > 0 ? formatAmount(debit) : '-'}</td>
                <td class="text-right">${credit > 0 ? formatAmount(credit) : '-'}</td>
                <td class="text-right">${formatAmount(balance)}</td>
            </tr>
        `;
    });
    
    // Footer rows - Current Total and Closing Balance
    const closingBalance = openingBalance - totalDebit + totalCredit;
    const closingInDebit = closingBalance < 0;
    
    html += `
        <tr style="background: #f1f5f9; border-top: 2px solid #cbd5e1;">
            <td colspan="4" style="text-align: right; padding: 10px 16px;"><strong>Current Total :</strong></td>
            <td class="text-right" style="padding: 10px 16px;"><strong>${formatAmount(totalDebit)}</strong></td>
            <td class="text-right" style="padding: 10px 16px;"><strong>${formatAmount(totalCredit)}</strong></td>
            <td class="text-right"></td>
        </tr>
        <tr style="background: #e2e8f0;">
            <td colspan="4" style="text-align: right; padding: 10px 16px;"><strong>Closing Balance :</strong></td>
            <td class="text-right" style="padding: 10px 16px;">${closingInDebit ? '<strong>' + formatAmount(Math.abs(closingBalance)) + '</strong>' : ''}</td>
            <td class="text-right" style="padding: 10px 16px;">${!closingInDebit ? '<strong>' + formatAmount(Math.abs(closingBalance)) + '</strong>' : ''}</td>
            <td class="text-right"></td>
        </tr>
    `;
    
    tbody.innerHTML = html;
    document.getElementById('recordCount').textContent = `${ledgerTransactions.length} entries`;
}

// Render billwise table
function renderBillwiseTable(tbody) {
    // Load billwise data from API
    loadLedgerBillwise();
}

// State for billwise data
let ledgerBills = [];

// Load ledger billwise data
async function loadLedgerBillwise() {
    if (!selectedLedger) return;
    
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading-cell"><div class="spinner"></div> Loading bills...</td></tr>';
    
    try {
        const fromDate = document.getElementById('fromDate').value;
        const toDate = document.getElementById('toDate').value;
        
        const params = new URLSearchParams();
        params.append('company', selectedCompany);
        if (fromDate) params.append('from_date', fromDate);
        if (toDate) params.append('to_date', toDate);
        
        const response = await apiFetch(`${CONFIG.API_BASE}/ledger/${encodeURIComponent(selectedLedger)}/billwise?${params}`);
        console.log('Billwise response:', response);
        
        ledgerBills = response?.bills || [];
        const onAccount = response?.on_account || 0;
        
        if (ledgerBills.length === 0 && onAccount === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="loading-cell">No pending bills found</td></tr>';
            document.getElementById('recordCount').textContent = '0 bills';
            return;
        }
        
        let html = '';
        let totalPending = 0;
        
        ledgerBills.forEach(bill => {
            const billAmount = bill.opening_amount || 0;
            const pending = bill.pending_amount || 0;
            const paid = billAmount - pending;
            const overdueDays = bill.overdue_days || 0;
            totalPending += pending;
            
            html += `
                <tr>
                    <td>${bill.bill_no || '-'}</td>
                    <td>${formatDate(bill.bill_date)}</td>
                    <td class="text-right">${formatAmount(billAmount)}</td>
                    <td class="text-right">${formatAmount(paid)}</td>
                    <td class="text-right">${formatAmount(pending)}</td>
                    <td class="text-right ${overdueDays > 0 ? 'text-danger' : ''}">${overdueDays > 0 ? overdueDays + ' days' : '-'}</td>
                </tr>
            `;
        });
        
        // Add On Account row if exists
        if (onAccount !== 0) {
            html += `
                <tr class="on-account-row">
                    <td colspan="4"><strong>On Account</strong></td>
                    <td class="text-right"><strong>${formatAmount(onAccount)}</strong></td>
                    <td></td>
                </tr>
            `;
        }
        
        // Add total row
        html += `
            <tr class="total-row">
                <td colspan="4"><strong>Total</strong></td>
                <td class="text-right"><strong>${formatAmount(totalPending + onAccount)}</strong></td>
                <td></td>
            </tr>
        `;
        
        tbody.innerHTML = html;
        document.getElementById('recordCount').textContent = `${ledgerBills.length} bills`;
        
    } catch (error) {
        console.error('Failed to load billwise:', error);
        tbody.innerHTML = '<tr><td colspan="6" class="loading-cell">Failed to load bills: ' + error.message + '</td></tr>';
    }
}

// Refresh data
function refreshData() {
    if (selectedLedger) {
        loadLedgerTransactions();
    } else {
        loadLedgerList();
    }
}

// Setup sorting event listeners
function setupSorting() {
    document.querySelectorAll('.data-table th[data-sort]').forEach(th => {
        th.addEventListener('click', () => {
            const column = th.dataset.sort;
            if (sortColumn === column) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn = column;
                sortDirection = 'asc';
            }
            updateSortIcons();
            sortTransactions();
            renderTransactionsTable(document.getElementById('tableBody'));
        });
    });
}

// Update sort icons
function updateSortIcons() {
    document.querySelectorAll('.data-table th[data-sort]').forEach(th => {
        const icon = th.querySelector('.sort-icon');
        if (!icon) return;
        
        if (th.dataset.sort === sortColumn) {
            icon.textContent = sortDirection === 'asc' ? '↑' : '↓';
        } else {
            icon.textContent = '↕';
        }
    });
}

// Sort transactions
function sortTransactions() {
    ledgerTransactions.sort((a, b) => {
        let aVal = a[sortColumn];
        let bVal = b[sortColumn];
        
        if (sortColumn === 'date') {
            aVal = new Date(aVal);
            bVal = new Date(bVal);
        }
        
        if (sortColumn === 'debit' || sortColumn === 'credit') {
            aVal = parseFloat(aVal) || 0;
            bVal = parseFloat(bVal) || 0;
        }
        
        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal?.toLowerCase() || '';
        }
        
        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
    });
}

// Initialize sorting on page load
document.addEventListener('DOMContentLoaded', () => {
    setupSorting();
});

console.log('TallyBridge Reports - Ledger JS loaded');
