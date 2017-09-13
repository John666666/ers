/**
 * 登录界面JS
 */
function login(){
	var username = $("#username").val();
	var password = $("#password").val();
	
	var formData = {"client_id": username, "pwd": password};
	
	$.post('login', formData, function(retData){
		if(!retData) {
			alert('登录出错，请稍后重试!');
			return;
		}
		if(retData.code == '200') {
			window.location.href = 'index';
		} else {
			alert(retData.message);
		}
	},'json');
};

$("#password").keypress(function(e){
	if(e.which == 13) {
		login();
	}
});