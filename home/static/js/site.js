document.addEventListener('DOMContentLoaded', function(){
  var menuBtn = document.getElementById('menu-toggle');
  var nav = document.querySelector('.main-nav');
  menuBtn && menuBtn.addEventListener('click', function(e){
    var expanded = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', (!expanded).toString());
    nav.classList.toggle('open');
  });

  // submenu toggles on mobile
  document.querySelectorAll('.main-nav .has-sub .sub-toggle').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      var li = btn.closest('li');
      var isOpen = li.classList.contains('open');
      li.classList.toggle('open', !isOpen);
      btn.setAttribute('aria-expanded', (!isOpen).toString());
    });
  });
});
