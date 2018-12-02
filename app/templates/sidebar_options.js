// CONTAINS ADDRESSES AND NAMES FOR SIDEBAR ITEMS

// {
// 	sidebar panel: [
// 		{option name : option content id}
// 	]
// }


sidebar_options = {
	'main-panel' : [
		{
			'name' : 'Join Requests',
			'link' : 'join-requests',
			funct : function() {
				console.log("FUNCTION WORKS!");
				query_join_requests();
			} 
		},
		{'Invite Member' : 'no-family'}
	]
}