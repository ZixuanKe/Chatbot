# coding: utf-8

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    print " request method: " , request.method
    if request.method == "GET":
        print "GET method's request string: ",request.GET
    elif request.method == "POST":
        print "POST CONTENT: " , request.POST
    else:
        pass #大概可有，前端浏览器构造报文细节仍然需要回顾（书本与同志）


    return render_to_response("index.html")