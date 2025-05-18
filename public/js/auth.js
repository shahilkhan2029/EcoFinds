// Authentication and User Management
class Auth {
    constructor() {
        this.currentUser = null;
        this.init();
    }

    init() {
        // Check for existing session
        this.checkSession();
        // Add event listeners
        this.addEventListeners();
    }

    checkSession() {
        const user = localStorage.getItem('user');
        if (user) {
            this.currentUser = JSON.parse(user);
            this.updateUI();
        }
    }

    addEventListeners() {
        // Login form submission
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        // Signup form submission
        const signupForm = document.getElementById('signupForm');
        if (signupForm) {
            signupForm.addEventListener('submit', (e) => this.handleSignup(e));
        }

        // Logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => this.handleLogout(e));
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            // In a real application, this would be an API call
            // For now, we'll simulate authentication
            const user = await this.authenticateUser(email, password);
            if (user) {
                this.setSession(user);
                window.location.href = 'index.html';
            } else {
                this.showError('Invalid email or password');
            }
        } catch (error) {
            this.showError('An error occurred during login');
        }
    }

    async handleSignup(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            this.showError('Passwords do not match');
            return;
        }

        try {
            // In a real application, this would be an API call
            const user = await this.registerUser(email, password);
            if (user) {
                this.setSession(user);
                window.location.href = 'index.html';
            }
        } catch (error) {
            this.showError('An error occurred during signup');
        }
    }

    handleLogout(e) {
        e.preventDefault();
        this.clearSession();
        window.location.href = 'index.html';
    }

    setSession(user) {
        this.currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));
        this.updateUI();
    }

    clearSession() {
        this.currentUser = null;
        localStorage.removeItem('user');
        this.updateUI();
    }

    updateUI() {
        const authButtons = document.getElementById('authButtons');
        const userMenu = document.getElementById('userMenu');
        const userName = document.getElementById('userName');

        if (this.currentUser) {
            if (authButtons) authButtons.classList.add('d-none');
            if (userMenu) {
                userMenu.classList.remove('d-none');
                if (userName) userName.textContent = this.currentUser.email;
            }
        } else {
            if (authButtons) authButtons.classList.remove('d-none');
            if (userMenu) userMenu.classList.add('d-none');
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.remove('d-none');
        }
    }

    // Simulated authentication (replace with actual API calls)
    async authenticateUser(email, password) {
        // This is a mock implementation
        // In a real application, this would make an API call to your backend
        return new Promise((resolve) => {
            setTimeout(() => {
                if (email === 'test@example.com' && password === 'Test@123') {
                    resolve({
                        id: 1,
                        email: email,
                        role: 'user'
                    });
                } else {
                    resolve(null);
                }
            }, 1000);
        });
    }

    // Simulated registration (replace with actual API calls)
    async registerUser(email, password) {
        // This is a mock implementation
        // In a real application, this would make an API call to your backend
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    id: Date.now(),
                    email: email,
                    role: 'user'
                });
            }, 1000);
        });
    }
}

// Initialize authentication
const auth = new Auth();

// Function to check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('currentUser') !== null;
}

// Function to get current user
function getCurrentUser() {
    const user = localStorage.getItem('currentUser');
    return user ? JSON.parse(user) : null;
}

// Function to update navbar based on auth state
function updateNavbar() {
    const authButtons = document.getElementById('authButtons');
    if (!authButtons) return;

    if (isLoggedIn()) {
        const user = getCurrentUser();
        authButtons.innerHTML = `
            <div class="user-menu">
                <span class="user-name">Welcome, ${user.name}</span>
                <button onclick="logout()" class="logout-btn">Logout</button>
            </div>
        `;
    } else {
        authButtons.innerHTML = `
            <a href="/pages/auth/login.html" class="login-btn">Login</a>
            <a href="/pages/auth/signup.html" class="signup-btn">Sign Up</a>
        `;
    }
}

// Function to handle logout
function logout() {
    localStorage.removeItem('currentUser');
    updateNavbar();
    window.location.href = '/';
}

// Function to handle signup
function handleSignup(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const errorMessage = document.getElementById('errorMessage');

    // Validate passwords match
    if (password !== confirmPassword) {
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'Passwords do not match';
        return;
    }

    // Get existing users
    const users = JSON.parse(localStorage.getItem('users')) || [];
    
    // Check if email already exists
    if (users.some(user => user.email === email)) {
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'Email already registered';
        return;
    }

    // Create new user
    const newUser = {
        id: Date.now(),
        name,
        email,
        password,
        createdAt: new Date().toISOString()
    };

    // Add to users array
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));

    // Show success message
    alert('Registration successful! Please login to continue.');
    
    // Redirect to login page
    window.location.href = 'login.html';
}

// Function to handle login
function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    // Get users from localStorage
    const users = JSON.parse(localStorage.getItem('users')) || [];
    
    // Find user
    const user = users.find(u => u.email === email && u.password === password);

    if (user) {
        // Store logged in user
        localStorage.setItem('currentUser', JSON.stringify(user));
        
        // Show success message
        alert('Login successful!');
        
        // Redirect to home page
        window.location.href = '/';
    } else {
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'Invalid email or password';
    }
}

// Update navbar when page loads
document.addEventListener('DOMContentLoaded', function() {
    updateNavbar();

    // Add event listeners for forms if they exist
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
}); 