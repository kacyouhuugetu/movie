var modal_html_template = null;
$(function(){

	modal_html_template = $('#modal-template').html();
	$('#modal-template').remove();

})

// 打开弹窗
function open_modal(settings){

	var title = settings.title;
	var body = settings.body;
	var time = settings.time;
	var closebtn = settings.closebtn;
	var open = settings.open;
	var close = settings.close;
	var id = 'modal_' + (Math.floor(Math.random()*1000));

	var modal_html = modal_html_template;

	if(!body){
		body = ''
	}


	modal_html = modal_html.replace(new RegExp('{modal_id}','g'), id);
	modal_html = modal_html.replace(new RegExp('{modal_title}','g'), title);
	modal_html = modal_html.replace(new RegExp('{modal_body}','g'), body);

	$('body').append(modal_html);

	if(!closebtn){
		$('#'+id).find('.modal-footer').remove();
	}
	if(!title){
		$('#'+id).find('.modal-header').remove();
	}

	if(open){
		$('#'+id).on('shown.bs.modal', function (e) {
			open();
		})
	}
	if(close){
		$('#'+id).on('hidden.bs.modal', function (e) {
			close();
		})
	}

	$('#'+id).modal('show');
	if(time){
		$('#'+id).on('shown.bs.modal', function (e) {
			window.setTimeout(function(){close_modal(id)}, time);
		})
	}

	return id;

}


// 关闭弹窗
function close_modal(modal_id){

	$('#'+modal_id).modal('hide');
	$('#'+modal_id).on('hidden.bs.modal', function (e) {
		$('#'+modal_id).remove();
	})

}


function show_message(message, time, end){
	if(!time){
		time = 2000;
	}

	open_modal({
		body : message,
		time : time,
		close : end
	});
}