
username = '{{ username }}';

console.log('user!: '+username);

console.log(document.domain + ':' + location.port);

jQuery(document).ready(function(){

	$("#side-menu-header").html(username);

	var socket = io.connect('http://' + document.domain + ':' + location.port);


current_family = '';

menu_options = {
	'user-menu' : {
		'user-menu-main-panel' : [
				{
					'name' : 'Join Requests',
					'link' : 'join-requests',
					funct : function() {
						console.log("MERGE FUNCTIA!");
						console.log("MERGE FUNCTIA!");
						console.log("MERGE FUNCTIA!");
						console.log("MERGE FUNCTIA!");
						console.log("MERGE FUNCTIA!");
						console.log("MERGE FUNCTIA!");
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
				},
				{
					'name' : 'Leave Family',
					'link' : 'leave-family',
					funct: function() {
						query_families('user','leave-family-table','/leave_family/');

					}
				}
			],
		'join-requests' : [
				{
					'name' : 'Leave Family',
					'link' : 'leave-family',
					funct: function() {
						console.log("MERGE FUNCTIA!");
						console.log("MERGE FUNCTIA!");
					}
				},
				{
					'name' : 'test2',
					'link' : 'join-family',
					funct: function() {
						console.log("MERGE FUNCTIA2!");
						console.log("MERGE FUNCTIA2!");

					}
				}
			],
		'leave-family' : [
			{
				'name' : 'test2',
				'link' : 'create-family',
				funct: function() {
					console.log('TESTTESTESTESTEST');
				}
			}
		]
	},
	'family-menu' : {
		'family-menu-main-panel' : [
				{
					'name' : 'Reminders',
					'link' : 'family-reminders',
					funct : function() {
						console.log("MERGE FUNCTIA pt reminder!");
						query_reminders();
					}
				},
				{
					'name' : 'Lists',
					'link' : 'family-lists',
					funct : function() {
						console.log('merge functia pt lists!');
						query_lists();
					}
				},
				{
					'name' : 'Calendar',
					'link' : 'family-calendar',
					funct : function() {
						console.log("MERGE FUNCTIA pt reminder!");
						query_events();
					}
				}
			]
	},
	'family-chat' : {
		'family-chat-main-panel' : [
			{
				'name' : 'Family Chat',
				'link' : 'family-chat',
				funct : function() {
					query_chat_messages();
				}
			}
		]
	}
}


//variable that holds the last page the user was on

{% if no_family == true %}

show_content('no-family');

{% else %}

load_sidebar_options('user-menu');

{% endif %}

function load_menu_options() {
	console.log('load_menu_options called');
	for (var key in menu_options) {
		console.log('KEY: '+key);
		load_menu_options_events(key);
	}
}

function load_menu_options_events(key) {
	$("#"+key).click(function(e) {
		console.log('CLICKED: ');
		console.log($(this));
		load_sidebar_options(key);
	});
}

load_menu_options();

function show_content(id) {

	console.log('show_content id = '+id);

	load_sidebar_options(id);
	hide_all_content();
	$('#content_'+id).css('display','flex');
}

function hide_all_content() {
	$(".content-2col").css('display','none');
}

//Function adding sidebar options
//Supports adding sidebar options by either clicking items on the top menu or
// items on the sidebar

//menu_options format:
//	-first level (dict) : top menu items
//	-second level (dict) : sidebar items that spawn another sidebar elements
//	-third layer (array of dicts) : sidebar elements
//		-name: name that appears on sidebar button
//		-link: link to content (content tabs have the format content_LINK)
//		-function: function to execute on clicking the sidebar element
function load_sidebar_options(menu_option,sidebar_option) {
	content = $("#"+menu_option);

	if (typeof sidebar_option === 'undefined') { sidebar_option = menu_option+"-main-panel"; }

	console.log('load_sidebar_options menu_option = '+menu_option);
	console.log('load_sidebar_options sidebar_option = '+sidebar_option);

	try {
		//first level: button is found on top bar
		if (menu_option in menu_options) {
			//sidebar is cleared, to be filled again
			$('#side-menu > a').remove();

			// menu = second level
			menu = menu_options[menu_option];
			console.log('load_sidebar_options menu: '+JSON.stringify(menu));
			console.log("load_sidebar_options sidebar option: "+JSON.stringify(menu[sidebar_option]));

			sidebar_options = menu[sidebar_option];
			//third level
			for (var i=0;i<=sidebar_options.length-1;i++) {

				console.log('load_sidebar_options sidebar[i]:' + JSON.stringify(sidebar_options[i]));

				option = sidebar_options[i];

				name = option['name'];
				link = option['link'];

				console.log('name = '+name);
				console.log('link = '+link);

				//sidebar element is created
				element = $('<a href="' + link +'"><div class="side-menu-option">'+ name +'</div></a>');

				//sidebar element is added
				$("#side-menu").append(element);

				//if there is a funct on the third level, it's bound to a click event
				if ('funct' in option) {
					funct = option['funct'];
					add_sidebar_funct(element,option['funct']);
				}

			}
			//load_menu_links method binds the click events to the new sidebar options
			//menu, menu_option are passed further for recursivity:
			//	if "link" is in menu, that means a newly created sidebar item is also on level 2
			//	 so it actually runs load_sidebar_options again for his own sidebar elements
			load_menu_links(menu, menu_option);

		}

	} catch(err) {
		console.log('No menu options for element  '+err);
	}
}

function add_sidebar_funct(element,funct) {

	element.click(function(e) {
		e.preventDefault();
		funct();
	});
}

//binds click events to new sidebar items
//	if "link" is in menu, that means a newly created sidebar item is also on level 2
//	 so it actually runs load_sidebar_options again for his own sidebar elements
function load_menu_links(menu, menu_option) {

	console.log('load_menu_links called: ');
	console.log('menu: '+JSON.stringify(menu))
	console.log('menu_option: '+JSON.stringify(menu_option))


	$("#side-menu > a").click(function(e) {
		e.preventDefault();
		link = $(this).attr('href');

		if (link in menu ) {
			console.log("FOUND AICI ASIDA SDASDASDASDASASD" + link);
			link2 = link;
			$('#content_'+link2).css('display','flex');
			load_sidebar_options(menu_option,link2);
			add_back_button(menu_option);
			show_content(link2);
			return '';
		}

		console.log("SHOWING LINK: =========> "+link);
		show_content(link);
	});

}

function add_back_button(menu_option) {
	element = $('<a class="sidebar-back-button"><div class="side-menu-option">Back</div></a>');
	$("#side-menu").append(element);
	$("#side-menu > .sidebar-back-button").click(function(e) {
		e.preventDefault();
		load_sidebar_options(menu_option);
		show_content(menu_option+'-main-panel');
	});
}


$("#family-join-button").click(function(e) {
	e.preventDefault();

	hide_all_content();
	show_content('join-family');
});

$("#join-family-search-name").click(function(e) {
	query_families('name',"families-table",'/post_join_request/');
});

$("#join-family-search-id").click(function(e) {
	query_families('id',"families-table",'/post_join_request/');
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

function hide_cursor_buttons(table_id) {
	console.log('hide_cursor_buttons');
	console.log(table_id+' td');
	$(document).click(function(e) {
    if ($(e.target).is(table_id+' td')) {
        e.preventDefault();
        console.log('pressed row');
    } else {
        console.log("did not press row");
        $(table_id).parent().find('.cursor-button').remove();
    }
	});
}




function refresh_cursor_button_event(table_id,url,extra_data) {

	if (typeof extra_data === 'undefined') { extra_data = ''; }

	console.log("refresh_cursor_button_event");
	console.log(table_id+" td");

	$(table_id+" td").click(function(e) {
	    console.log("row click");
	    var num = Math.floor((Math.random() * 10) + 1);
	    var div = $('<div class="cursor-button">Send Join Request</div>');
	    container = $(table_id).parent();
	    console.log('REFRESH CONTAINER: ');
	    console.log(container);

	    hide_cursor_buttons(table_id);

	    div.appendTo(container).offset({ top: e.pageY, left: e.pageX });

	    console.log(container)
	    button = container.find('.cursor-button');
	    console.log(button);

		id = $(e.target).parent().find('td').first().html();

		add_cursor_button_event(id,url,extra_data);

	});

}



function add_cursor_button_event(id,url,extra_data) {

	if (typeof extra_data === 'undefined') { extra_data = ''; }

	console.log("add_cursor_button_event");

	$(".cursor-button").click(function(e) {

		username = '{{ username }}';
		console.log("USERNAME: " + username);

		data = {
			'id' : id,
			'user' : username
		}

		if (extra_data !== '') {

			console.log("ADD CURSOR FOUND EXTRA DATA:  ");
			console.log(JSON.stringify(extra_data));

			for (var key in extra_data) {
				data[key] = extra_data[key];
			}
			console.log('DATA AFTER EXTRA: '+JSON.stringify(data));

		}

		$.ajax({
			url: url,
			method: 'POST',
			data: JSON.stringify(data)
		});

	});

}



function empty_table(table_id) {
	$(table_id+" tr, h3").remove();
}

function query_families(query_type, table_id, popup_url) {

	if (typeof popup_url === 'undefined') { popup_url = ''; }

	data = {};

	table_id = "#" + table_id;

	if (query_type === 'name') {
		data = JSON.stringify({
			'query_type' : 'name',
			'name' : $('#join-family-name').val(),
			'location_data': $('#join-family-location').val()
		});
	} else if (query_type === 'id') {
		data = JSON.stringify({
			'query_type' : 'id',
			'id' : $("#join-family-id").val()
		});
	} else if (query_type === 'user') {
		data = JSON.stringify({
			'query_type' : 'user',
			'username' : '{{ username }}'
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

				empty_table(table_id);

				html = `<tr>
			                    <th> ID </th>
			                    <th> Name </th>
			                    <th> Location </th>
			                    <th> No. of members </th>
			                </tr>`;


				if(families.length != 0 ) {

					for( var i=0;i<families.length;i++ ) {
						family = families[i];
						console.log(family);
						html += `
							<tr>
			                    <td> `+family['id']+` </td>
			                    <td> `+family['name']+` </td>
			                    <td> `+family['location']+` </td>
			                    <td> `+family['members']+` </td>
			                </tr>
					`}

					$(table_id).append(html);

					console.log("POPUP_URL = "+popup_url)

					if(popup_url !== '') {
						refresh_cursor_button_event(table_id,popup_url);
					}


				} else {
					console.log('NO FAMILIES');
					$(table_id).append('<h3 style="text-align:center;">No families found.</h2>');
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

					extra_data = {
						'family' : current_family
					}

					refresh_cursor_button_event('#join-requests-table','/accept_join_request/',extra_data);

				}

			}


		}
	});

}



function add_request_cursor_button() {
	refresh_cursor_button_event('join-requests-table','/accept_join_request/');
}


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

function load_family_droplist() {

	data = {
		'query_type' : 'user',
		'username' : '{{ username }}'
	}

	data = JSON.stringify(data);

	$.ajax({
		url : '/query_families/',
		method : 'POST',
		data: data,
		success : function(data) {
			data = JSON.parse(data);
			families = data['families'];
			families = JSON.parse(families)
			if( JSON.stringify(families) === '[]') {
				console.log('NO FAMILY ============');
			} else {

				empty_family_droplist();

				for(var i=0;i<families.length;i++) {
					name = families[i]['name'];
					console.log('FAMILIES ========'+name);
					html = '<option value="'+name+'" selected="selected">'+name+'</option>';
					$("#family-droplist").append(html);
				}

				if(families.length === 1) {
					console.log('ADASDASDASS');
					console.log(families);
					
					data = {
						'family_name' : families[0].name,
						'username' : '{{ username }}'
					}
					$.ajax({
						url: '/set_current_family/',
						method: 'POST',
						data: JSON.stringify(data),
						success: function(data) {
							data = JSON.parse(data);
							current_family = name;
						}
					});

				}

				get_current_family();
			}
		}
	});
}

function empty_family_droplist() {
	$("#family-droplist").find('option').remove();
}

load_family_droplist();

function set_current_family(name) {
	data = {
		'family_name' : name,
		'username' : '{{ username }}'
	}
	$.ajax({
		url: '/set_current_family/',
		method: 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			data = JSON.parse(data);
			current_family = name;
			location.reload(0);
		}
	});
}

function get_current_family() {
	data = {
		'username' : '{{ username }}'
	}

	$.ajax({
		url: '/get_current_family/',
		method: 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			data = JSON.parse(data);

			if(data['status'] == 'success' && data['current_family'] !== '') {
				droplist = $("#family-droplist");
				droplist.val(data['current_family']);
				current_family = data['current_family'];
			}
		}
	});

	join_family_chat();
}

function return_current_family() {
	return current_family;
}

get_current_family();

function query_reminders() {

	console.log('CURRENT FAMILY = ========123123=======')
	console.log(current_family);

	data = {
		'family_name' : return_current_family()
	}

	$.ajax({
		url: '/query_reminders/',
		method: 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			console.log("VARUTUUUUUUU");
			data=JSON.parse(data);
			if(data['status'] === 'success') {
				reminders = JSON.parse(data['reminders']);
				reminders = reminders['reminders'];

				load_reminders(reminders);
			}
		}
	});

}

function add_reminders(body) {

	data = JSON.stringify({
		'family_name' : current_family,
		'username' : '{{ username }}',
		'body' : body,
	});

	console.log('add_reminders data: ');
	console.log(data);

	$.ajax({
		url: '/post_reminders/',
		method: 'POST',
		data: data,
		success: function(data) {
			data = JSON.parse(data);
			query_reminders();
		}
	});

}

function load_reminders(reminders) {

	console.log('load_reminders data: '+JSON.stringify(reminders));

	table = $("#reminders-table");
	table.find('tr').remove();

	for (var i=0;i<=reminders.length-1;i++)	{
		console.log('reminder: '+reminders[i]);
		html = '<tr>';
		html += '<td style="display:none">'+i+'</td>';
		html += '<td>'+reminders[i]['body']+'</td>';
		html += '<td>by:'+reminders[i]['user']+'</td>';
		html += '<td>'+reminders[i]['date_time']+'</td>';
		html += '</tr>';
		element = $(html);
		var delete_checkbox = $('<td>Delete:<input type="checkbox" style="margin-left:5px;"></td>');
		table.append(element);
		element.append(delete_checkbox);
		load_reminder_event(delete_checkbox, element);
	}
}

function load_reminder_event(element_to_click, element_to_delete) {

	element_to_click.click(function(e) {
		id = $(this).closest('tr').find('td').first().html();
		console.log('ID ===============');
		console.log(id);
		delete_reminders(id);
		element_to_delete.remove();
		setTimeout(query_reminders,500);
	});

}

function delete_reminders(id) {

	data = {
		'id' : id,
		'family_name' : current_family
	};

	$.ajax({
		url : '/delete_reminders/',
		method : 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			data = JSON.parse(data);
		}
	});
}

