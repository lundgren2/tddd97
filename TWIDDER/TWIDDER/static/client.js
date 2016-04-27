/**
 * Created by tobiaslundgren on 2016-01-20.
 */
var connection;


Handlebars.registerHelper('link', function(text, url) {
  text = Handlebars.Utils.escapeExpression(text);
  url  = Handlebars.Utils.escapeExpression(url);

  var result = '<a href="' + url + '">' + text + '</a>';

  return new Handlebars.SafeString(result);
});


displayView = function() {
    if(localStorage.userToken) {
        document.getElementById("mainview").innerHTML = document.getElementById("profileview").innerHTML;
        tabs();
    } else {

        document.getElementById("mainview").innerHTML = document.getElementById("welcomeview").innerHTML;
    }
};

window.onload = function() {
    // code that is exexuted as the page is loaded.
    // you shall put your own custom code here.
    displayView();
    //window.alert("Hello TDDD97!");
};

function rendertemplate() {
    var context = {
        usrfirstname: "usrData.firstname",
        usrfamname: "usrData.familyname",
        usrgender: "usrData.gender",
        usrcity: "usrData.city",
        usrcountry: "usrData.country",
        usremail: "usrData.email"
    };

    var source = document.getElementById("profileInformation").innerHTML;
    var template = Handlebars.compile(source);
    document.getElementById("personalinfo2").innerHTML = template(context);
}


function connectSocket(email) {
    connection = new WebSocket('ws://localhost:5000/api');
    console.log("connection: " + connection);
    // Event handler
    connection.onopen = function () {
        emailjson = JSON.stringify({ email: email });

      connection.send(emailjson); // Send the message 'Ping' to the server
    };
    // Log errors
    connection.onerror = function (error) {
        console.log('WebSocket Error ' + error);
    };

    // Receive messages from the server
    connection.onmessage = function (message) {
        var jsonmessage = JSON.parse(message.data);
        console.log('Server: ' + message.data);
        if (message.data == "signout") {
            signOut(get_token());
        }
    };

    connection.onclose = function () {
        console.log("Socket closed")
    }

}


var HttpRequest = function (method, path, data, callback) {
    console.info("HttpRequest");
    var xml = new XMLHttpRequest();
    console.info(path);

    xml.onreadystatechange = function () {
        if (xml.readyState==4 && xml.status==200) {
            var serverResponse = JSON.parse(xml.responseText);
            if (serverResponse.success) {
                callback(serverResponse);
            } else {
                console.info(serverResponse.message);
            }
        }
    };
    var url = "http://localhost:5000" + path;

    xml.open(method, url, true); //CHECK OM DYNAMISK WORKS
    if (method == "GET") {
        xml.send(null);
    } else if (method == "POST") {
        //window.alert(data);
        xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xml.send(data);
    }

};


function passwordLength() {
    var password = document.getElementById("password").value;
    if(password.length < 7) {
        document.getElementById("password").setCustomValidity("Password too short!");
        return false;
} else {
        document.getElementById("password").setCustomValidity("");
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
        console.info("truepass");
        document.getElementById("confirm_password").setCustomValidity("");
        return false;
    }
    password.onchange = passwordLength;
    password.onchange = validatePassword;
    confirm_password.onkeyup = validatePassword;
}

function loginConverter(formInput) {
    console.info("loggar in...");
    var retrievedObject = serverstub.signIn(formInput.email.value, formInput.password.value);

        if(retrievedObject.success === true){
            localStorage.setItem('userToken', JSON.stringify(retrievedObject.data));
            displayView();
            tabs("home");
			return true;
        }else{
            document.getElementById("loginfail").innerHTML = retrievedObject.message;
            return false;
        }

    console.log('retrievedObject: ', JSON.parse(retrievedObject));

}

// SERVER SIDE LOGIN
function login(formInput) {
    console.info("loginfunktion");
    var data = "email=" + formInput.email.value + "&password=" + formInput.password.value;
    console.info(data);

    HttpRequest("POST", "/signin", data, function (result) {
        if (result.data) {
            connectSocket(formInput.email.value);
            localStorage.setItem("userToken", result.data);
            //localStorage.setItem("email", formInput.email.data);
        }
        displayView();
        tabs("home");
    })
}

