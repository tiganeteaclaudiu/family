
username = '{{ username }}';

console.log('user!: '+username);


jQuery(document).ready(function(){


sidebar_options = {
	'main-panel' : {
		'options' : [
			{
				'name' : 'Join Requests',
				'link' : 'join-requests',
				funct : function() {
					console.log("MERGE FUNCTIA!");
					query_join_requests();
					}
			},
			{
				'name' : 'Create Family',
				'link' : 'create-family'
			},
			{
				'name' : 'Join Family',
				'link' : 'join-family'
			}
		]
	}
}

//variable that holds the last page the user was on

{% if no_family == true %}

show_content('no-family');

{% else %}

show_content('main-panel');

{% endif %}

function show_content(id) {
	load_sidebar_options(id);
	hide_all_content();
	$('#content_'+id).css('display','flex');
}

function hide_all_content() {
	$(".content-2col").css('display','none');
}


function load_sidebar_options(content_id) {
	content = $("#"+content_id);
	
	try {

		if (content_id in sidebar_options) {

			menu = sidebar_options[content_id];
			console.log('MENU: '+JSON.stringify(menu));

			$('#side-menu > a').remove();

			for(var i=0;i<menu['options'].length;i++) {

				name = menu['options'][i]['name'];
				link = menu['options'][i]['link'];

				element = $('<a href="' + link +'"><div class="side-menu-option">'+ name +'</div></a>');

				$("#side-menu").append(element);

				if ('funct' in menu['options'][i]) {

					funct = menu['options'][i]['funct'];

					element.click(function(e) {
						e.preventDefault();
						funct();
					});

				}

			}

			load_sidebar_links();

		}

	} catch(err) {
		console.log('No sidebar options for element  '+err);
	}
}


function load_sidebar_links() {

	$("#side-menu > a").click(function(e) {
		e.preventDefault();
		link = $(this).attr('href');

		show_content(link);
	});

}


$("#family-join-button").click(function(e) {
	e.preventDefault();

	hide_all_content();
	show_content('join-family');
});

$("#join-family-search-name").click(function(e) {
	query_families('name');
});

$("#join-family-search-id").click(function(e) {
	query_families('id');
});

$("#join-family-switch-button").click(function(e) {
	if ($("#join-family-id-row").css("display") === 'none' ) {
		$("#join-family-name-row").hide();
		$("#join-family-id-row").css("display","flex");
		$("#join-family-switch-button").html('Search by name');
	} else {
		$("#join-family-id-row").hide();
		$("#join-family-name-row").css("display","flex");
		$("#join-family-switch-button").html('Search by ID');
	}
}); 

$("#family-create-button").click(function(e) {
	e.preventDefault();

	hide_all_content();
	show_content('created-family');
});

$(document).click(function(e) {
    if ($(e.target).is('#families-table td')) {
        e.preventDefault();
        console.log('pressed row');
    } else {
        console.log("did not press row");
        $('.cursor-button').remove();
    }
});

function refresh_cursor_button_event() {

	console.log("refresh_cursor_button_event");

	$("#families-table td").click(function(e) {
	    console.log("row click");
	    var num = Math.floor((Math.random() * 10) + 1);
	    var div = $('<div class="cursor-button">Send Join Request</div>');
	    container = $("#content_join-family");

	    $('.cursor-button').remove();

	    div.appendTo(container).offset({ top: e.pageY, left: e.pageX });

		family_id = $(e.target).parent().find('td').first().html();

		add_cursor_button_event(family_id);

	});

}

function add_cursor_button_event(family_id) {

	console.log("add_cursor_button_event");

	$(".cursor-button").click(function(e) {

		username = '{{ username }}';
		console.log("USERNAME: " + username);

		$.ajax({
			url: '/post_join_request/',
			method: 'POST',
			data: JSON.stringify({
				'family' : family_id,
				'user' : username
			}),
		});

	});

}

function empty_families_table() {
	$("#families-table tr, h3").remove()
}

function query_families(query_type) {

	data = {};

	if (query_type === 'name') {
		data = JSON.stringify({
			'query_type' : 'name',
			'name' : $('#join-family-name').val(),
			'location_data': $('#join-family-location').val()
		});
	} else {
		data = JSON.stringify({
			'query_type' : 'id',
			'id' : $("#join-family-id").val()
		});
	}

	$.ajax({
			url : '/query_families/',
			method : 'POST',
			data: data,
			success : function(data) {
				data = JSON.parse(data);
				families = data['families'];
				families = JSON.parse(families)
				console.log(families);

				empty_families_table();


				if(families.length != 0 ) {

					html = `<tr>
			                    <th> ID </th>
			                    <th> Name </th>
			                    <th> Location </th>
			                    <th> No. of members </th>
			                </tr>`

					$("#families-table").append(html);

					for( var i=0;i<families.length;i++ ) {
						family = families[i];
						console.log(family);
						html = `
							<tr>
			                    <td> `+family['id']+` </td>
			                    <td> `+family['name']+` </td>
			                    <td> `+family['location']+` </td>
			                    <td> `+family['members']+` </td>
			                </tr>
					`}

					$("#families-table").append(html);
					refresh_cursor_button_event();

				} else {
					console.log('NO FAMILIES');
					$("#families-table").append('<h3 style="text-align:center;">No families found.</h2>');
				}

			}
		});

}

function query_join_requests() {

	data = JSON.stringify({
		'username' : '{{ username }}'
	});

	$.ajax({
		url: '/query_join_requests/',
		method: 'GET',
		success: function(data) {

			console.log('aici1');

			data = JSON.parse(data);

			$("#join-requests-table tr").remove();

			html = `<tr>
	                    <th> ID </th>
	                    <th> Name </th>
	                    <th> Location </th>
	                    <th> Family </th>
	                </tr>`

			$("#join-requests-table").append(html);

			for( var i=0;i<data.length;i++ ) {
				
				family = data[i]['family'];
				requests = data[i]['requests'];

				console.log('aici: '+family+' --- '+JSON.stringify(requests));

				for (var j=0;j<requests.length;j++) {

					request = requests[j];

					html = `
						<tr>
		                    <td> `+request['id']+` </td>
		                    <td> `+request['name']+` </td>
		                    <td> `+request['location']+` </td>
		                    <td> `+family+` </td>
		                </tr>
					`

					$("#join-requests-table").append(html);
					add_request_cursor_button();

				}

			}


		}
	});

}

function add_request_cursor_button() {

	console.log("request_cursor_button_event");

	$("#join-requests-table td").click(function(e) {
	    console.log("row click");
	    var num = Math.floor((Math.random() * 10) + 1);
	    var div = $('<div class="cursor-button2">Accept</div>');
	    container = $("#content_join-requests");

	    $('.cursor-button2').remove();

	    div.appendTo(container).offset({ top: e.pageY, left: e.pageX });

		request_id = $(e.target).parent().find('td').first().html();

		request_cursor_button_event(request_id);

	});

}

function request_cursor_button_event(request_id) {

	console.log("request_cursor_button_event");

	$(".cursor-button2").click(function(e) {

		family = $(e.target).parent().find('td').last().html();
		console.log("cursor event family: " + family);

		$.ajax({
			url: '/accept_join_request/',
			method: 'POST',
			data: JSON.stringify({
				'requester_id' : request_id,
				'family' : family
			}),
			success: function(data) {
				query_join_requests();
			}
		});

	});

}

$(document).click(function(e) {
    if ($(e.target).is('#join-requests-table td')) {
        e.preventDefault();
        console.log('pressed row');
    } else {
        console.log("did not press row");
        $('.cursor-button2').remove();
    }
});

function add_family_member(username,family) {

	data = JSON.stringify({
		'username' : username,
		'family' : family
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

}

// ---------------------------- BUTTON EVENTS 

$("#content-back-button").click(function(e) {
	e.preventDefault();

});

$("#create-family-post-button").click(function(e){
	e.preventDefault();
	console.log('Submitted data.');
	name = $("#create-family-name").val();
	country = $("#create-family-country").val();
	location_data = $("#create-family-location").val();
	phrase = $("#create-family-phrase").val();


	data = JSON.stringify({
		'name' : name,
		'country' : country,
		'location_data' : location_data,
		'phrase' : phrase
	});

	$.ajax({
		url: '/post_family/',
		method: 'POST',
		data: data,
		success: function(data) {
			data = JSON.parse(data);
			if(data['status'] === 'success') {
				console.log('post_family success');
				add_family_member('{{ username }}',name);
				show_content('created-family');
			}

		}
	});
});

$("#created-family-button").click(function(e) {
	e.preventDefault();
	location.reload();
});


});