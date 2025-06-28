document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");

    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {

        event.preventDefault(); // Prevent the default form submission
        console.log("Form submitted!");
        alert("Logging in...");
    });
    
    const links = document.querySelectorAll("a");
    console.log("Links found:", links.length);

    links.forEach(link => {
        const href = link.getAttribute("href");

        if (!href || href.trim() === "") {
            // Add a visual hint
            link.style.color = "red";
            link.style.pointerEvents = "none"; // disables the link
            link.style.cursor = "not-allowed";

            // Show alert when clicked
            link.addEventListener("click", function (e) {
                e.preventDefault(); // stop default behavior
                alert("This link is broken or missing!");
            });
        }
    });

});
