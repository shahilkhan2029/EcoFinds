// Function to handle user logout
function logout() {
    // Clear any stored user data
    localStorage.removeItem('user');
    sessionStorage.removeItem('user');
    
    // Clear any cookies
    document.cookie.split(";").forEach(function(c) { 
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
    });
    
    // Redirect to login page
    window.location.href = '/login.html';
}

// Add click event listener to logout button if it exists
document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
}); 