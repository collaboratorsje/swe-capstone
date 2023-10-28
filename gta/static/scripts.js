// static/scripts.js

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert:not(.static-alert)');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 1000); // Matches the duration of the fade effect
        });
    }, 5000); // Duration until the fade-out starts
});

