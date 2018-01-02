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
    localStorage.files = null;
    $("#files").html("");

    let request = $.ajax({
        url: "/api/v1/files",
    });

    request.done(function(data) {
        let files = data['files'];
        for (let i = 0; i < files.length; i++) {
            addUploadedFile(files[i].name, files[i].token);
        }
        showUploadedFiles();
    });

    request.fail(function(err) {
        $("#files").append('<tr class="bg-danger"><td scope="row">Something went wrong.</td><td></td></tr>');
    });
}

function fetchConvertedFiles() {
    localStorage.converted_files = null;
    $("#converted-files").html("");

    let request = $.ajax({
        url: "/api/v1/files",
        data: {
            'converted': 1,
        },
    });

    request.done(function(data) {
        let files = data['files'];
        for (let i = 0; i < files.length; i++) {
            addConvertedFile({
                'filename': files[i].name,
                'token': files[i].token,
                'type': files[i].type,
                'status': files[i].status
            });
        }
        showConvertedFiles();
    });

    request.fail(function(err) {
    	$("#converted-files").append('<tr class="bg-danger"><td scope="row">Something went wrong.</td><td></td><td></td></tr>');
    });
}

function showUploadedFile(filename, token) {
	let actionButton = '<button class="btn btn-primary" data-toggle="modal" data-target="#convertModal" onclick="convertModal(\'' + token + '\')">Convert</button><button class="btn btn-danger" onclick="deleteFile(\'' + token + '\')">Delete</button>';
	$("#files").append('<tr>' + '<td scope="row">' + filename + '</td><td>' + actionButton + '</td></tr>');
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

function convertModal(token) {
    $("#convert-token").val(token);
}

function convertFile() {
    let token = $("#convert-token").val();
    let convert_from = $("#source-type").val();
    let convert_to = $("#destination-type").val();

    $("#source-type").val("");
    $("#destination-type").val("");

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

    $("#convertModal").modal('hide');
}

function downloadFile(token) {
    window.location = "/api/v1/files/download/" + token
}

function deleteFile(token) {
	let request = $.ajax({
		url: "/api/v1/files/delete/" + token,
		type: "POST",

		beforeSend: function (r) {
			r.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
		},
	});

    request.done(function(request) {
        fetchUploadedFiles();    
    });

	request.fail(function(error) {
		console.error(error);
	});
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

function initializeConvertionModal() {

}

$(function () {
    'use strict';

    if (getCookie('user') === "") {
        window.location = "/login.html";
    }

    initializeUpload();
	initializeConvertionModal();

    fetchUploadedFiles();
    fetchConvertedFiles();
});

