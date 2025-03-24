document.addEventListener('DOMContentLoaded', () => {
    // Check if user is already logged in (only on login page)
    if (window.location.pathname === '/' && localStorage.getItem('user')) {
        window.location.href = '/dashboard';
        return;
    }

    // Helper function to handle form submissions
    const handleFormSubmit = async (formId, endpoint, successMessage, redirect = false) => {
        const form = document.getElementById(formId);
        if (!form) return; // Skip if form doesn't exist on this page

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const usernameInput = form.querySelector('input[type="text"]');
            const passwordInput = form.querySelector('input[type="password"]');
            const submitBtn = form.querySelector('.btn-primary');

            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();

            // Basic validation
            if (!username || !password) {
                showError('Please fill in all fields', form);
                return;
            }

            // Disable button during request
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';

            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    if (redirect) {
                        localStorage.setItem('user', JSON.stringify(data.user));
                        window.location.href = '/dashboard';
                    } else {
                        showSuccess(successMessage, form);
                        form.reset();
                    }
                } else {
                    showError(data.error || 'Something went wrong', form);
                }
            } catch (error) {
                console.error(`Error during ${endpoint}:`, error);
                showError('Request failed. Check your connection.', form);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = endpoint === '/login' ? 'Login' : 'Register';
            }
        });
    };

    // Helper function to show error message
    const showError = (message, form) => {
        let errorDiv = form.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            form.insertBefore(errorDiv, form.firstChild);
        }
        errorDiv.textContent = message;
        errorDiv.style.color = '#ff6b6b'; // Matches --danger-color
        errorDiv.style.marginBottom = '1rem';
        setTimeout(() => errorDiv.remove(), 3000); // Auto-hide after 3s
    };

    // Helper function to show success message
    const showSuccess = (message, form) => {
        let successDiv = form.querySelector('.success-message');
        if (!successDiv) {
            successDiv = document.createElement('div');
            successDiv.className = 'success-message';
            form.insertBefore(successDiv, form.firstChild);
        }
        successDiv.textContent = message;
        successDiv.style.color = '#40c057'; // Matches --secondary-color
        successDiv.style.marginBottom = '1rem';
        setTimeout(() => successDiv.remove(), 3000); // Auto-hide after 3s
    };

    // Initialize form handlers based on page
    handleFormSubmit('login-form', '/login', 'Login successful', true);
    handleFormSubmit('register-form', '/register', 'Registration successful! You can now log in.');
});