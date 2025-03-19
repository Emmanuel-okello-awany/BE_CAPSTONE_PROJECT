// Show an alert when form is submitted
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    
    forms.forEach(form => {
        form.addEventListener("submit", function () {
            alert("Form submitted successfully!");
        });
    });
});
