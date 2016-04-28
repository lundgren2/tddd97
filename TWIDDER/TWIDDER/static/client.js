/**
 * Created by tobiaslundgren on 2016-01-20.
 */
var connection;

Handlebars.registerHelper('if_eq', function(a, b, opts) {
    if(a == b) // Or === depending on your needs
        return opts.fn(this);
    else
        return opts.inverse(this);
});

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
}

function connectSocket(email) {
    console.log("connectSocketEmail 1");
    connection = new WebSocket('ws://localhost:5000/api');
    console.log("connection: " + connection);
    // Event handler
    connection.onopen = function () {
        console.log("connectSocketEmail 3");
        emailjson = JSON.stringify({ email: email });
// TODO: caught
      connection.send(email); // Send the message 'Ping' to the server
    };
    // Log errors
    connection.onerror = function (error) {
        console.log("connectSocketEmail error");
        console.log('WebSocket Error ' + error);
    };

    // Receive messages from the server
    connection.onmessage = function (message) {
        console.log("connectSocketEmail Message");
        console.log('Server: ' + message.data);

        if (message.data == "signout") {
            console.log("SIGNOUTSESSIONLOGISANDAJD");
            logoutUser();
        }
    };

    connection.onclose = function () {
        console.log("Socket closed")
    }

}


var HttpRequest = function (method, path, data, callback) {
    console.info("HttpRequest");
    var xml = new XMLHttpRequest();
    console.info("PATH i HTTPRequest: " + path);

    xml.onreadystatechange = function () {
        if (xml.readyState==4 && xml.status==200) {
            var serverResponse = JSON.parse(xml.responseText);
            if (serverResponse) {
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


// SERVER SIDE LOGIN
function login(formInput) {
    var data = "email=" + formInput.email.value + "&password=" + formInput.password.value;
    console.info(data);
    HttpRequest("POST", "/signin", data, function (result) {
        connectSocket(formInput.email.value);
        if (result.data) {
            console.log("i login email value: " + formInput.email.value);

            localStorage.setItem("userToken", result.data);
            localStorage.setItem("email", formInput.email.value);
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
    });

    login(formInput);

}
//SERVER SIDE LOGOUT
function logoutUser() {
    var logindata =  "token=" + get_token();
    console.info(logindata);
    HttpRequest("POST", "/signout", logindata, function (res){
        if (res.success) {
            localStorage.removeItem('userToken');
            localStorage.removeItem('email');
        }
        else {
            console.info("ELSE");
        }
        displayView();
        tabs("home");
    });
}
// GET LOCAL TOKEN
function get_token() {
    var token = localStorage.getItem('userToken');
    //return JSON.parse(token);
    return token;
}


function renderData(usrData, tab) {
    var context = {
    usrfirstname: usrData[1],
    usrfamname: usrData[2],
    usrgender: usrData[3],
    usrcity: usrData[4],
    usrcountry: usrData[5],
    usremail: usrData[0],
    tabs: tab
    };

    var source = document.getElementById("profileInformation").innerHTML;
    var template = Handlebars.compile(source);
    if (context.tabs == "profile") {
        document.getElementById("personalinformation").innerHTML = template(context);
    } else {
        document.getElementById("browseinformation").innerHTML = template(context);
    }

}

// SERVER SIDE
function getUserDataByToken() {
    var data = "token=" + get_token();

    HttpRequest("POST", "/getuserdatabytoken", data, function (result) {
        if (result.data) {
            console.log(result.data);
            renderData(result.data, "profile");
            console.log("BARA I HOME!");
            get_messages();
        }
    });
}


function getUserDataByEmail(email) {
    var data = "token=" + get_token() + "&email=" + email;

    HttpRequest("POST", "/getuserdatabyemail", data, function (result) {
        if (result.data) {
            console.info(result.data);
            renderData(result.data, "browse");
            console.log("BARA I BROWSE!");
            get_messages(email);
        }
    });

    return false;
}

function browseUserInfo(email) {
    tabs("browse");

    var token = localStorage.getItem("userToken");
    console.log("Browsed user loaded.");


    getUserDataByEmail(email.value);
    document.getElementById("browseinfo").className = "show";
    //get_messages(email.value);

    return false;
}


function tabs(tab) {
    var element1 = document.getElementById("home");
    var element2 = document.getElementById("browse");
    var element3 = document.getElementById("account");

    if (tab == "home" || tab == "browse" || tab == "account") {
        element1.classList.remove("selected");
        element2.classList.remove("selected");
        element3.classList.remove("selected");
    }

    if (tab != "browse" && tab != "account") {
        document.getElementById("tabview").innerHTML = document.getElementById("hometab").innerHTML;
        element1.classList.add("selected");
        getUserDataByToken();
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

function updateWall() {
    var email = document.getElementById("usremail").innerHTML;
    get_messages(email);
}

function get_messages(email) {
    var messContent;
    document.getElementById("userwall").innerHTML = "";
    if (email == null) {
        var data = "token=" + get_token();
        HttpRequest("POST", "/getusermessagebytoken", data, function (result) {
            if (result.success) {
                for (var i = 0; i < result.data.length; ++i) {
                    messContent = "<div class=\"message\">" + result.data[i][1] + ": " + result.data[i][3] + "</div><br>";
                    document.getElementById("userwall").innerHTML += messContent;
                }
            }

        });
    } else {
        var data = "token=" + get_token() + "&email=" + email;
        HttpRequest("POST", "/getusermessagebyemail", data, function (result) {
            if (result.success) {
                for (var i = 0; i < result.data.length; ++i) {
                    messContent = "<div class=\"message\">" + result.data[i][1] + ": " + result.data[i][3] + "</div><br>";
                    document.getElementById("userwall").innerHTML += messContent;
                }
            }
        });
    }

    return false; //ta ej bort
}

function postMessage(token, message, email) {
    var data = "token=" + token + "&message=" + message + "&email=" + email;
    HttpRequest("POST", "/postmessage", data, function (result) {
        console.log(result.message);
    })
}

function post_message(formInput) {
    var message = formInput.textbox.value;
    var email = document.getElementById("usremail").innerHTML;
    console.log("POSTAT TILL: ", message);
    postMessage(get_token(), message, email);
    console.log("POSTAR MAIL", get_token(), email);
    document.getElementById('textbox').value = "";
    get_messages(email);
    return false;
}

// SERVERSIDE
function changePassword(token, oldpw, newpw) {
    var data = "token=" + token + "&old_password=" + oldpw + "&new_password=" + newpw;
        HttpRequest("POST", "/changepass", data, function (result) {
           document.getElementById("info").innerHTML = result.message;
        });
}

function changePass(formInput){
    changePassword(get_token(), formInput.oldPassword.value, formInput.newPassword.value);
    tabs("account");
    return false;
}