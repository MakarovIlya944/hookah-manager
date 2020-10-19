import css from '../css/Simple-Slider.css';
require('./slider.js');
require('./selector.js');

document.getElementById('mass').onchange(changeMass('mass'));
document.getElementById('mass-range').onchange(changeMass('mass-range'));
document.getElementById('mass-range').onmousemove(changeMass('mass-range'));