// -----------------------------FAMILY LISTS
$('#lists-add-button').click(function(e) {
	e.preventDefault();

	console.log('WOOOOOOOO');
	clone =	$("#lists-element-input").clone();

	clone.appendTo('#family-lists-elements-container');
	clone.val('');
});


function query_lists() {

	console.log('CURRENT FAMILY = ========123123=======')
	console.log(current_family);

	data = {
		'family_name' : return_current_family()
	}

	$.ajax({
		url: '/query_lists/',
		method: 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			console.log("VARUTUUUUUUU");
			data=JSON.parse(data);
			if(data['status'] === 'success') {
				lists = JSON.parse(data['lists']);
				lists = lists['lists'];

				load_lists(lists);
			}
		}
	});

}

function load_lists(lists) {

	$("#family-lists-table").find('td').remove();

	for(var i=0;i<lists.length;i++) {
		id =lists[i]['id'];
		title = lists[i]['title'];
		date_time = lists[i]['date_time'];
		date_time = date_time.substr(0,10);
		user = lists[i]['user'];
		elements = JSON.parse(lists[i]['elements'])['elements'];

		html = '<tr class="family-lists-table-row">';
		// html = '<td style="display:none">'+id+'</td>';
		html += '<td>'+i+'</td>';
		html += '<td>'+title+'</td>';
		html += '<td>'+user+'</td>';
		html += '<td>'+date_time+'</td>';
		html += '</tr>';

		new_row = $(html);

		var delete_button = $('<td>X</td>');
		new_row.append(delete_button);

		//load delete button event
		load_list_remove_events(delete_button, new_row);

		$("#family-lists-table").append(new_row);

		for(var j=0;j<elements.length;j++) {
			console.log(elements[j]);
			html = `<tr class='family-lists-element' style="display:none;background-color: #2ad4ea;width: 100%;">
				<td>`+(elements.length-j)+`</td>
				<td>`+elements[j]+`</td>
				<td></td>
				<td></td>
			</tr>`;

			new_element_row = $(html);

			new_element_row.insertAfter(new_row);
		}
			new_row.closest('tr').next().addClass('inset-shadow');
	}

	load_lists_events();

}

