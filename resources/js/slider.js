$(function() {
    new Swiper(".swiper-container", {
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

    function onChangeSlide() {
        console.log('slide changed');
    }

    brandSwiper.on('slideChangeTransitionEnd', onChangeSlide);
    new Swiper(".swiper-container-taste", {
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