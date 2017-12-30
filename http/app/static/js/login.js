$(function () {
    'use strict';

    //if (getCookie('user') !== "") {
    //    window.location = "/";
    //}

    $("#login").submit(function (ev) {
        ev.preventDefault();

        let form = ev.target;

        let username = form[0].value;
        let password = form[1].value;

        let request = $.ajax({
            url: "/api/v1/login",
            method: "POST",
            data: {
                "username": username,
                "password": password
            },
        });

        request.done(function(response) {
            console.log(response);
        });

    });
});

