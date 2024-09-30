const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const errorMessage = document.getElementById('error');
const successMessage = document.getElementById('success');
const registrationButton = document.getElementById('registerButton');

// Listen for input event on the confirm password field
confirmPasswordInput.addEventListener('input', function() {
    if (passwordInput.value === confirmPasswordInput.value) {
        errorMessage.style.display = 'none';
        successMessage.style.display = 'block';
        registrationButton.style.display = 'block'
    } else {
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
        registrationButton.style.display = 'none'
    }
});