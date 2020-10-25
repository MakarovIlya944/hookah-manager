// import css from '../css/Simple-Slider.css';
const slider = require('./slider.js');
const sel = require('./selector.js');

$(function() {
    document.getElementById('mass').onchange = () => { sel.changeMass('mass'); };
    document.getElementById('mass-range').onchange = () => { sel.changeMass('mass-range'); };
    document.getElementById('mass-range').onmousemove = () => { sel.changeMass('mass-range'); };

    document.getElementsByName('mark-dropdown').forEach((v, k, p) => {
        v.onmousemove = () => { sel.changeMark(true, this); };
    })
});