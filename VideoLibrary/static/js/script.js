document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    
    // Check local storage for theme
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        themeToggle.innerText = "☀️ Light Mode";
    }

    themeToggle.addEventListener("click", function() {
        body.classList.toggle("dark-mode");
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            themeToggle.innerText = "☀️ Light Mode";
        } else {
            localStorage.setItem("theme", "light");
            themeToggle.innerText = "🌙 Dark Mode";
        }
    });
});
