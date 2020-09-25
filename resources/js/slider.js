export function initSliders() {
    new Swiper('.swiper-container', {
        loop: true,
        pagination: '.swiper-pagination',
        paginationClickable: true,
        slidesPerView: 1,
        spaceBetween: 30,
        height: 100,
        direction: "vertical"
    });
}