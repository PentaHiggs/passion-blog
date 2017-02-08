function showNameEmailwarning(bool) {
	if (bool) {
    return;
	}
    return;
}


$(document).ready($('a[title="commentResponseLink"]').click( function(event) {
    var idNoStr = event.target.id.substring(2);
    var textSource = "#crtext" + idNoStr;
    $('#RespondingToDiv').html($(textSource).html());
    // Displays link to allow resetting form to respond to original author
    $('#RestoreDiv').css('display', '');
    // Sets up the form to send the ID no of the post it's responding to in a hidden field
    $('#ResponseTo').attr('value', idNoStr);
}));

// Undoes the actions of the above function
$(document).ready($('#RestoreOriginalResponse').click( function() {
    $('#RespondingToDiv').html(" Responding to original author ");
    $('#RestoreDiv').css('display', 'none');
    $('#ResponseTo').attr('value', '');
}));
/*
$("#commentsForm").validate({
	rules: {
		nameInput : {
			required : true
		},
		emailInput : {
			required : true,
			email : true,
			remote : {
				url : "/ajax/comments/",
				type : "GET",
				dataType : "json",
				data : {
					purpose : "nameEmailValidation",
					name : function() {
						return $( "#nameInput1" ).val();
					},
					email : function() {
						return $( "#emailInput1" ).val();
					}
				},
				success : function(data, tStatus, jqReq) {
					if (!data.valid) {
						// Tell the user that the given name is under use with a different email, he must thus
						// select another name to use with the given email.
						showNameEmailWarning(true);
					}
					else { // combination is valid
						// Hide any warnings related to incorrect name-email combinations
						showNameEmailWarning(false);
					}
				}
			}
		},
		commentText : {
			required : true,
		},
	}
});
*/