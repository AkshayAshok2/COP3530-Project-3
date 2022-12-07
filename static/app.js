'use strict';

const switcher = document.querySelector('.btn');
const searching = document.querySelector('.search');
const in1 = document.querySelector('.input1');
const in2 = document.querySelector('.input2');

var temp = "BPDP";

switcher.addEventListener('click', function() {
    const className = document.body.className;
    console.log('current class name: ' + className);

    //if enter button is clicked, store the information.
    document.write(temp);

    //now move onto the next page
    location.href = "../templates/result.html";

    //clear everything afterwards
    temp = "BPDP";
});

searching.addEventListener('click', function() {
    document.body.classList.toggle('bpdp-search');
    document.body.classList.toggle('filter-search');
    const className = document.body.className;
    if(className == "bpdp-search") {
        this.textContent = "BPDP Search";
        temp = "BPDP";
    } else {
        this.textContent = "Filter Search";
        temp = "Filter";
    }

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
