
document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("mobileMenuBtn");
    const closeBtn = document.getElementById("sidebarCloseBtn");
    const sidebar = document.getElementById("appSidebar");
    const overlay = document.getElementById("sidebarOverlay");

    console.log("Sidebar JavaScript loaded");

    if (!menuBtn || !closeBtn || !sidebar || !overlay) {
        console.error("Sidebar elements are missing!");
        return;
    }

    function openSidebar() {
        sidebar.classList.add("active");
        overlay.classList.add("active");
        document.body.classList.add("sidebar-open");

        menuBtn.setAttribute("aria-expanded", "true");

        console.log("Sidebar opened");
    }

    function closeSidebar() {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
        document.body.classList.remove("sidebar-open");

        menuBtn.setAttribute("aria-expanded", "false");
    }

    menuBtn.addEventListener("click", openSidebar);
    closeBtn.addEventListener("click", closeSidebar);
    overlay.addEventListener("click", closeSidebar);

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeSidebar();
        }
    });

    sidebar.querySelectorAll(".nav-link").forEach(function (link) {
        link.addEventListener("click", closeSidebar);
    });

});
