//JAVASCRIPT FOR LOGIN PAGE

//only load script after page finished loading
$(document).ready(function(){

	console.log('Document ready.');

$("#login-submit").click(function(){
	console.log('Submitted data.');
	username = $("#login-username");
	email = $("#login-email");
	password = $("#login-password");
	submit = $("#login-submit");

	data = JSON.stringify({
		'username' : username.val(),
		'email' : email.val(),
		'password' : password.val(),
	});

	$.ajax({
		url: '/post_login/',
		method: 'POST',
		data: data,
		dataType: 'text',
  		contentType: "application/json",
		success: function(data) {
			console.log('post_login success');
			// data = JSON.parse(data);
			// if(data['status'] === 'success') {
			// 	console.log('logged_in')
			// 	window.location.href = 'index.html';
			// }
			// else console.log("Login failed");
		},
		error: function(error) {
			console.log("ERROR");
		}
	});

});