function load_lists_events() {
	$(".family-lists-table-row").click(function(e) {
		e.preventDefault();
		console.log('clicked:');
		console.log($(this));
		elements = $(this).nextUntil('.family-lists-table-row');
		if($(this).closest('tr').next().css('display') === 'none') {
			elements.show();
		} else {
			elements.hide();
		}
	});

}

function load_list_remove_events(element_to_click, element_to_delete) {
	element_to_click.click(function(e) {
		id = $(this).closest('tr').find('td').first().html();
		console.log('clicked remove list');
		console.log(id);
		delete_list(id);

		element_rows = $(element_to_delete).nextUntil('.family-lists-table-row');
		element_rows.remove();

		element_to_delete.remove();
		console.log('removed');
		// setTimeout(query_reminders,2000);
	});
}

function delete_list(id) {

	data = {
		'id' : id,
		'family_name' : current_family
	};

	$.ajax({
		url : '/delete_lists/',
		method : 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			data = JSON.parse(data);
			query_lists();
		}
	});
}

function jsonify_lists() {

	inputs = $("#family-lists-elements-container > .lists-input");
	json_object = {'elements' : []};

	console.log("INPUTS: ");
	console.log(inputs);

	elements = [];

	for(var i=0;i<inputs.length;i++) {
		value = inputs.eq(i).val();

		if(value !== '') {
			elements.push(value);
		}
	}

	json_object['elements'] = elements;

	return JSON.stringify(json_object)

}

