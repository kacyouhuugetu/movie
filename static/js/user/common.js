var username_pattern = '^\\w{8,20}$';
var password_pattern = '^[a-zA-Z0-9_]{8,20}$';
var phone_pattern = '^\\d{11}$';
var email_address_pattern = '^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$';


function verify_username(string, require){
	if(!string){
		return require?false:true;
	}

	if(string.match(username_pattern)){
		return true;
	}
	else{
		return false;
	}

}
function verify_password(string, require){
	if(!string){
		return require?false:true;
	}

	if(string.match(password_pattern)){
		return true;
	}
	else{
		return false;
	}

}
function verify_phone(string, require){
	if(!string){
		return require?false:true;
	}

	if(string.match(phone_pattern)){
		return true;
	}
	else{
		return false;
	}

}
function verify_email_address(string, require){
	if(!string){
		return require?false:true;
	}

	if(string.length>100){
		return false;
	}

	if(string.match(email_address_pattern)){
		return true;
	}
	else{
		return false;
	}
	
}

