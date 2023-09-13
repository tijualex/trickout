(function () {
  "use strict";

  /*==================================================================
  [ Validate ]*/`
  var name = document.getElementById("full_name");
  var uname = document.getElementById("uname");
  var email = document.getElementById("email");
  var passwd = document.getElementById("pass");
  var cpasswd = document.getElementById("cpass");

  document.querySelector('.validate-form').addEventListener('submit', function (event) {
    var check = true;

    if (!validateName()) {
      showValidate(name);
      check = false;
    }

    if (!validateUname()) {
      showValidate(uname);
      check = false;
    }

    if (!validateEmail()) {
      showValidate(email);
      check = false;
    }
    if (!validatePwd()) {
      showValidate(passwd);
      check = false;
    }
    if (!validateCpwd()) {
      showValidate(cpasswd);
      check = false;
    }


    if (!check) {
      event.preventDefault(); // Prevent the form from submitting
    }
  });

  document.querySelectorAll('.validate-form .input100').forEach(function (element) {
    element.addEventListener('focus', function () {
      hideValidate(this);
    });
  });

  function validateName() {
    var letters = /^[A-Za-z ]*$/;
    // alert("Working")
    var fname = document.getElementById("t1").value;

    if ((!letters.test(fname) || fname.length <= 2) && fname.length > 0 || fname == "") {

      return false;
    } else {

      return true;
    }
  }

  function validateUname() {
    // alert("hello user")
    var letters = /^[A-Za-z ]*$/;
    var uname = document.getElementById("t2").value;
    if ((!letters.test(uname) || uname.length <= 2) && uname.length > 0 || uname == "") {

      return false;
    } else {

      return true;
    }
  }

  function validateEmail() {
    var email_exp = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var email = document.getElementById("t3").value;
    if (!email_exp.test(email) || !(email.length > 0) || email == "") {
      return false;
    } else {
      return true;
    }
  }

  function validatePwd() {
    var pwd_exp = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])/;
    var pwd = document.getElementById("t5").value;
    if (!pwd_exp.test(pwd) || (pwd.length <= 5) || (pwd.length > 12) || pwd == "") {
      return false;
    } else {
      return true;
    }
  }

  function validateCpwd() {
    var cpwd = document.getElementById("t6").value;
    var pwd = document.getElementById("t5").value;
    if (pwd !== cpwd || cpwd == "") {
      return false;
    } else {

      return true;
    }
  }

  function showValidate(input) {
    var thisAlert = input.parentNode;

    thisAlert.classList.add('alert-validate');
  }

  function hideValidate(input) {
    var thisAlert = input.parentNode;

    thisAlert.classList.remove('alert-validate');
  }

})();