function add_lists() {

	elements = jsonify_lists();

	data = JSON.stringify({
		'family_name' : current_family,
		'username' : '{{ username }}',
		'title' : $("#lists-title-input").val(),
		'elements' : elements
	});

	console.log('add_lists data: ');
	console.log(elements);

	title = $("#lists-title-input").val();

	if(title === '') {
		alert('Please insert a title to your new list.');
	} else {
		//check if list of elements is empty

		if (elements === '{"elements":[]}') {
			alert('Please insert at least one item in elements list.')
		} else {
			//list is good to add
			$.ajax({
				url: '/post_lists/',
				method: 'POST',
				data: data,
				success: function(data) {
					data = JSON.parse(data);
					query_lists();
				}
			});
		}

	}

}

function reload_list_input() {
		inputs =	$('[id="lists-element-input"]');
		inputs.remove();
		new_input = $('<input type="text" id="lists-element-input" placeholder="Element" maxlength="140" class="lists-input">');
		$("#family-lists-elements-container").append(new_input);
}


//------------------------------- FAMILY CALENDAR
//
// $('#calendar').fullCalendar({
//     selectable: true,
//     header: {
//       left: '',
//       center: 'title',
//       left: 'prev,next today'
//     },
//     dayClick: function(date) {
//       alert('clicked ' + date.format());
//     },
//     select: function(startDate, endDate) {
//       alert('selected ' + startDate.format() + ' to ' + endDate.format());
//     },
// 		events: [
// 			{
// 				title  : 'event1',
// 				start  : '2019-02-01',
// 				description: 'This is a cool event'
// 			},
// 			{
// 				title  : 'eventtesttestestewst',
// 				start  : '2019-02-01'
// 			},
// 			{
// 				title  : 'event2',
// 				start  : '2019-02-05',
// 				end    : '2019-02-07'
// 			},
// 			{
// 				title  : 'event3',
// 				start  : '2019-02-09T12:30:00',
// 				allDay : false // will make the time show
// 			}
// 		]
//   }
//   );


