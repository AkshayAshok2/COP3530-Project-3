'use strict';

const switcher = document.querySelector('.btn');
const search1 = document.querySelector('.bpdp');
const search2 = document.querySelector('.filter');
const backBut = document.querySelector('.bck');

const in1 = document.querySelector('.input1');
const in2 = document.querySelector('.input2');

switcher.addEventListener('click', function() {
    const className = document.body.className;
    if(className == "light-theme") {
        this.textContent = "Enter";
    } else {
        this.textContent = "Back";
    }
    console.log('current class name: ' + className);

    //if enter button is clicked, store the information.
    var charInput = document.getElementsByName('characters')[0].value;
    var keyInput = document.getElementsByName('keywords')[0].value;
    //now move onto the next page
    location.href="result.html";
    //clear everything afterwards
    document.getElementsByName('characters')[0].value = "";
    document.getElementsByName('keywords')[0].value = "";
});

search1.addEventListener('click', function() {
    document.body.classList.toggle('light-theme');
    document.body.classList.toggle('dark-theme');

    const className = document.body.className;
    console.log('current class name: ' + className);
});
search2.addEventListener('click', function() {
    document.body.classList.toggle('light-theme');
    document.body.classList.toggle('dark-theme');

    const className = document.body.className;
    console.log('current class name: ' + className);
});

in1.addEventListener('click', function() {
    document.body.classList.toggle('light-theme');
    document.body.classList.toggle('dark-theme');

    const className = document.body.className;
    console.log('current class name: ' + className);
});
in2.addEventListener('click', function() {
    document.body.classList.toggle('light-theme');
    document.body.classList.toggle('dark-theme');

    const className = document.body.className;
    console.log('current class name: ' + className);
});

backBut.addEventListener('click', function() {
    const className = document.body.className;
    if(className == "light-theme") {
        this.textContent = "Enter";
    } else {
        this.textContent = "Back";
    }
    console.log('current class name: ' + className);
    location.href="index.html";
});