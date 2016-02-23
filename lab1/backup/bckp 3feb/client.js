/**
 * Created by tobiaslundgren on 2016-01-20.
 */

displayView = function() {
    if(!localStorage.userToken) {

        document.getElementById("mainview").innerHTML = document.getElementById("welcomeview").innerHTML;

    } else {

        document.getElementById("mainview").innerHTML = document.getElementById("profileview").innerHTML;
        tabs();
    }
};

window.onload = function() {
    // code that is exexuted as the page is loaded.
    // you shall put your own custom code here.
    displayView();
    //window.alert("Hello TDDD97!");
};

function passwordLength() {
    //var password = ;
    if(document.getElementById("password").value.length < 5) {
        document.getElementById("password").setCustomValidity("Password too short!");
        return false;
} else {
        //document.getElementById("password").setCustomValidity("");
        return true;
    }
}
function validatePassword() {
    var password, confirm_password;
    password = document.getElementById("password").value;
    confirm_password = document.getElementById("confirm_password").value;

    if(password != confirm_password) {
    document.getElementById("confirm_password").setCustomValidity("Passwords Don't Match");
               console.info("false pass");
        return false;
  } else {
    //confirm_password.setCustomValidity("");
                console.info("truepass");
 //document.getElementById("confirm_password").setCustomValidity("");
        return false;
    }
    password.onchange = passwordLength;
    password.onchange = validatePassword;
    confirm_password.onkeyup = validatePassword;
}

function loginConverter(formInput) {
    console.info("loggar in...");
    token = serverstub.signIn(formInput.email.value, formInput.password.value);
    localStorage.setItem('userToken', JSON.stringify(token.data));
    var retrievedObject = localStorage.getItem('userToken');
    console.log('retrievedObject: ', JSON.parse(retrievedObject));
    displayView();
    tabs("home");


}
function logoutUser() {
    serverstub.signOut(get_token());
    localStorage.removeItem('userToken');
    displayView();

}

function signupConverter(formInput) {
  if(true) {
        var formData = {
            "email": formInput.email.value,
            "password": formInput.password.value,
            "firstname": formInput.firstname.value,
            "familyname": formInput.lastname.value,
            "gender": formInput.gender.value,
            "city": formInput.city.value,
            "country": formInput.country.value
        };
        var resp = serverstub.signUp(formData);
         if(resp.success === true) {
            var resplog = loginConverter(formInput);
            console.log(resplog);
        }

    return true;
    } else {
      alert("Invalid password");
      return false;
 }

}

function get_token() {
    var token = localStorage.getItem('userToken');
    return JSON.parse(token);
}
function hej() {
    var token = get_token();
    return serverstub.getUserDataByToken(token);
    //alert(token.message);
}

function getUserInfo(email) {
    if (email == null) {
    email = serverstub.getUserDataByToken(get_token()).data.email;
    }

    var token = localStorage.getItem("userToken");
    console.log(token, email);
    var usrData = serverstub.getUserDataByEmail(get_token(), email).data;

    document.getElementById("usrfirstname").innerHTML = usrData.firstname;
    document.getElementById("usrfamname").innerHTML = usrData.familyname;
    document.getElementById("usrgender").innerHTML = usrData.gender;
    document.getElementById("usrcity").innerHTML = usrData.city;
    document.getElementById("usrcountry").innerHTML = usrData.country;
    document.getElementById("usremail").innerHTML = usrData.email;

}

function tabs(tab) {
    var element1 = document.getElementById("home");
    var element2 = document.getElementById("browse");
    var element3 = document.getElementById("account");
    element1.classList.remove("selected");
    element2.classList.remove("selected");
    element3.classList.remove("selected");

    if (tab != "browse" && tab != "account") {
        document.getElementById("tabview").innerHTML = document.getElementById("hometab").innerHTML;
        element1.classList.add("selected");
    }
    if (tab == "browse") {
        document.getElementById("tabview").innerHTML = document.getElementById("browsetab").innerHTML;
        element2.classList.add("selected");
    }
    if (tab == "account") {
        document.getElementById("tabview").innerHTML = document.getElementById("accounttab").innerHTML;
        element3.classList.add("selected");
    }
   getUserInfo();
}