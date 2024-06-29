function updateTheme(isDarkMode) {
    const toggleButton = document.querySelector("#dark-mode-toggle")
    if (isDarkMode) {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
        toggleButton.classList.remove('bi-moon-fill')
        toggleButton.classList.add('bi-brightness-high-fill')
    } else {
        document.documentElement.removeAttribute('data-bs-theme')
        toggleButton.classList.remove('bi-brightness-high-fill')
        toggleButton.classList.add('bi-moon-fill')
    }
}

function applyDarkTheme() {
    const userPreference = localStorage.getItem('dark-mode')
    const systemPreference = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches

    if (userPreference === 'enabled' || (!userPreference && systemPreference)) {
        updateTheme(true)
    } else {
        updateTheme(false)
    }
}

function toggleDarkMode() {
    const isDarkMode = document.documentElement.getAttribute('data-bs-theme') === 'dark'
    localStorage.setItem('dark-mode', isDarkMode ? 'disabled' : 'enabled')
    updateTheme(!isDarkMode)
}

// Aplicar o tema escuro quando a página é carregada
document.addEventListener('DOMContentLoaded', function() {
    applyDarkTheme();

    const toggleButton = document.querySelector("#dark-mode-toggle")
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleDarkMode)
    }
});

// Monitorar as alterações nas preferências de tema do usuário
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('dark-mode')) {
            applyDarkTheme();
        }
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