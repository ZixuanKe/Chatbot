#coding: utf-8

from django.shortcuts import render_to_response
from thread import *
from gevent import pywsgi, sleep
from geventwebsocket.handler import WebSocketHandler
from models import *
import datetime
import  re
from process.Transfer import *
from django.http import StreamingHttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse




#成功移植为json
#下一步传输 表情 图片 文件
import base64
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

import socket
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
print myname
print myaddr


clienting = []     #未分配
oppClient = {}     #分配结果
#多线程共享变量  默认有GIL全局锁


class WebSocketApp(object):
    '''Send random data to the websocket'''

    def __call__(self, environ, start_response):        #重载()运算

        global clienting
        global oppClient
        global file_name
        self.dead = False
        print "YES!!!!!"
        ws = environ['wsgi.websocket']  #接受wensocket消息，并且send回复
        print "Remote_ADDR ", environ ['REMOTE_ADDR']
        print "Remote_PORT ", environ['REMOTE_PORT']
        print "PATH_INFO: ",  environ["PATH_INFO"]

        remote_point = str(environ['REMOTE_ADDR']) + ":" + str(environ['REMOTE_PORT'])


        clienting.append(ws)     # 将 websock信息放在client上

        ws.send(Transfer().encodeMessage(Message("server","You are suceessful connected to the server!")))
        ws.send(Transfer().encodeMessage(Message("server","Searching someone to talk with you !")))

        print "send server!"
        #多余两个未分配时，选定陌生人

        while True: #分配，2、此处刷新，应该使用cookie记住身份


            print "send!"
            ws.send(Transfer().encodeMessage(Message("alive","")))   #确认对方是否刷新
            temp = Transfer().decodeMessage(ws.receive())

            print temp.head
            if temp.head not in  ["alive","Login"]:
                print "The ws has been dead!"
                clienting.remove(ws)
                self.dead = True
                break

            print "alive!"



            print "length of clenting: " , len(clienting)
            print "length of oppClient: " , len(oppClient)

            if len(oppClient) >= 2 and len(clienting) == 0:
                break

            sleep(1)
            if len(clienting) < 2:
                continue

            else:
                print "yes"
                self.mutaing(ws)
                break


        #gevent对多线程有限制,要配合顶层设计
        while True:

            if self.dead == True:
                break

            message = ws.receive()

            if message is None:
                print "client leave, "      #离开后数据结构作相应改变
                oppClient[ws].send(Transfer().encodeMessage(Message("Logout","")))
                del oppClient[ws]
                break


            message = Transfer().decodeMessage(message)   #解json编码

            print message.head
            if message.head == "Login" or message.head == "alive":         #关系要搞清楚 服务器 客户端 建议画出具体图像解决
                print "The Opp Login"
                oppClient[ws].send(Transfer().encodeMessage(Message("server","You are now talking with a stranger! Say Hi!")))
                continue
            if message.head == "Logout":
                print "The Opp Logout"
                ws.send(Transfer().encodeMessage(Message("server","Stranger has disconnected")))
                del oppClient[ws]    #删掉已经分配的
                break

            if message.head == "message":       #普通信息，转发并记录到数据库
                #print "Got message: %s" %message.body

                print datetime.datetime.now()   # 当前时间
                #后期可以考虑不直接写入数据库，由脚本将日志写入数据库
                # history.objects.create(user_A=remote_point,message_type=message.head,message_content=message.body)
                oppClient[ws].send(Transfer().encodeMessage(Message("message",message.body)))
                    #给对应的人发送消息即可

            if message.head == "file-refuse":
                oppClient[ws].send(Transfer().encodeMessage(Message(message.head,message.body)))

            if message.head == "file-accept":
                oppClient[ws].send(Transfer().encodeMessage(Message(message.head,message.body)))

            if message.head == "file-request":
                file_name = message.body            #暂存文件名
                oppClient[ws].send(Transfer().encodeMessage(Message(message.head,message.body)))

            if message.head == "file-ok":           #上传完成信号，通知对端开始启动下载
                file_name = message.body            #暂存文件名
                oppClient[ws].send(Transfer().encodeMessage(Message(message.head,message.body)))

            if message.head == "file-ok+":           #上传完成信号，通知对端开始启动下载
                file_name = message.body            #暂存文件名
                oppClient[ws].send(Transfer().encodeMessage(Message(message.head,message.body)))

            if "file-content" in message.head:  #分段接受数据


                file_object = open(file_name, 'a')  #base64可以直接写入,追加用a
                print message.head
                print file_name

                start = re.sub("[^0-9]", "",str(message.head))  #只保留数字
                print start
                print message.body

                #file_object.seek(int(start))  #从start的位置开始追加
                file_object.write(  message.body )   #存储二进制数据，接受到的编码均为base64
                file_object.close( )


    def mutaing(self,ws):

            ws1 = clienting[1]
            oppClient[ws] = ws1
            oppClient[ws1] = ws

            clienting.remove(ws1)
            clienting.remove(ws)

def listnning():            #Sever端监听函数
    try:
        server = pywsgi.WSGIServer((myaddr, 10), WebSocketApp(),
        handler_class=WebSocketHandler)     #建立websocket监听端口
        print "Listnning 127.0.0.1:10"
        server.serve_forever()
    except Exception:
        print "The IP:Port has been in bind"

def stranger(request):
    #进入首页 加入websocket 开始监听
    print "Recive Request", request
    start_new_thread(listnning,())      #不应多次listen

    return render_to_response("stranger.html")


def stranger_history(request):

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        user_ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        user_ip = request.META['REMOTE_ADDR']        #获取用户IP

    records = history.objects.filter(user_A__contains=user_ip)
    print user_ip
    print records

    list = []
    for i in records:
        list.append( [str(i.id) , str(i.user_A) , str(i.time) , str(i.message_type) , str(i.message_content)] )
    print list
    return render_to_response("stranger_history.html",{'records':list})


#1、如何显示在某处(添加某行)
#2、如何绑定按钮事件
#3、如何发送Ip Port
#4、增加断开/连接 键
#5、之后沿用socketserver即可
#6、模式选择）

def big_file_download(request):
    # do something...

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")      #需要限定打开方式 二进制
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    file_name = request.GET['file']		# 通过file方法直接获得文件名，需要提供文件名进行下载
    response = HttpResponse(readFile(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + file_name
    return response

@csrf_exempt
def file_receive(request):

    print request.method
    print request.FILES['upload']
    print str(request.FILES['upload'])
    handle_uploaded_file( request.FILES['upload'],str(request.FILES['upload']) )
    return render_to_response("receive.html")


def handle_uploaded_file(f,name):   # 成功分块保存到服务器
    file_name = name

    try:
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception, e:
        print e

    return file_name

#ws 通知对端
#对端接受后跳入下载页面


# 1、完成发送file-ok信号
# 2、file-ok后查询相应文件进行下载