var today_date = moment().format('YYYY-MM-DD');
console.log(today_date);
// $('#calendar').fullCalendar('gotoDate', today_date);
$('#calendar').fullCalendar({
    theme: false,
    header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,basicWeek'
        // right: 'month,basicWeek,basicDay'
    },
    // header: { center: 'month,agendaWeek' }, // buttons for switching between views
    defaultDate: today_date,
    businessHours:
     {
        rendering: 'inverse-background',
        dow: [0,1]
     },
    editable: false,
    eventLimit: true, // allow "more" link when too many events
    eventRender: function (event, element) {
           element.attr('href', 'javascript:void(0);');
           element.click(function() {
						 console.log(event);
	 						console.log('desc: '+event.description);
	 						console.log('title '+event.title);
							console.log('ID XXXXXXX=--====== '+event.id);

							show_event_input(event);
           });
       },
		selectable : true,
		dayClick: function(date) {
      // alert('clicked ' + date.format());
			show_event_input({'start' : date, 'end' : date});
    },
    select: function(startDate, endDate) {
      // alert('selected ' + startDate.format() + ' to ' + endDate.format());
			show_event_input({'start' : startDate, 'end' : endDate});
    }
	});

function show_event_input(event) {
	title_field = $("#event-title-input");
	description_field = $("#events-description-input");
	start_date_field = $("#event-start-date");
	end_date_field = $("#event-end-date");

	console.log(title_field);
	console.log(description_field);
	console.log(start_date_field);
	console.log(end_date_field);

	console.log(event.title);
	console.log(event.description);
	console.log(event.start.format());
	console.log(event.end.format());

	title_field.val(event.title);
	description_field.val(event.description);
	start_date_field.html(event.start.format());
	end_date_field.html(event.end.format());

	$("#event-delete-button").off("click");

	$("#event-delete-button").click(function() {
		console.log('PRESSED DELETEXXXXXXXXXXXXXXXXXXXXXXXXXXX');
		delete_event(event);
	});

	if(event.title != undefined) {
		console.log('CLICKED EVENT TO UPDATE');
		$("#event-create-button-text").html('Update');

		$("#event-create-button").off('click');

		$("#event-create-button").click(function() {
			console.log('CLICKED UPDATE')
			event_data = {
				'id' : event.id,
				'title' : title_field.val(),
				'description' : description_field.val(),
				'start_date' : start_date_field.html(),
				'end_date' : end_date_field.html()
			}

			update_calendar_event(event_data);
		})
	} else {
		$("#event-create-button-text").html('Create');

		$("#event-create-button").off('click');

		$("#event-create-button").click(function() {
			if(verify_event_inputs() === true) {
				create_calendar_event();
			}
		})
	}

	$("#family-event-create-wrapper").css('display','flex');
}

