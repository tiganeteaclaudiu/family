//JAVASCRIPT FOR LOGIN PAGE

//only load script after page finished loading
$(document).ready(function(){

	console.log('Document ready.');

	$(document).keypress(function(event){
	    var keycode = (event.keyCode ? event.keyCode : event.which);
	    if(keycode == '13'){
	        login_post();  
	    }
	});

	$("#login-submit").click(function(e) {
		e.preventDefault();
		login_post();
	});

	function login_post() {
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
				data = JSON.parse(data);
				if(data['status'] === 'success') {
					console.log('logged_in')
					window.location.href = '../index/';
				}
				else console.log("Login failed");
			}
		});
	}

});