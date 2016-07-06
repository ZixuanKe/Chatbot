				var inputElement = document.getElementById("sendFile");
				var file = inputElement.files[0];
				var reader = new FileReader();	//准备读取文件
				reader.readAsDataURL(file);//文件读取完毕后该函数响应
				
		
				reader.onload = function loaded(evt) {
					
					//以下将字符串切割后再上传,一次512byte
					var theFile = (evt.target.result);
					var fileLength =  (evt.target.result).length;
					
					var fileFragemnt = Math.ceil( fileLength/512 ); //计算需要的片段数

					//稍后可以对文件过小时进行直接显示处理
				
					var start = 0;
					for (i=1; i< fileFragemnt; i++) {	//最后一个片段不定长，另外发送
												
					if (clickSend == true){

									var messg = {
									head: "message",
									body: msg
									};
							websocket.send( JSON.stringify(messg) );		
							clickSend = false;
						
					}
					
						var messg = {	// 最后一包
						head: "file-content:" + start,
						body: theFile.slice(start,( i * 512))	//小包发送不影响其他信息发送
						};
					//发送文件
					
					websocket.send(JSON.stringify(messg))
					
					
					
					start = start + 512;
					//跳转到django下载页面，交给后端处理
					
					}	//for循环结束
					
					
					//	发送最后一个包	
					var messg = {
						head: "file-content:" + start,
						body: theFile.slice(start,fileLength-1)
						};
					//发送文件
					websocket.send(JSON.stringify(messg))

				
					
						} //onload
					