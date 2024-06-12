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