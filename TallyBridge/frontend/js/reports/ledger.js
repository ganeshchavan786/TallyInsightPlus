// Ledger Report JavaScript
// TallyBridge Reports Module

// State (allLedgers is in common.js)
let selectedLedger = '';
let ledgerTransactions = [];
let currentTab = 'transactions';
let sortColumn = 'date';
let sortDirection = 'desc';

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;
    
    initializeDates();
    
    const loaded = await loadCompanies();
    console.log('Companies loaded:', loaded, 'selectedCompany:', selectedCompany);
    if (loaded && selectedCompany) {
        await loadLedgerList();
    } else {
        console.warn('No company selected, cannot load ledgers');
    }
});

// Company change handler
async function onCompanyChange() {
    selectedLedger = '';
    document.getElementById('ledgerSearchInput').value = '';
    document.getElementById('ledgerStats').style.display = 'none';
    document.getElementById('ledgerTabs').style.display = 'none';
    showTableEmpty('tableBody', 'Select a ledger to view transactions', 7);
    document.getElementById('tableTitle').textContent = 'Select a Ledger';
    
    await loadLedgerList();
    showToast(`Loaded ${allLedgers.length} ledgers for ${selectedCompany}`, 'success');
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
    
    ledgerTransactions.forEach(txn => {
        const debit = parseFloat(txn.debit) || 0;
        const credit = parseFloat(txn.credit) || 0;
        balance = balance + debit - credit;
        
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
