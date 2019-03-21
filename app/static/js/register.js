//JAVASCRIPT FOR REGISTRATION PAGE

//only load script after page finished loading
$(document).ready(function(){

	console.log('Document ready.');

$("#register-submit").click(function(){
	console.log('Submitted data.');
	username = $("#register-username");
	email = $("#register-email");
	password = $("#register-password");
	password_confirm = $("#register-password-confirm");
	location_data = $("#register-location");
	submit = $("#register-submit");

	data = JSON.stringify({
		'username' : username.val(),
		'email' : email.val(),
		'password' : password.val(),
		'confirm_password' : password_confirm.val(),
		'location' : location_data.val()
	});

	$.ajax({
		url: '/post_register/',
		method: 'POST',
		data: data,
		success: function(data) {
			console.log('post_login success');
			data = JSON.parse(data);
			if(data['status'] === 'success') {
				window.location.href = '../login/';
			}
			else {
				$("#registration-failure").html(data['message']);
				$("#registration-failure").show();
			}
		}
	});
});

});