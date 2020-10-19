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
        direction: "vertical",
        on: {
            init: function() {
                console.log('swiper initialized');
            },
        },
    });


    var s = brandSwiper.on;
    s('slideChange', () => {
        console.log('slide changed');
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
});