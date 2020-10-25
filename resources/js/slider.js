const sel = require('./selector.js');

$(function() {
    var mainSwiper = new Swiper(".swiper-container", {
        loop: !0,
        paginationClickable: !0,
        nextButton: ".swiper-button-next",
        prevButton: ".swiper-button-prev",
        speed: 600,
        mousewheel: true,
    });
    var brandSwiper = new Swiper(".swiper-container-brand", {
        loop: true,
        paginationClickable: true,
        speed: 600,
        mousewheel: true,
        wrapperClass: "swiper-wrapper-brand",
        slidesPerView: 1,
        spaceBetween: 30,
        height: 100,
        direction: "vertical"
    });

    var tasteSwiper = new Swiper(".swiper-container-taste", {
        loop: true,
        paginationClickable: true,
        speed: 600,
        mousewheel: true,
        wrapperClass: "swiper-wrapper-taste",
        slidesPerView: 1,
        spaceBetween: 30,
        height: 100,
        direction: "vertical"
    });
    var slides = {};
    for (let index = 0; index < tasteSwiper.slides.length; index++) {
        var c = tasteSwiper.slides[index].classList[1];
        if (c in slides)
            slides[c].push(tasteSwiper.slides[index]);
        else {
            slides[c] = [];
            slides[c].push(tasteSwiper.slides[index]);
        }
    }

    function changeBrand() {
        debugger
        var currentClass = brandSwiper.slides[brandSwiper.activeIndex].classList[1];
        tasteSwiper.removeAllSlides();
        for (let index = 0; index < slides[currentClass].length; index++) {
            tasteSwiper.appendSlide(slides[currentClass][index]);
        }
        tasteSwiper.update();
        mySwiper.slideTo(0, 1, false);
    }

    brandSwiper.on('transitionEnd', changeBrand);
});