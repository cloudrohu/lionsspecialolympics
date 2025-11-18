document.addEventListener('DOMContentLoaded', function() {
  var track = document.getElementById('carousel-track');
  if (!track) return; // no slides

  var slides = track.children;
  var total = slides.length;
  var index = 0;
  var dots = document.querySelectorAll('#carousel-dots .dot');
  var prevBtn = document.getElementById('carousel-prev');
  var nextBtn = document.getElementById('carousel-next');
  var interval = 6000;
  var timer = null;

  function goTo(i) {
    index = (i + total) % total;
    track.style.transform = 'translateX(' + (-index * 100) + '%)';
    dots.forEach(function(d){ d.classList.remove('active'); });
    if (dots[index]) dots[index].classList.add('active');
  }

  function next() { goTo(index + 1); }
  function prev() { goTo(index - 1); }

  if (nextBtn) nextBtn.addEventListener('click', function(){ next(); resetTimer(); });
  if (prevBtn) prevBtn.addEventListener('click', function(){ prev(); resetTimer(); });

  dots.forEach(function(dot){
    dot.addEventListener('click', function(){ goTo(parseInt(this.dataset.index,10)); resetTimer(); });
  });

  function startTimer(){ timer = setInterval(next, interval); }
  function stopTimer(){ if (timer) clearInterval(timer); timer = null; }
  function resetTimer(){ stopTimer(); startTimer(); }

  // Pause on hover
  track.addEventListener('mouseenter', stopTimer);
  track.addEventListener('mouseleave', startTimer);

  // start
  goTo(0);
  startTimer();
});
