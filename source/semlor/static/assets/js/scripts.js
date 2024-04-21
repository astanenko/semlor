$(document).ready(function() {
    const body = $('body');

    function toggleMode() {
        body.toggleClass('dark-mode');
        const isDarkMode = body.hasClass('dark-mode');
        localStorage.setItem('mode', isDarkMode ? 'dark' : 'light');
    }

    $('#toggleModeBtn').click(toggleMode);
    if (localStorage.getItem('mode') === 'dark') {
        body.addClass('dark-mode');
    }
});