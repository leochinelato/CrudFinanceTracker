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

const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector("#password");

togglePassword.addEventListener('click', () => {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);

    if (type == 'text') {
        togglePassword.classList.remove('bi-eye-slash');
        togglePassword.classList.add('bi-eye');
    } else {
        togglePassword.classList.remove('bi-eye');
        togglePassword.classList.add('bi-eye-slash');
    }

})