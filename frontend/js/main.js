// Entry JS file for AI Career Agent
console.log('Main JS loaded - Authentication bypassed for better UX');

// Simplified AuthManager that bypasses all authentication
class AuthManager {
    static async checkAuthentication() {
        // Always return authenticated for better UX
        return { 
            authenticated: true, 
            user: { 
                name: 'Demo User',
                username: 'demo',
                role: 'user'
            } 
        };
    }

    static async logout() {
        // Mock logout - no actual logout needed
        console.log('Logout bypassed for demo purposes');
        return { success: true };
    }

    static redirectToLogin() {
        // No redirect needed - authentication bypassed
        console.log('Login redirect bypassed for better UX');
    }

    static async requireAuth() {
        // Always return authenticated status
        return { 
            authenticated: true, 
            user: { 
                name: 'Demo User',
                username: 'demo',
                role: 'user'
            } 
        };
    }

    static addLogoutButton() {
        // No logout button needed when auth is bypassed
        console.log('Logout button not needed - authentication bypassed');
    }

    static async init() {
        // Always return authenticated status for better UX
        console.log('Authentication bypassed - user automatically authenticated as Demo User');
        return { 
            authenticated: true, 
            user: { 
                name: 'Demo User',
                username: 'demo',
                role: 'user'
            } 
        };
    }
}

// Initialize bypassed authentication on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Authentication system bypassed for better user experience');
    const authStatus = await AuthManager.init();
    console.log('User automatically authenticated:', authStatus.user.name);
});

// Make AuthManager globally available
window.AuthManager = AuthManager;
