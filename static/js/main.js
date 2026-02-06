/**
 * JavaScript for Smart Pharmacy Inventory Management System
 * Author: Senior Full Stack Python Developer
 * Purpose: Dynamic interactions, form validation, and UI enhancements
 */

// ============================================================================
// DOCUMENT READY
// ============================================================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('Smart Pharmacy System Initialized');

    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Auto-hide alerts after 5 seconds
    autoHideAlerts();

    // Add form validation
    addFormValidation();
});

// ============================================================================
// ALERT FUNCTIONS
// ============================================================================

/**
 * Auto-hide flash messages after 5 seconds
 */
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Show custom alert message
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, danger, warning, info)
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container-fluid') || document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// ============================================================================
// FORM VALIDATION
// ============================================================================

/**
 * Add Bootstrap form validation to all forms
 */
function addFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Validate stock quantity
 * @param {number} quantity - Requested quantity
 * @param {number} available - Available stock
 * @returns {boolean}
 */
function validateStock(quantity, available) {
    if (quantity > available) {
        showAlert(`Only ${available} units available in stock!`, 'danger');
        return false;
    }
    return true;
}

// ============================================================================
// SEARCH FUNCTIONALITY
// ============================================================================

/**
 * Real-time table search/filter
 * @param {string} inputId - ID of search input
 * @param {string} tableId - ID of table to search
 */
function setupTableSearch(inputId, tableId) {
    const searchInput = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    if (!searchInput || !table) return;

    searchInput.addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Format number as currency
 * @param {number} amount - Amount to format
 * @returns {string}
 */
function formatCurrency(amount) {
    return `₹${parseFloat(amount).toFixed(2)}`;
}

/**
 * Calculate days between two dates
 * @param {Date} date1 - First date
 * @param {Date} date2 - Second date
 * @returns {number}
 */
function daysBetween(date1, date2) {
    const oneDay = 24 * 60 * 60 * 1000;
    return Math.round(Math.abs((date1 - date2) / oneDay));
}

/**
 * Confirm action with user
 * @param {string} message - Confirmation message
 * @returns {boolean}
 */
function confirmAction(message) {
    return confirm(message);
}

// ============================================================================
// PRINT FUNCTIONALITY
// ============================================================================

/**
 * Print current page
 */
function printPage() {
    window.print();
}

/**
 * Print specific element
 * @param {string} elementId - ID of element to print
 */
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<html><head><title>Print</title>');
    printWindow.document.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// ============================================================================
// DATE UTILITIES
// ============================================================================

/**
 * Set minimum date for date input to today
 * @param {string} inputId - ID of date input
 */
function setMinDateToday(inputId) {
    const dateInput = document.getElementById(inputId);
    if (!dateInput) return;

    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
}

/**
 * Format date to readable string
 * @param {Date} date - Date to format
 * @returns {string}
 */
function formatDate(date) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-IN', options);
}

// ============================================================================
// ANIMATION HELPERS
// ============================================================================

/**
 * Smooth scroll to element
 * @param {string} elementId - ID of element to scroll to
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Add fade-in animation to element
 * @param {HTMLElement} element - Element to animate
 */
function fadeIn(element) {
    element.style.opacity = 0;
    element.style.display = 'block';

    let opacity = 0;
    const timer = setInterval(() => {
        if (opacity >= 1) {
            clearInterval(timer);
        }
        element.style.opacity = opacity;
        opacity += 0.1;
    }, 50);
}

// ============================================================================
// EXPORT FUNCTIONS
// ============================================================================

// Make functions available globally
window.showAlert = showAlert;
window.validateStock = validateStock;
window.setupTableSearch = setupTableSearch;
window.formatCurrency = formatCurrency;
window.confirmAction = confirmAction;
window.printPage = printPage;
window.printElement = printElement;
window.setMinDateToday = setMinDateToday;
window.formatDate = formatDate;
window.smoothScrollTo = smoothScrollTo;

console.log('✓ Smart Pharmacy JavaScript loaded successfully');
