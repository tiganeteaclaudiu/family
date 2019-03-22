
username = '{{ username }}';

console.log('user!: '+username);

function init_variables(username) {
	
	$.ajax({
		url: '/get_username/',
		method: 'POST',
		success: function(data) {
			data = JSON.parse(data);
			username = data['username'];
			console.log("USERNAME: "+username);
		}
	});

}


jQuery(document).ready(function(){

init_variables();

function hide_all_content() {
	$(".content-2col").css('display','none');
}

$("#family-join-button").click(function(e) {
	e.preventDefault();

	hide_all_content();
	$("#content_join-family").css('display','flex');
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

		username = {{ username }};
		console.log("USERNAME: " + username);

		// $.ajax({
		// 	url: '/post_join_request/',
		// 	method: 'POST',
		// 	data: JSON.stringify({
		// 		'family' : family_id,
		// 		'user' : username
		// 	}),
		// });

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

})
