// var email = document.querySelector("firstname");
// var password = document.querySelector("firstname");
// var validEmail = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
// var containsDigit = /\d/;
// var containsCap = /[A-Z]/;
// // var valPassLen = document.sign_up.password.length;

// var invalid = [];
// console.log(password)
// if (password.contains.length === 0) {
//     invalid.push("Password cannot be blank");
// }

// if (password.contains.length < 8) {
//     invalid.push("Password must be at least 8 characters long");
// }

// if (!containsCap.test(password)) {
//     invalid.push("Password must have at least one capital letter");
// }

// if (containsDigit.test(password)) {
//     invalid.push("Password must have at least one numeric character (0-9)");
// }


// // return true;

// // $('.submit').click(function(){
// //   validateForm();
// //  });

// var element = document.getElementById("firstname");

// //If it isn't "undefined" and it isn't "null", then it exists.
// if (typeof(element) != 'undefined' && element != null) {
//     alert('Element exists!');
// } else {
//     alert('Element does not exist!');

// }
// if ( === 0) {
//     invalid.push("Password cannot be blank");
// }

function myFunction() {
    var x, text;

    // Get the value of the input field with id="numb"
    x = document.getElementById("firstname").value;

    // If x is Not a Number or less than one or greater than 10
    if (isNaN(x) || x < 1 || x > 10) {
        text = "* First name length be greater than 1 and less than 15";

    } else {
        text = "";
    }
    text = text + "\n" + "dfsdf"
    document.getElementById("demo").innerHTML = text;
}