function verify_event_inputs() {
	title_field = $("#event-title-input");
	description_field = $("#events-description-input");

	title = title_field.val();
	description = description_field.val();

	console.log('verify');
	console.log(title + '  ' + description);

	if(title === '') {
		alert('Please insert a title to your new event.');
		return false;
	} else {
		if (description === '') {
			alert('Please insert a description for your new event.');
			return false
		} else {
			return true
		}

	}
}

function create_calendar_event() {
	console.log('entered create_event');

	start_date = $("#event-start-date").html();
	end_date = $("#event-end-date").html();
	event_title = $("#event-title-input").val();
	event_description = $("#events-description-input").val();

	data = JSON.stringify({
		'start_date' : start_date,
		'end_date' : end_date,
		'event_title' : event_title,
		'event_description' : event_description
	});

	$.ajax({
		url: '/post_events/',
		method: 'POST',
		data: data,
		success: function(data) {
			data = JSON.parse(data);
			if(data['status'] === 'success') {
				setTimeout(query_events,1000);
				$("#family-event-create-wrapper").hide();
			}
		}
	});

}


function query_events() {

	console.log('CURRENT FAMILY = ========123123=======')
	console.log(current_family);

	events = []

	$.ajax({
		url: '/query_events/',
		method: 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			console.log("query_events result:");
			console.log(JSON.parse(data));
			data=JSON.parse(data);
			events = JSON.parse(data['events']);

			console.log('events ==============')
			console.log(events);

			load_calendar_events(events['events']);

			console.log('returning events');
			console.log(events['events']);
		return events['events'];
		}
	});
}

function load_calendar_events(events) {
	console.log('events ==============22')
	console.log(events);

	$("#calendar").fullCalendar('removeEvents');

	setTimeout(function() {
			$('#calendar').fullCalendar('addEventSource', events);
	}, 500);

}

function delete_event(event) {

	data = {
		'id' : event.id
	};

	$.ajax({
		url : '/delete_event/',
		method : 'POST',
		data: JSON.stringify(data),
		success: function(data) {
			data = JSON.parse(data);
			$("#family-event-create-wrapper").hide();
			query_events();
		}
	});
}

