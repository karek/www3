function edit_click() {

//Close all open forms
	cancel();

//  wyslac zapytanie o aktualna wartosc pol
	var btn = $(document.activeElement);
	var tr = btn.parent().parent();
	var id = tr.data("id");
	var cur_obw;

	var karty = tr.find(".ileKart");
	var uprawnieni = tr.find(".uprawnionych")

	btn.hide();
	btn.next().show();
	btn.next().next().show();

    $.ajax({
        url : "obwod/", // the endpoint
        type : "POST", // http method
        data : { obw_id : id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
			cur_obw = json;
			console.log("In Opening: ")
			console.log(cur_obw);
			karty.replaceWith( "<td class = 'ileKart otwarteIle'> " +
				"<input class='otwIle' data-ile=" + cur_obw.ile + " type='number' value=" + cur_obw.ile + " min=0> </td>");

			uprawnieni.replaceWith( "<td class = 'uprawnionych otwarteUpr'> " +
				"<input class='otwUpr' data-ile=" + cur_obw.upr + " type='number' value=" + cur_obw.upr +" min=0> </td>");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function cancel() {
	show_edits();
	close_inputs();
};

function close_inputs() {
	$('.otwarteIle').replaceWith("<td class='ileKart'>" +  $('.otwarteIle').find(".otwIle").data("ile") + "</td>");
	$('.otwarteUpr').replaceWith("<td class='uprawnionych'>" +  $('.otwarteUpr').find(".otwUpr").data("ile") + "</td>");
};

function show_edits() {
	$('.message').empty();
	$('.zapisz').hide();
	$('.anuluj').hide();
	$('.edytuj').show();
};

function save() {
	var btn = $(document.activeElement);
	var tr = btn.parent().parent();
	var id = tr.data("id");
	var ile = $('.otwarteIle').find(".otwIle").val();
	var upr = $('.otwarteUpr').find(".otwUpr").val();
	var wer = tr.find(".wersja").val();

	$.ajax({
        url : "save/", // the endpoint
        type : "POST", // http method
        data : { obw_id : id, ileKart: ile, upr: upr, wer: wer}, // data sent with the post request

        // handle a successful response
        success : function(json) {
			cur_obw = json.dict;
			show_edits();
			tr.find(".ileKart").replaceWith("<td class='ileKart'>" + cur_obw.ile + "</td>");
			tr.find(".uprawnionych").replaceWith("<td class='uprawnionych'>" + cur_obw.upr + "</td>");
			tr.find(".wersja").val(cur_obw.wer);


			if(json.err == true) {
				$('.message').append("<h2>Błąd! Ktoś w międzyczasie zapisał inny wynik!</h2>");
			}

			console.log("Closing: ")
			console.log(cur_obw)

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
			cancel();
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