//SERVER SIDE SIGNUP
function signup(formInput) {
    var data = 
        "email=" + formInput.email.value +
        "&password=" + formInput.password.value +
        "&firstname=" + formInput.firstname.value +
        "&familyname=" + formInput.lastname.value +
        "&gender=" + formInput.gender.value +
        "&city=" + formInput.city.value +
        "&country=" + formInput.country.value;
        
    HttpRequest("POST", "/signup", data, function (result){
        //alert(result.message);
    })

    login(formInput);

}
//SERVER SIDE LOGOUT
function logoutUser() {
    var logindata =  "token=" + get_token();
    console.info(logindata);
    HttpRequest("POST", "/signout", logindata, function (res){
        if (res.success) {
            localStorage.removeItem('userToken');
        }
        else {
            console.info("ELSSE");
        }
        displayView();
        tabs("home");
    })

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
// GET LOCAL TOKEN
function get_token() {
    var token = localStorage.getItem('userToken');
    //return JSON.parse(token);
    return token;
}

// SERVER SIDE
function getUserDataByToken() {

    var data = "token=" + get_token();

    HttpRequest("POST", "/getuserdatabytoken", data, function (result) {
        if (result.data) {
            connectSocket(result.data.email);
            console.log(result.data);
            
        }
    })
}


function getUserDataByEmail(email) {
    
    var data = "token=" + get_token() + "&email=" + email;
    var qemail;

<<<<<<< HEAD
    HttpRequest("POST", "/getuserdatabytoken", "token=" + get_token() , function (result) {
        if (result.data) {
            connectSocket(result.data.email);
            qemail = result.data.email;

        }
    })

    HttpRequest("POST", "/getuserdatabyemail", data, function (result) {
        if (result.data) {
            connectSocket(qemail);
            console.log(result.data);
        }
    })
=======
    email = getUserDataByToken(get_token()).data.email;

    email = getUserDataByToken(get_token()).data.email;

    var token = localStorage.getItem("userToken");
    console.log("user info loaded.");
    var usrData = serverstub.getUserDataByEmail(get_token(), email).data;

    var context = {
        usrfirstname: usrData.firstname,
        usrfamname: usrData.familyname,
        usrgender: usrData.gender,
        usrcity: usrData.city,
        usrcountry: usrData.country,
        usremail: usrData.email
    };
    var html = template(context);

    document.getElementById("usrfirstname").innerHTML = usrData.firstname;
    document.getElementById("usrfamname").innerHTML = usrData.familyname;
    document.getElementById("usrgender").innerHTML = usrData.gender;
    document.getElementById("usrcity").innerHTML = usrData.city;
    document.getElementById("usrcountry").innerHTML = usrData.country;
    document.getElementById("usremail").innerHTML = usrData.email;
    get_messages();
    return false;
>>>>>>> master
}

function browseUserInfo(email) {
    tabs("browse");

    var token = localStorage.getItem("userToken");
    console.log(token);
    console.log(email.value);
    console.log("Browsed user loaded.");


    if(serverstub.getUserDataByEmail(get_token(), email.value).success === true) {
        var usrData = serverstub.getUserDataByEmail(get_token(), email.value).data;

        document.getElementById("usrfirstname").innerHTML = usrData.firstname;
        document.getElementById("usrfamname").innerHTML = usrData.familyname;
        document.getElementById("usrgender").innerHTML = usrData.gender;
        document.getElementById("usrcity").innerHTML = usrData.city;
        document.getElementById("usrcountry").innerHTML = usrData.country;
        document.getElementById("usremail").innerHTML = usrData.email;

        get_messages(email.value);
        document.getElementById("browseinfo").className = "show";
     }else {
    document.getElementById("error").innerHTML = "User doesn't exist. Please try again.";
     }

    return false;
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
        getUserInfo();
    }
    if (tab == "browse") {
        document.getElementById("tabview").innerHTML = document.getElementById("browsetab").innerHTML;
        element2.classList.add("selected");
    }
    if (tab == "account") {
        document.getElementById("tabview").innerHTML = document.getElementById("accounttab").innerHTML;
        element3.classList.add("selected");
    }
    return false;
}


function get_messages(email) {
    if (email == null) {
        var email = document.getElementById("usremail").innerHTML;
    }

    var token = get_token();
    var usrData = serverstub.getUserMessagesByEmail(get_token(), email).data;
    var dataLenght = usrData.length;
    var messContent;
    console.log(usrData);

document.getElementById("userwall").innerHTML = "";
    for (var i = 0; i < dataLenght; ++i) {

        messContent = "<div class=\"message\">" + usrData[i].writer + ": " + usrData[i].content + "</div><br>";
        document.getElementById("userwall").innerHTML += messContent;
    }
    return false;
}

function post_message(formInput) {
    var message = formInput.textbox.value;
    console.log("POSTAT TILL: ", message);

    //var email = serverstub.getUserDataByToken(get_token()).data.email;
    var email = document.getElementById("usremail").innerHTML;
    var token = get_token();
    console.log("POSTAR MAIL", token, email);

    var resp = serverstub.postMessage(token, message, email);
         if(resp.success === true) {
             console.log(resp);
             get_messages(email);
            document.getElementById('textbox').value = "";
         }
    return false;
}

function changePass(formInput){
    var retrievedObject = serverstub.changePassword(get_token(), formInput.oldPassword.value, formInput.newPassword.value)
    tabs("account");
     if(retrievedObject.success === true) {
         document.getElementById("info").innerHTML = "Password is successfully changed!.";
         info.classList.remove("failed");
     }else{
         info.classList.add("failed");
         document.getElementById("info").innerHTML = "Failed to change password.";


     }
    return false;
}