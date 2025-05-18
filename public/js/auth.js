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