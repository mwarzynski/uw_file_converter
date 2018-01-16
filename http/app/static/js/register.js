$(function () {
    'use strict';

    if (getCookie('user') !== "") {
        window.location = "/";
    }

    $("#register").submit(function (ev) {
        ev.preventDefault();

        let form = ev.target;

        let username = form[0].value;
        let password = form[1].value;

        let request = $.ajax({
            url: "/api/v1/auth/register",
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
            console.error(response);
        });
    });
});

