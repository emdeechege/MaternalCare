// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getDaysInMonth(month, year) {
    var date = new Date(year, month, 1);
    var days = [];
    while (date.getMonth() === month) {
        days.push(new Date(date));
        date.setDate(date.getDate() + 1);
    }
    return days;
}

// $(document).ready(function () {

function submitForm(form_id) {

    var $bookForm = $('#' + )

    $bookForm.submit(function (event) {
        event.preventDefault()
        console.log('submited')
        var $formData = $(this).serialize()
        var $thisURL = $bookForm.attr('data-url') || window.location.href
        console.log($formData)
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            // dataType: Text,
            success: handleFormSuccess,
            error: handleFormError,
        })
    })

    function handleFormSuccess(info, textStatus, jqXHR) {
        // var $testContent = $('.js_update_items')
        // $testContent.html(info)
        console.log(info)
    }

    function handleFormError(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
        console.log(textStatus)
        console.log(errorThrown)
    }
}

function getId(id) {
    var el = $('#' + id)
    var $month = el.attr('data-month')
    var $day = $('#' + id).html();

    console.log($month, $day)
}