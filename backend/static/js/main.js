// Entry JS file for AI Career Agent
console.log('Main JS loaded');

// Authentication utility functions
class AuthManager {
    static async checkAuthentication() {
        try {
            const response = await fetch('http://127.0.0.1:5002/auth-status');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Auth check failed:', error);
            return { authenticated: false };
        }
    }

    static async logout() {
        try {
            const response = await fetch('http://127.0.0.1:5001/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const data = await response.json();
            if (data.success) {
                window.location.href = 'http://127.0.0.1:5001/login';
            }
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }

    static redirectToLogin() {
        window.location.href = 'http://127.0.0.1:5001/login';
    }

    static async requireAuth() {
        // Authentication bypassed for better UX
        return { authenticated: true, user: { name: 'Demo User' } };
        
        /* Original code:
        const authStatus = await this.checkAuthentication();
        if (!authStatus.authenticated) {
            this.redirectToLogin();
            return false;
        }
        return authStatus;
        */
    }

    static addLogoutButton() {
        // Add logout button to navigation if it doesn't exist
        const nav = document.querySelector('nav') || document.querySelector('.navigation') || document.querySelector('header');
        if (nav && !document.getElementById('logoutButton')) {
            const logoutBtn = document.createElement('button');
            logoutBtn.id = 'logoutButton';
            logoutBtn.innerHTML = '🚪 Logout';
            logoutBtn.style.cssText = `
                background: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
                margin-left: 10px;
                font-size: 0.9rem;
            `;
            logoutBtn.onclick = () => AuthManager.logout();
            nav.appendChild(logoutBtn);
        }
    }

    static async init() {
        // Authentication disabled for better UX
        console.log('Authentication bypassed for development');
        return { authenticated: true, user: { name: 'Demo User' } };
        
        /* Original authentication code:
        // Check authentication on page load
        const authStatus = await this.checkAuthentication();
        if (authStatus.authenticated) {
            console.log('User authenticated:', authStatus.user);
            this.addLogoutButton();
            return authStatus;
        } else {
            // Only redirect if we're not already on the login page
            if (!window.location.pathname.includes('login')) {
                this.redirectToLogin();
            }
            return null;
        }
        */
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Authentication bypassed - just log success
    console.log('AI Career Agent loaded successfully - No authentication required');
});

// Make AuthManager globally available but with authentication disabled
window.AuthManager = {
    checkAuthentication: () => Promise.resolve({ authenticated: true, user: { name: 'Demo User' } }),
    requireAuth: () => Promise.resolve({ authenticated: true, user: { name: 'Demo User' } }),
    init: () => Promise.resolve({ authenticated: true, user: { name: 'Demo User' } }),
    redirectToLogin: () => console.log('Login redirect disabled'),
    logout: () => console.log('Logout disabled'),
    addLogoutButton: () => console.log('Logout button disabled')
};
