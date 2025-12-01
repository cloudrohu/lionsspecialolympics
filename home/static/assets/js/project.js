const slider = document.getElementById("testimonialSlider");
const nextBtn = document.getElementById("next");
const prevBtn = document.getElementById("prev");
const dotsContainer = document.getElementById("dots");

const cards = slider.children;
let index = 0;
const visible = {
  default: 1,
  768: 2,
  1024: 3
};

function getVisibleCards() {
  let width = window.innerWidth;
  if (width >= 1024) return visible[1024];
  if (width >= 768) return visible[768];
  return visible.default;
}

function updateCarousel() {
  slider.style.transform = `translateX(-${index * (100 / getVisibleCards())}%)`;
  updateDots();
}

function createDots() {
  dotsContainer.innerHTML = "";
  let totalDots = cards.length - getVisibleCards() + 1;
  for (let i = 0; i < totalDots; i++) {
    const dot = document.createElement("div");
    dot.className = "w-3 h-3 bg-gray-400 rounded-full cursor-pointer";
    dot.addEventListener("click", () => {
      index = i;
      updateCarousel();
    });
    dotsContainer.appendChild(dot);
  }
}

function updateDots() {
  [...dotsContainer.children].forEach((dot, i) => {
    dot.className =
      "w-3 h-3 rounded-full cursor-pointer " +
      (i === index ? "bg-gray-800" : "bg-gray-400");
  });
}

nextBtn.addEventListener("click", () => {
  index++;
  if (index > cards.length - getVisibleCards()) index = 0;
  updateCarousel();
});

prevBtn.addEventListener("click", () => {
  index--;
  if (index < 0) index = cards.length - getVisibleCards();
  updateCarousel();
});

// Auto Slide
setInterval(() => {
  index++;
  if (index > cards.length - getVisibleCards()) index = 0;
  updateCarousel();
}, 3000);

window.addEventListener("resize", () => {
  index = 0;
  createDots();
  updateCarousel();
});

createDots();
updateCarousel();