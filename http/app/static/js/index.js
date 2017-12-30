function getFiles() {
    let files = Array();
    if (localStorage.files) {
        files = JSON.parse(localStorage.files);
    }
    return files;
}

function addFile(name, token) {
    let files = getFiles();
    files.push({
        'filename': name,
        'token': token,
        'converted': false
    })
    localStorage.files = JSON.stringify(files);
}

$(function () {
    'use strict';

    if (getCookie('user') === "") {
        window.location = "/login.html";
    }

    $("#fileupload").change((event) => {
        let input = event.target;

        if (input.files.length < 1) {
            return;
        }

        let reader = new FileReader();

        reader.onload = function() {
            let fileData = reader.result;
            let blob = new Blob(
                [ new Uint8Array(fileData)],
                { type: input.files[0].type }
            );

            let request = $.ajax({ 
                url: '/api/v1/upload',
                type: 'PUT',
                contentType: input.files[0].type,
                data: fileData,
                processData: false,
                
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-Filename', input.files[0].name);
                    xhr.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
                },

                // TODO: (chivay?) Progress Bar...
            });

            request.done(function(response) {
                if (response.status == "OK") {
                    addFile(response.name, response.token);
                    $('#files').append('<li>' + response.name + '</li>');
                } else {
                    console.error(response.status);
                }
            });

            request.fail(function(error) {
                // TODO: Nice error notification using Bootstrap CSS...
                console.error(error.statusText);
                alert("Something went wrong.");
            });
        }

        reader.readAsArrayBuffer(input.files[0]);
    });

    let files = getFiles();
    for (let i = 0; i < files.length; i++) {
        let file = files[i];

        let style = "";
        if (file.converted === true) {
            style = "list-group-item-success";
        }

        let action = "";
        if (file.converted === true) {
            action = 'onclick=\'alert(\"' + i + '\");\'';
        }

        $("#files").append('<li class="list-group-item ' + style + '" ' + action + '>' + file.filename + '</li>');
    }
});

