function register(){

	$('#register_form').find('#password_').removeClass('error_field');
	$('#register_form').find('[name]').removeClass('error_field');
	
	var result = verify_form();

	// 验证成功，提交表单
	if(result.flag=='SUCCESS'){
		$.ajax({
			async : false,
			type : 'post',
			url : $('#register_url').val(),
			dataType : 'json',
			data : $('#register_form').serialize(),
			success : function(data){
				fail_field = data.fail_field;
				msg = data.msg;

				if(fail_field){

					$('#register_form').find('[name="field"]'.replace('field', fail_field)).addClass('error_field');

					show_message(msg, 2000);
				}
				else{

					show_message('注册成功，现在跳转至登录页面', 2000, function(){
						window.location.href = $('#to_login_url').val();
					})


				}
			}

		});
	}
	// 验证失败，显示错误信息
	else{

		$('#register_form').find('#password_').addClass('error_field');
		show_message(result.message, 2000);
	}

	return false;
}


function verify_form(){

	var password = $('#register_form').find('#password_').val();

	if(!verify_password(password, true)){
		return {'flag': 'FAIL', 'message': '密码是8位到20位的由数字、字母或下划线组成的字符串'}
	}

	// 通过验证，利用SHA256加密密码
	$('#register_form').find('[name="password"]').val(sha256(password));

	return {'flag' : 'SUCCESS'};

}