function update_calendar_event(event_data) {

	$.ajax({
		url : '/update_event/',
		method : 'POST',
		data: JSON.stringify(event_data),
		success: function(data) {
			data = JSON.parse(data);
			$("#family-event-create-wrapper").hide();
			query_events();
		}
	});
}

//--------------- SOCKETIO

function join_family_chat() {
	console.log('[SOCKETIO] Trying to join family chat.')
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.emit('join_family_chat', {});
}

function add_chat_message(body, sender, timestamp){
	container = $("#family-chat-container");
	received = true;

	if (sender === username){
		received = false;
	} else {
		received = true;
	}

	//change class depending on message sender (sent or received)
	if (received === true) {
		new_message_html = '<div class="family-chat-message-row-received">';
		new_message_html += '<p class="family-chat-message-sender">'+sender+':</p>';
		new_message_html += "<p class='family-chat-message-body'>"+body+"</p>";
	} else {
		new_message_html =  '<div class="family-chat-message-row-sent">';
		new_message_html += '<p class="family-chat-message-sender">You:</p>';
		new_message_html += "<p class='family-chat-message-body'>"+body+"</p>";
	}

	new_message_html += '</div>';

	new_message_element = $(new_message_html);
	console.log('[CHAT] adding element html:');
	console.log(new_message_html);
	container.append(new_message_element);

	console.log('[CHAT] adding element element:');
	console.log(new_message_element);
}

$("#family-chat-input-send").click(function() {
	console.log('CLICKED FAMILY CHAT INPUT SEND');
	family_chat_send_message();
});

function family_chat_send_message() {
	body = $("#family-chat-input").val();
	sender = username;
	timestamp = new Date();

	console.log('[CHAT] Sending message:')
	console.log('body: '+body);
	console.log('sender: '+sender);
	console.log('timestamp: '+timestamp);

	socket.emit('chat_message', {body: body, sender: sender, timestamp: timestamp});
}

socket.on('connect', function() {
	socket.emit('message', {data: 'I\'m connected!'});
});

socket.on('joined_room', function(msg){
msg = JSON.parse(msg);
room_username = msg['username'];
console.log(room_username+' joined the room!');
});

socket.on('chat_message', function(msg){
	msg = JSON.parse(msg);

	body = msg['body'];
	sender = msg['sender'];
	timestamp = msg['timestamp'];

	console.log('[CHAT] Message:');
	console.log('sender: '+sender);
	console.log('body: '+body);
	console.log('timestamp: '+timestamp);

	add_chat_message(body,sender,timestamp);
});


function query_chat_messages() {

	$.ajax({
		url: '/query_chat_messages/',
		method: 'POST',
		data: '',
		success: function(data) {
			data=JSON.parse(data);
			messages = JSON.parse(data['messages']);
			console.log('query chat data;');
			console.log(messages);
		}
	});

}


// ---------------------------- BUTTON EVENTS
$("#content-back-button").click(function(e) {
	e.preventDefault();
	console.log(current_family);
	// query_reminders();
	add_lists();
});

$("#family-droplist").change(function() {
	value = $(this).val();
	console.log("FAMILY DROPLIST CURRENT: "+value);

	set_current_family(value);

	$("#family-droplist").val(value);

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

				set_current_family(name);
				setTimeout(load_family_droplist,1000);
			}

		}
	});

});

$("#created-family-button").click(function(e) {
	e.preventDefault();
	location.reload();
});

$("#reminder-add-button").click(function(e) {
	e.preventDefault();
	reminder_body = $("#reminder-input").val();
	add_reminders(reminder_body);

})

$("#lists-close-button").click(function(e) {
	e.preventDefault();
	reload_list_input();
	$("#family-lists-create-container").hide();
	$("#lists-create-container-button").show();
});

$("#lists-create-container-button").click(function(e) {
	e.preventDefault();
	$("#family-lists-create-container").css('display','flex');
	$(this).hide();
});

$("#lists-create-button").click(function(e) {
	e.preventDefault();
	add_lists();
});

//calendar buttons
$("#event-input-close-button").click(function(e) {
	e.preventDefault();
	// reload_list_input();
	$("#family-event-create-wrapper").hide();
});


});
