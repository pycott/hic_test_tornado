function getCSRFTokenValue() {
    return getCookie("_xsrf");
}

$(function () {
    $.ajaxSetup({
        headers: {
            'X-Csrftoken': getCSRFTokenValue()
        }
    });
});