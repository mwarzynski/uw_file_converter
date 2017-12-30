function getUploadedFiles() {
    let files = Array();
    if (localStorage.files) {
        f = JSON.parse(localStorage.files);
        if (f !== null) {
            files = f;
        }
    }
    return files;
}

function addUploadedFile(name, token) {
    let files = getUploadedFiles();
    files.push({
        'filename': name,
        'token': token,
    })
    localStorage.files = JSON.stringify(files);
}

function getConvertedFiles() {
    let files = Array();
    if (localStorage.converted_files) {
        f = JSON.parse(localStorage.converted_files);
        if (f !== null) {
            files = f;
        }
    }
    return files;
}

function addConvertedFile(file) {
    let files = getConvertedFiles();
    files.push(file)
    localStorage.converted_files = JSON.stringify(files);
}

function fetchUploadedFiles() {
    let request = $.ajax({
        url: "/api/v1/files",
    });

    request.done(function(data) {
        let files = data['files'];
        localStorage.files = null;
        for (let i = 0; i < files.length; i++) {
            addUploadedFile(files[i].name, files[i].token);
        }
    });
}

function fetchConvertedFiles() {
    let request = $.ajax({
        url: "/api/v1/files",
        data: {
            'converted': 1,
        },
    });

    request.done(function(data) {
        let files = data['files'];
        localStorage.converted_files = null;
        for (let i = 0; i < files.length; i++) {
            addConvertedFile({
                'filename': files[i].name,
                'token': files[i].token,
                'type': files[i].type,
                'status': files[i].status
            });
        }
    });
}

function showUploadedFile(filename, token) {
	let actionButton = '<button class="btn btn-primary" onclick="convertFile(\'' + token + '\', \'m4a\', \'mp3\')">Convert</button>';
	$("#files").append('<tr>' + '<th scope="row">' + filename + '</th><td>' + actionButton + '</td></tr>');
}

function showUploadedFiles() {
    let files = getUploadedFiles();
    for (let i = 0; i < files.length; i++) {
        let file = files[i];
        showUploadedFile(file.filename, file.token);
    }
}

function showConvertedFile(filename, token, type) {
	let actionButton = '<button class="btn btn-success" onclick="downloadFile(\'' + token + '\')">Download</button>';
	$("#converted-files").append('<tr>' + '<td scope="row">' + filename + '</td><td>' + type + '</td><td>' + actionButton + '</td></tr>');
}

function showConvertedFiles() {
    let files = getConvertedFiles();
    for (let i = 0; i < files.length; i++) {
        let file = files[i];
        showConvertedFile(file.filename, file.token, file.type);
    }
}

function convertFile(token, convert_from, convert_to) {
	let request = $.ajax({
		url: "/api/v1/files/convert",
		type: "POST",
		data: JSON.stringify({
			'token': token,
			'convert_from': convert_from,
			'convert_to': convert_to
		}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",

		beforeSend: function (r) {
			r.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
		},
	});

	request.fail(function(error) {
		console.error(error);
	});
}

function downloadFile(token) {
    window.location = "/api/v1/files/download/" + token
}

function initializeUpload() {
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
                url: '/api/v1/files/upload',
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
                    addUploadedFile(response.name, response.token);
                    showUploadedFile(response.name, response.token);
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
}

$(function () {
    'use strict';

    if (getCookie('user') === "") {
        window.location = "/login.html";
    }

    initializeUpload();

    fetchUploadedFiles();
    fetchConvertedFiles();

    showUploadedFiles();
    showConvertedFiles();
});

