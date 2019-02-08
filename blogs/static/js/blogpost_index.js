$("#likes").click(function(){
	var blogid;
	blogid = $(this).attr("data-blogid");
	$.get('/like_post/', {blogpost_id: blogid}, function(data){
		$('#like_count').html(data);

	});
});