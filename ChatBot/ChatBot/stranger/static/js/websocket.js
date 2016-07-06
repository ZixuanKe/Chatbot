
	var myIp = "192.168.17.1"
    var wsUri ="ws://" + myIp + ":10"; 	//公网IP
    var output;
	var clickSend;
	var accept = 0;
    function init() {
        output = document.getElementById("historyMsg");
        testWebSocket();
    }
	
    function testWebSocket() {		
        websocket = new WebSocket(wsUri);
        websocket.onopen = function(evt) {
            onOpen(evt)				
        };
        websocket.onclose = function(evt) {
            onClose(evt)			
        };
        websocket.onmessage = function(evt) {
            onMessage(evt)			
        };
        websocket.onerror = function(evt) {
            onError(evt)			
        };
    }

    function onOpen(evt) {
        writeToScreen("CONNECTED TO SERVER");
				var messg = {
			head: "Login",
			body: ""
		};
		
		websocket.send(JSON.stringify(messg));
	   //setInterval("heartBeat()","1000")


    }

    function onClose(evt) {
        //writeToScreen("DISCONNECTED FROM SERVER");
    }

    function onMessage(evt) {
		clickSend = false;
		if(JSON.parse(evt.data).head == "Logout"){		
			writeToScreen('<span style="color: black;">SERVER: '+ "STRANGER has disconnected" +'</span>');
			var messg = {
			head: "Logout",
			body: ""
			};
		
		websocket.send(JSON.stringify(messg));
		}
		
		else if(JSON.parse(evt.data).head == "alive"){	
						var messg = {
			head: "alive",
			body: ""
		};
			websocket.send(JSON.stringify(messg))
		}
		else if(JSON.parse(evt.data).head == "server"){	
			
			
			writeToScreen('<span style="color: black;">SERVER: '+ JSON.parse(evt.data).body +'</span>');
			
		}
		
		else if(JSON.parse(evt.data).head == "file-request"){
			
			
			if(confirm('Stranger would like to send you the file: \n' + JSON.parse(evt.data).body + "\nWould you like to accept it?")){
				//如果接受
				
			var messg = {
			head: "file-accept",
			body: JSON.parse(evt.data).body
			};
			websocket.send(JSON.stringify(messg))	
			writeToScreen('<span style="color: red;">SERVER: '+ '请耐心等候对方上传文件~~' +'</span>');
			writeToScreen('<span style="color: red;">SERVER: '+ '上传完成后您将自动跳入下载页面' +'</span>');
			writeToScreen('<span style="color: red;">SERVER: '+ '请勿阻止弹出对话框' +'</span>');
			accept = 1;
			var messg = {
			head: "file-ok+",
			body: JSON.parse(evt.data).body
			};
			websocket.send(JSON.stringify(messg))	
			
			} //对应同意的if
			
			
			else{
				//如果拒绝,向服务器发送拒绝消息
			var messg = {
			head: "file-refuse",
			body: JSON.parse(evt.data).body
			};
			websocket.send(JSON.stringify(messg))
			writeToScreen('<span style="color: red;">SERVER: '+ '您已拒绝对方文件发送请求' +'</span>');
			accept = -1;

				
			}//对应拒绝
			
		}
		
		
			else if(JSON.parse(evt.data).head == "file-ok+"){
				
			//收到接受信号
			//提醒对方重新判断
			var messg = {			//发送完成
				head: "file-ok",
				body: document.getElementById('upload').files[0].name
			};
			websocket.send( JSON.stringify(messg) );	//告诉服务器即将 上传的文件，服务器发送确认消息	
					
	
			}
			
			
			

			else if(JSON.parse(evt.data).head == "file-ok"){
			
			
			var file_name = JSON.parse(evt.data).body
			//get方法 file = 
			//eg. http://127.0.0.1:8000/index/stranger/filedownload/?file=GBDT.docx
			
				console.log(accept);
				if (accept == 1){
				var a = document.createElement("a");
				document.body.appendChild(a);
				a.href = "http://" + myIp + ":8000/index/stranger/filedownload/?file=" + file_name; //url 是你得到的连接
				a.target = '_new'; //指定在新窗口打开
				a.click();
				document.body.removeChild(a);
				accept = 0;
				}
				if(accept == -1){
					accept = 0;		//拒绝接受均恢复 0：未选择 1：接受 -1：拒绝
				}


			} //对应上传完成的if
		
		
		else if(JSON.parse(evt.data).head == "file-refuse"){	//收到拒绝消息
			
			writeToScreen('<span style="color: red;">SERVER: '+ '陌生人拒绝接受你要发送的文件 : ' + JSON.parse(evt.data).body +'</span>');
			accept = -1;
		}
		
		else if(JSON.parse(evt.data).head == "file-accept"){	//收到拒绝消息
			
			writeToScreen('<span style="color: red;">SERVER: '+ '陌生人接受了你发送文件 : ' + JSON.parse(evt.data).body + ' 的请求' +'</span>');
			accept = 1;
		
		
		}
		else{		
		writeToScreen('<span style="color: red;">STRANGER: '+ JSON.parse(evt.data).body +'</span>');
       
		}
    }

    function onError(evt) {
			writeToScreen('<span style="color: red;">ERROR: Please Refresh The WebSite</span> ');    
			}

    function doSend(message) {
			writeToScreen('<span style="color: blue;">YOU: '+ message +'</span>');
			var messg = {
			head: "message",
			body: message
		};
        websocket.send( JSON.stringify(messg) );		
		clickSend = false;
    }

    function writeToScreen(message) {
        var pre = document.createElement("p");
        pre.style.wordWrap = "break-word";			
        pre.innerHTML = message;
        output.appendChild(pre);
    }

	
	
	function handleFiles(){	//处理选中的文件
	//获取首个选中文件的文件名
	var messg = {
			head: "file-request",
			body: document.getElementById('upload').files[0].name
		};
        websocket.send( JSON.stringify(messg) );	//告诉服务器即将 上传的文件，服务器发送确认消息	

		
	　if(window.FormData) {　
		　　　　var formData = new FormData();
		　　　　// 建立一个upload表单项，值为上传的文件
		　　　　formData.append('upload', document.getElementById('upload').files[0]);
			//formData.append('upload', 'afrberb');
		　　　　var xhr = new XMLHttpRequest();
		　　　　xhr.open('POST',"http://" + myIp + ":8000/index/stranger/filerecive/");
		
		　　　　// 定义上传完成后的回调函数
		　　　　xhr.onload = function () {
		　　　　　　if (xhr.status === 200) {
				accept = 0;
		　　　　　　} else {
		　　　　　　　　console.log('出错了');
		　　　　　　}
		　　　　};
		　　　　xhr.send(formData);
		　　xhr.upload.onprogress = function (event) {
　　　　		if (event.lengthComputable) {
　　　　　　		var complete = (event.loaded / event.total * 100 | 0);
　　　　　	　	var progress = document.getElementById('uploadprogress');
　　　　　　		progress.value = progress.innerHTML = complete;
　　　	　}
			if(complete == 100){
				alert("上传成功！");
					
			var messg = {			//发送完成
				head: "file-ok",
				body: document.getElementById('upload').files[0].name
			};
			websocket.send( JSON.stringify(messg) );	//告诉服务器即将 上传的文件，服务器发送确认消息	
					
			}	//对应上传完成的if
　　};
		　　}
	
	}
	
	function sendButton(){
		var messageInput = document.getElementById('messageInput');
		msg = messageInput.value;
		messageInput.value = '';
		messageInput.focus();
		
		//if (msg.trim().length != 0) {
		doSend(msg); //把消息发送到服务器
	}
	
    window.addEventListener("load", init, false);
	
		


	
	
	//无需重新声明script
	//文件另外使用http方式上传
	//django解析post数据不完整
	//解析post报文，保存二进制数据即可，可以考虑在编码

	

			