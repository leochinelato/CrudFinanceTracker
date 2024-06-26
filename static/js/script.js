function applyDarkTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-bs-theme');
    }
}

// Aplicar o tema escuro quando a página é carregada
document.addEventListener('DOMContentLoaded', function() {
    applyDarkTheme();
});

// Monitorar as alterações nas preferências de tema do usuário
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        applyDarkTheme();
    });
}

(function() {
    const togglePasswordButton = document.querySelector('#togglePassword');
    const passwordField = document.querySelector("#password");

    if (togglePasswordButton) {
        togglePasswordButton.addEventListener('click', () => {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);

            if (type == 'text') {
                togglePasswordButton.classList.remove('bi-eye-slash');
                togglePasswordButton.classList.add('bi-eye');
            } else {
                togglePasswordButton.classList.remove('bi-eye');
                togglePasswordButton.classList.add('bi-eye-slash');
            }
        });
    }
})();

document.getElementById('form2').onsubmit = function(event) {
    event.preventDefault()

    this.submit()
}