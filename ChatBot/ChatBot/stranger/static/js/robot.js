	
	var myIp = "192.168.17.1"

	 function init() {
        output = document.getElementById("historyMsg");
    }
	

    function writeToScreen(message) {
        var pre = document.createElement("p");
        pre.style.wordWrap = "break-word";			
        pre.innerHTML = message;
        output.appendChild(pre);
    }

	

	function sendButton(){
		var messageInput = document.getElementById('messageInput');
		msg = messageInput.value;
		messageInput.value = '';
		messageInput.focus();
		writeToScreen('<span style="color: black;">YOU: '+ msg +'</span>');	

		$.ajax({
			method:'get',
			url:"http://" + myIp + ":8000/index/robot/chatting/",
			data:{
				message:msg
			},
			success:function(res){
		writeToScreen('<span style="color: blue;">Robot: '+ res +'</span>');	
			}
		});
		//if (msg.trim().length != 0) {
	}
	
	
		
		//myAjax({
		//	method:'POST',
		//	url:'http://127.0.0.1:8000/index/robot/chatting
		//	contentType:'json',
		//	data:JSON.stringify({
		//		message:msg
		//	}),
		//	success:function(res){
		///		console.log(res);
		//	}
		//});
		
    window.addEventListener("load", init, false);
	//前端未写
	
	
	
	//无需重新声明script
	//文件另外使用http方式上传
	//django解析post数据不完整
	//解析post报文，保存二进制数据即可，可以考虑在编码
