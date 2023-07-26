const menuToggles = document.querySelectorAll('.menu-toggle');

menuToggles.forEach(function(menuToggle) {
  menuToggle.addEventListener('click', function() {
    const submenu = this.nextElementSibling;
    submenu.classList.toggle('show');
  });
});