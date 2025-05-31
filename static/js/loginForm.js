function showLogin() {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('forgotPasswordForm').classList.add('hidden');
}

function showRegister() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
    document.getElementById('forgotPasswordForm').classList.add('hidden');
}

function showForgotPassword() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('forgotPasswordForm').classList.remove('hidden');
}

// Password visibility toggle
function togglePassword(fieldId) {
    const passwordField = document.getElementById(fieldId);
    const toggleIcon = document.getElementById('toggleIcon_' + fieldId);

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Phone number formatting
document.getElementById('id_phone')?.addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.startsWith('380')) {
        value = value.slice(3);
    }

    let formatted = '+380';
    if (value.length >= 2) formatted += ' (' + value.slice(0, 2) + ')';
    if (value.length >= 5) formatted += ' ' + value.slice(2, 5);
    if (value.length >= 7) formatted += '-' + value.slice(5, 7);
    if (value.length >= 9) formatted += '-' + value.slice(7, 9);

    e.target.value = formatted;
});

// Password strength indicator
document.getElementById('id_password1')?.addEventListener('input', function (e) {
    const password = e.target.value;
    let strength = 0;

    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    // Remove existing strength indicator
    const existingIndicator = e.target.parentNode.querySelector('.password-strength');
    if (existingIndicator) {
        existingIndicator.remove();
    }

    if (password.length > 0) {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength mt-2 flex space-x-1';

        for (let i = 0; i < 5; i++) {
            const bar = document.createElement('div');
            bar.className = `h-1 rounded-full flex-1 ${i < strength ?
                (strength <= 2 ? 'bg-red-500' : strength <= 3 ? 'bg-yellow-500' : 'bg-green-500') :
                'bg-gray-600'}`;
            indicator.appendChild(bar);
        }

        e.target.parentNode.appendChild(indicator);
    }
});

// Form validation
document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let hasErrors = false;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('border-red-500');
                    hasErrors = true;
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            // Password confirmation check
            const password1 = form.querySelector('#id_password1');
            const password2 = form.querySelector('#id_password2');

            if (password1 && password2 && password1.value !== password2.value) {
                password2.classList.add('border-red-500');
                hasErrors = true;

                // Show error message
                let errorMsg = password2.parentNode.querySelector('.error-msg');
                if (!errorMsg) {
                    errorMsg = document.createElement('p');
                    errorMsg.className = 'error-msg text-red-400 text-sm mt-1';
                    errorMsg.textContent = 'Паролі не співпадають';
                    password2.parentNode.appendChild(errorMsg);
                }
            }

            if (hasErrors) {
                e.preventDefault();
            }
        });
    });
});