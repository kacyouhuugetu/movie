function login(){

	// 将密码sha256加密后发送
	var password = $('#login_form').find('#password_').val();
	$('#login_form').find('[name="password"]').val(sha256(password));

	$.ajax({
		async : false,
		type : 'post',
		url : $('#login_url').val(),
		dataType : 'json',
		data : $('#login_form').serialize(),
		success : function(data){
			console.log(data)
			if(data.flag == 'SUCCESS'){
				show_message('登录成功，现在跳转至主页面', 2000, function(){
					window.location.href = $('#main_page_url').val();
				});
				
			}
			else{
				show_message(data.msg, 2000);
			}
		}

	});

	return false;

}