// Function to delete a property
async function deleteProperty(propertyId) {
    // Show confirmation dialog
    if (!confirm('Are you sure you want to delete this property? This action cannot be undone.')) {
        return;
    }

    try {
        // Show loading state
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.innerHTML = `
            <div class="loading-spinner"></div>
            <p>Deleting property...</p>
        `;
        document.body.appendChild(loadingOverlay);

        // Make API call to delete property
        const response = await fetch(`/api/properties/${propertyId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                // Add any authentication headers if needed
            }
        });

        if (!response.ok) {
            throw new Error('Failed to delete property');
        }

        // Show success message
        showNotification('Property deleted successfully', 'success');

        // Remove the property card from the UI
        const propertyCard = document.querySelector(`[data-property-id="${propertyId}"]`);
        if (propertyCard) {
            propertyCard.remove();
        }

        // Redirect to properties page if on property details page
        if (window.location.pathname.includes('property-details')) {
            window.location.href = '/properties.html';
        }

    } catch (error) {
        console.error('Error deleting property:', error);
        showNotification('Failed to delete property. Please try again.', 'error');
    } finally {
        // Remove loading overlay
        const loadingOverlay = document.querySelector('.loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.remove();
        }
    }
}

// Function to show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Add styles for notifications and loading overlay
const styles = `
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        color: white;
    }

    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 5px solid #f3f3f3;
        border-top: 5px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 15px;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        background: white;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-width: 300px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    }

    .notification.success {
        border-left: 4px solid #28a745;
    }

    .notification.error {
        border-left: 4px solid #dc3545;
    }

    .notification-content {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .notification i {
        font-size: 1.2rem;
    }

    .notification.success i {
        color: #28a745;
    }

    .notification.error i {
        color: #dc3545;
    }

    .notification-close {
        background: none;
        border: none;
        color: #666;
        cursor: pointer;
        padding: 0 5px;
    }

    .notification-close:hover {
        color: #333;
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;

// Add styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

// Add click event listeners to delete buttons
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-property-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const propertyId = this.dataset.propertyId;
            deleteProperty(propertyId);
        });
    });
}); 