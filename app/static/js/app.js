jQuery(document).ready(function(){

	// $("#content_join-family").not($("#THIS")).click(function(e) {
	// 	console.log('click');
	// 	$('.cursor-button').remove();
	// })
$("#families-table tr").click(function(e) {
    console.log("row click");
    var num = Math.floor((Math.random() * 10) + 1);
    var div = $('<div class="cursor-button">Send Join Request</div>');
    container = $("#content_join-family");

    $('.cursor-button').remove();

    div.appendTo(container).offset({ top: e.pageY, left: e.pageX });
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

})