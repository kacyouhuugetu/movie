function search_movie(search_key){

	if(search_key){
		$('#search_movie_form').find('name=[search_key]').val(search_key);
	}

	var result = null;

	$.ajax({
		async : false,
		type : 'get',
		url : $('#douban_movie_search_movie_url').val(),
		dataType : 'json',
		data : $('#search_movie_form').serialize(),
		success : function(data){
			result = data;
		}
	});

	return result;

}

function to_movie_detail(id){
	window.location.href = $('#douban_movie_movie_detail_url').val() + '/' + id;
}