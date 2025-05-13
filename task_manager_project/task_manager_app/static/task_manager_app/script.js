document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded - initializing dropdowns");
    
    // Find all dropdown toggle elements
    const dropdownToggleList = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    
    // Create dropdown instances
    if (typeof bootstrap !== 'undefined') {
        console.log("Bootstrap found, initializing", dropdownToggleList.length, "dropdowns");
        dropdownToggleList.forEach(function(dropdownToggle) {
            new bootstrap.Dropdown(dropdownToggle);
        });
    } else {
        console.error("Bootstrap JavaScript is not loaded properly!");
    }
});