// Main Application Logic
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle image gallery
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.querySelector('.main-image');
    if (thumbnails.length && mainImage) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', () => {
                mainImage.src = thumbnail.src;
                thumbnails.forEach(t => t.classList.remove('active'));
                thumbnail.classList.add('active');
            });
        });
    }

    // Handle contact form submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }

    // Handle property form submission
    const propertyForm = document.getElementById('propertyForm');
    if (propertyForm) {
        propertyForm.addEventListener('submit', handlePropertySubmit);
    }
});

// Contact form submission handler
async function handleContactSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        phone: formData.get('phone'),
        message: formData.get('message')
    };

    try {
        // In a real application, this would be an API call
        await submitContactForm(data);
        showAlert('Message sent successfully!', 'success');
        e.target.reset();
    } catch (error) {
        showAlert('Error sending message. Please try again.', 'danger');
    }
}

// Property form submission handler
async function handlePropertySubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        title: formData.get('title'),
        type: formData.get('type'),
        price: formData.get('price'),
        location: formData.get('location'),
        bedrooms: formData.get('bedrooms'),
        bathrooms: formData.get('bathrooms'),
        area: formData.get('area'),
        description: formData.get('description'),
        property_type: formData.get('property_type')
    };

    try {
        // In a real application, this would be an API call
        await submitPropertyForm(data);
        showAlert('Property added successfully!', 'success');
        e.target.reset();
    } catch (error) {
        showAlert('Error adding property. Please try again.', 'danger');
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Mock API calls (replace with actual API calls)
async function submitContactForm(data) {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log('Contact form submitted:', data);
            resolve();
        }, 1000);
    });
}

async function submitPropertyForm(data) {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log('Property form submitted:', data);
            resolve();
        }, 1000);
    });
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Utility function to format date
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Utility function to handle image upload
function handleImageUpload(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
} 