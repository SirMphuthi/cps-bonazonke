document.addEventListener('DOMContentLoaded', function() {
    const landingPage = document.getElementById('landing-page-container');
    const loginModal = document.getElementById('loginModal');
    const dashboard = document.getElementById('dashboard-container');
    const showLoginBtn = document.getElementById('show-login-btn');
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const logoutBtn = document.getElementById('logoutBtn');

    showLoginBtn.addEventListener('click', function() {
        landingPage.style.display = 'none';
        loginModal.classList.remove('hidden');
    });

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = loginForm.username.value;
        const password = loginForm.password.value;
        if (username === 'operator1' && password === 'password123') {
            loginModal.classList.add('hidden');
            dashboard.classList.remove('hidden');
            loginError.textContent = '';
        } else {
            loginError.textContent = 'Invalid credentials.';
        }
    });

    // Optional: Logout button to return to landing page
    logoutBtn.addEventListener('click', function() {
        dashboard.classList.add('hidden');
        landingPage.style.display = '';
        loginForm.reset();
        loginError.textContent = '';
    });
});