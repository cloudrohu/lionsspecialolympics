const menuBtn = document.getElementById("menuBtn");
const closeBtn = document.getElementById("closeBtn");
const mobileMenu = document.getElementById("mobileMenu");
const overlay = document.getElementById("overlay");
const menuItems = document.querySelectorAll(".menu-item");

menuBtn.addEventListener("click", () => {
    mobileMenu.classList.add("open");
    overlay.classList.add("show");

    // Add stagger animation
    menuItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add("show");
        }, index * 100);
    });
});

closeBtn.addEventListener("click", closeMenu);
overlay.addEventListener("click", closeMenu);

function closeMenu() {
    mobileMenu.classList.remove("open");
    overlay.classList.remove("show");

    // Remove animation for next opening
    menuItems.forEach(item => item.classList.remove("show"));
}

const counters = document.querySelectorAll(".count");
let started = false;

function startCountAnimation() {
    counters.forEach(counter => {
        const target = +counter.getAttribute("data-target");
        let count = 0;
        const speed = target / 200; // smoother animation

        function update() {
            if (count < target) {
                count += speed;
                counter.innerText = Math.floor(count);
                requestAnimationFrame(update);
            } else {
                counter.innerText = target;
            }
        }
        update();
    });
}

function checkScroll() {
    const section = document.getElementById("impactSection");
    const position = section.getBoundingClientRect().top;

    if (position < window.innerHeight - 100 && !started) {
        startCountAnimation();
        started = true;
    }
}

window.addEventListener("scroll", checkScroll);


var swiper = new Swiper(".swiper", {
    loop: true,
    spaceBetween: 20,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
});
let track = document.getElementById("sliderTrack");
let dotsContainer = document.getElementById("dots");
let total = document.querySelectorAll(".project-card").length;

let index = 0;

// Create dots dynamically
for (let i = 0; i < total; i++) {
    let dot = document.createElement("div");
    dot.classList.add("dot");
    if (i === 0) dot.classList.add("active");
    dot.dataset.idx = i;
    dotsContainer.appendChild(dot);

    dot.onclick = () => {
        index = i;
        updateSlider();
    };
}
const newsData = {
    1: {
        title: "Fundraising For Digital Library",
        slug: "fundraising-digital-library",
        date: "24 Nov 2025 | 09:32 AM",
        content: "Complete details of the Digital Library fundraising news…"
    },
    2: {
        title: "Community Event Update",
        slug: "community-event",
        date: "23 Nov 2025 | 07:45 PM",
        content: "Full details about the community event update…"
    },
    3: {
        title: "Tech Seminar Highlights",
        slug: "tech-seminar",
        date: "22 Nov 2025 | 11:20 AM",
        content: "Detailed seminar highlights and announcements…"
    }
};

function openNewsPopup(id) {
    document.getElementById("popupTitle").innerText = newsData[id].title;
    document.getElementById("popupSlug").innerText = "Slug: " + newsData[id].slug;
    document.getElementById("popupDate").innerText = "Published: " + newsData[id].date;
    document.getElementById("popupContent").innerText = newsData[id].content;

    document.getElementById("newsPopup").style.display = "flex";
}

function closeNewsPopup() {
    document.getElementById("newsPopup").style.display = "none";
}

function closeNewsPopup() {
    document.getElementById("newsPopup").classList.add("hidden");
}
new Swiper(".swiper", {
    loop: true,
    spaceBetween: 20,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
});



// ESC key to close
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closePopupFunc();
});
ScrollReveal().reveal('.reveal', {
    distance: "40px",
    duration: 900,
    interval: 120,
    origin: "bottom"
});
new Swiper(".testimonialSlider", {
    loop: true,
    autoplay: {
        delay: 3000,
    },
    spaceBetween: 30,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
});

// POPUP ELEMENTS
const popup = document.getElementById("imagePopupGALLERY");
const popupImage = document.getElementById("popupImage");
const closePopupBtn = document.getElementById("closePopup");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");

// Get all gallery images
const galleryItems = document.querySelectorAll(".gallery-img");

// Create array of all image src
let galleryImages = [];
galleryItems.forEach(img => galleryImages.push(img.src));

