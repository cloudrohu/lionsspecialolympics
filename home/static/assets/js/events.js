const slider = document.getElementById("eventAuto");
const cards = slider.children.length;
let index = 0;

function runSlider() {
  const width = window.innerWidth;

  // DESKTOP >= 1024
  if (width >= 1024) {
    if (cards === 4) {
      slider.style.transform = "translateX(0)";
      return;
    }
    index = (index + 1) % Math.ceil(cards / 4);
    slider.style.transform = `translateX(-${index * 25}%)`;
    return;
  }

  // TABLET 768–1023
  if (width >= 768 && width < 1024) {
    if (cards <= 2) {
      slider.style.transform = "translateX(0)";
      return;
    }
    index = (index + 1) % Math.ceil(cards / 2);
    slider.style.transform = `translateX(-${index * 50}%)`;
    return;
  }

  // MOBILE < 768
  if (width < 768) {
    index = (index + 1) % cards;
    slider.style.transform = `translateX(-${index * 85}%)`;
  }
}

setInterval(runSlider, 2400);
const tabs = document.querySelectorAll(".tabBtn");
const groups = document.querySelectorAll(".events");

tabs.forEach(btn => {
  btn.addEventListener("click", () => {

    tabs.forEach(t => t.classList.remove("activeTab"));
    btn.classList.add("activeTab");

    const year = btn.getAttribute("data-year");

    groups.forEach(group => {
      if (group.getAttribute("data-year") === year) {
        group.classList.remove("hidden");
      } else {
        group.classList.add("hidden");
      }
    });

  });
});