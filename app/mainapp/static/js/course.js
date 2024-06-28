
showTwoElementsWhat();
showFirstSlideCourseTalent();

const pc_mobileWidthMediaQuery = window.matchMedia('(max-width: 1300px)');
pc_mobileWidthMediaQuery.addEventListener('change', function (event) {
    showMissionPcWhat(event.matches)
});

function showTwoElementsWhat() {
    var slides = document.getElementsByClassName("pc__what__card");

    slides[0].style.display = "flex";
    slides[1].style.display = "flex";
}

function showFirstSlideCourseTalent() {
    var slide = document.querySelector(".pc__lesson__card");

    slide.style.display = "flex";
}

// ЗАПУСК СЛАЙДЕРОВ

function showMissionPcWhat(isMobileSize) {
    if (isMobileSize) {
        showSlidePcWhat(0, 1);
        showSlides("pc__teacher__card", "pc__teacher__dot", 0);
        showSlides("pc__how-card", "pc__how-card__dot", 0);
        showSlides("pc__lesson__card", "pc__lesson__dot", 0);
    } else {
        showSlidesAllpcWhat();
        showSlidesAllTeacher();
        // window.addEventListener('scroll', checkCardStudy);
    }
}

function showSlidePcWhat(a, b) {
    var i;
    var slides = document.getElementsByClassName("pc__what__card");
    var dots = document.getElementsByClassName("pc__what__dot");

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" pc__what__dot-active", "");
    }

    slides[a].style.display = "flex";
    slides[b].style.display = "flex";
    dots[a].className += " pc__what__dot-active";
    // dots[b].className += "pc__what__dot-active";
}

function showSlidesAllpcWhat() {
    var i;
    var slides = document.getElementsByClassName("pc__what__card");
    var dots = document.getElementsByClassName("pc__what__dot");

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "flex";
    }
}

function showSlidesAllTeacher() {
    var i;
    var slides = document.getElementsByClassName("pc__teacher__card");

    if (slides.length > 0) {
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "block";
        }        
    }
}

// РАБОТА СЛАЙДЕРА

function showSlides(slidesClassName, dotsClassName, n) {
    var i;
    var slides = document.getElementsByClassName(slidesClassName);
    var dots = document.getElementsByClassName(dotsClassName);
    console.log(dots)

    if (slides.length > 0) {

        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
            dots[i].className = dots[i].className.replace(` ${dotsClassName}-active`, "");
        }

        slides[n].style.display = "block";
        dots[n].className += ` ${dotsClassName}-active`;

    }
}

// ВСПЛЫТИЕ КАРТОЧЕК ОБУЧЕНИЯ

const cardsStudy = document.querySelectorAll('.pc__how-card');

const checkCardStudy = () => {
    const trigger = window.innerHeight * 0.77;
     for (const card of cardsStudy) {
        const topOfCard = card.getBoundingClientRect().top;
        if (topOfCard < trigger) {
            card.classList.add('pc__how-card-show');
        } else {
            card.classList.remove('pc__how-card-show');
        }
     }
}
window.addEventListener('scroll', checkCardStudy);
