#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
from models import *
import datetime
import  re
from process.Transfer import *
from django.http import StreamingHttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from Chat2Ch2r import chat2Ch2r



#成功移植为json
#下一步传输 表情 图片 文件
import base64
import sys
reload(sys)


sys.setdefaultencoding('utf-8')

ch2r = chat2Ch2r()


@csrf_exempt
def robot(request):

    return render_to_response("robot.html")   #直接返回标签方便写会


@csrf_exempt
def answerFromCh2r(request):

    '''
    接受前端post信息
    返回回复信息 并且让前端显示
    :param request:
    :return:
    '''
    #尝试 第一次问句时 使用新进程登录，随后与该进程通讯，考虑回调方法以互相通知
    print request.method
    print "POST: ",request.POST
    print "GET: ",request.GET
    print "FILES: ",request.FILES
    question = request.GET['message']

    ch2r.newQuestion(question)          #通知有新问题
    message = ch2r.getAnswer()          #获取新结果
    ch2r.clear()


    print "respond: ",message

    return HttpResponse(message)   #直接返回标签方便写会