let currentIndex = 0;


// -------------------- OPEN POPUP --------------------
function openPopup(src) {
    currentIndex = galleryImages.indexOf(src); // find clicked image index

    popup.classList.remove("hidden");
    popupImage.src = src;

    // Animation
    setTimeout(() => {
        popupImage.classList.remove("scale-95", "opacity-0");
        popupImage.classList.add("scale-100", "opacity-100");
    }, 50);
}


// -------------------- CLOSE POPUP --------------------
function closePopup() {
    popupImage.classList.add("scale-95", "opacity-0");
    popupImage.classList.remove("scale-100", "opacity-100");

    setTimeout(() => {
        popup.classList.add("hidden");
    }, 200);
}

closePopupBtn.addEventListener("click", closePopup);


// -------------------- NEXT IMAGE --------------------
nextBtn.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % galleryImages.length;
    popupImage.src = galleryImages[currentIndex];
});


// -------------------- PREVIOUS IMAGE --------------------
prevBtn.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
    popupImage.src = galleryImages[currentIndex];
});


// -------------------- CLOSE ON BACKDROP CLICK --------------------
popup.addEventListener("click", (e) => {
    if (e.target === popup) {
        closePopup();
    }
});

const tsTrack = document.getElementById("tsTrack");
const tsPrev = document.getElementById("tsPrev");
const tsNext = document.getElementById("tsNext");
const tsDots = document.getElementById("tsDots");

let slideIndex = 0;
const slides = document.querySelectorAll(".ts-slide");

// total groups
function getVisibleSlides() {
    if (window.innerWidth >= 1024) return 3;
    if (window.innerWidth >= 640) return 2;
    return 1;
}

function updateSlider() {
    const visible = getVisibleSlides();
    const totalGroups = Math.ceil(slides.length / visible);

    slideIndex = Math.max(0, Math.min(slideIndex, totalGroups - 1));

    const shift = slideIndex * (100 / visible);
    tsTrack.style.transform = `translateX(-${shift}%)`;

    updateDots(totalGroups);
}

function updateDots(totalGroups) {
    tsDots.innerHTML = "";
    for (let i = 0; i < totalGroups; i++) {
        const dot = document.createElement("div");
        dot.className = "w-3 h-3 rounded-full " +
            (i === slideIndex ? "bg-red-600" : "bg-gray-300 cursor-pointer");

        dot.addEventListener("click", () => {
            slideIndex = i;
            updateSlider();
        });

        tsDots.appendChild(dot);
    }
}

tsNext.addEventListener("click", () => {
    slideIndex++;
    updateSlider();
});

tsPrev.addEventListener("click", () => {
    slideIndex--;
    updateSlider();
});

// Auto Slide
setInterval(() => {
    slideIndex++;
    updateSlider();
}, 3500);

// Update on resize
window.addEventListener("resize", updateSlider);

updateSlider();

var slider = new Swiper(".swiper", {
  loop: true,
  centeredSlides: true,
  grabCursor: true,
  speed: 600,
  spaceBetween: 30,
  effect: "coverflow",

  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
    pauseOnMouseEnter: true, // hover par rukega
  },

  coverflowEffect: {
    rotate: 15,     // 3D rotate
    stretch: 0,
    depth: 150,
    modifier: 1,
    slideShadows: false,
    scale: 0.9,    // side slightly small
  },

  slidesPerView: 1,
  breakpoints: {
    768: { slidesPerView: 2 },
    1024: { slidesPerView: 3 },
  },

  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});
  var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 28,
    centeredSlides: true,
    loop: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
            spaceBetween: 20,
            centeredSlides: false,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 28,
            centeredSlides: true,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 32,
        },
    },
});
new Swiper(".swiper", {
  loop: true,
  speed: 500,
  spaceBetween: 30,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  slidesPerView: 1,
  breakpoints: {
    768: { slidesPerView: 2 },
    1024: { slidesPerView: 3 },
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  }
});

function openModal(id) {
document.getElementById(id).classList.remove("hidden");
document.getElementById(id).classList.add("flex");
}
function closeModal(id) {
document.getElementById(id).classList.add("hidden");
}