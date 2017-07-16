var UploadForm = function (form, fileInput, progress) {
    form.on('submit', upload);
    var result = $("#result");
    var file = getFile();

    fileInput.on("change", function () {
        file = getFile();
    });

    function getFile() {
        return fileInput[0].files[0];
    }

    function handleProgress(e) {
        if (e.lengthComputable) {
            progress.attr({
                value: e.loaded,
                max: e.total
            });
        }
    }

    function handleSuccess(data, textStatus, jqXHR) {
        result.text('SUCCESS: ' + data);
    }

    function handleError(jqXHR, textStatus, errorThrown) {
        result.text('ERRORS: ' + textStatus);
    }

    function createCustomXHR() {
        var myXhr = $.ajaxSettings.xhr();
        if (myXhr.upload) {
            myXhr.upload.addEventListener('progress', handleProgress, false);
        }
        return myXhr;
    }

    function upload(e) {
        e.stopPropagation();
        e.preventDefault();

        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: new FormData(form[0]),
            cache: false,
            contentType: false,
            processData: false,
            xhr: createCustomXHR,
            success: handleSuccess,
            error: handleError
        });
    }
};
