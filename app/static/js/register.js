//JAVASCRIPT FOR REGISTRATION PAGE

//only load script after page finished loading
$(document).ready(function(){

	console.log('Document ready.');

$("#register-submit").click(function(){
	console.log('Submitted data.');
	username = $("#register-username");
	email = $("#register-email");
	password = $("#register-password");
	submit = $("#register-submit");

	data = JSON.stringify({
		'username' : username.val(),
		'email' : email.val(),
		'password' : password.val(),
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
			else console.log("Register failed");
		}
	});
});

$("#family-submit").click(function(){
	console.log('Submitted data.');
	username = $("#user-username");
	family = $("#family-name");
	submit = $("#family-submit");

	data = JSON.stringify({
		'username' : username.val(),
		'family' : family.val()
	});

	$.ajax({
		url: '/add_family_member/',
		method: 'POST',
		data: data,
		success: function(data) {
			console.log('add_family_member success');
			// data = JSON.parse(data);
			// if(data['status'] === 'success') {
			// 	window.location.href = '../index/';
			// }
			// else console.log("Register failed");
		}
	});
});

});