// import css from '../css/Simple-Slider.css';
const slider = require('./slider.js');
const sel = require('./selector.js');

$(function() {
    document.getElementsByName('mark-dropdown').forEach((v, k, p) => {
        v.onmousemove = () => { sel.changeMark(true, this); };
    })
});