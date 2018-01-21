$(function () {
    'use strict';

    if (getCookie('user') !== "") {
        window.location = "/";
    }

    $("#login").submit(function (ev) {
        $("#errorBox").css("display", "none");
        ev.preventDefault();

        let form = ev.target;

        let username = form[0].value;
        let password = form[1].value;

        let request = $.ajax({
            url: "/api/v1/auth/login",
            method: "POST", 
            data: {
                "user": username,
                "password": password
            },
            
            beforeSend: function (r) {
                r.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
            }
        });

        request.done(function(response) {
            window.location = "/";
        });

        request.fail(function(response) {
            $("#errorBox").css("display", "block");
            console.error(response);
        });
    });
});

