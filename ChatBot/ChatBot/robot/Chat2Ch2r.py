#coding: utf-8


import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
from thread import  *




class chat2Ch2r():
    '''
    专用于与ch2r保持持续通讯
    '''

    def __init__(self):
        self.req = ""
        self.count = 0
        self.answer = ""

    def newQuestion(self,req):
        self.req = req
        if self.count == 0:
            start_new_thread(self.chat,())  #开始新线程登录，利用类内变量进行通讯，类之间由回调函数通讯
            self.count += 1


    def getAnswer(self):
        while True:
            if self.answer == "":
                continue
            else:
                break			#等待线程
        return self.answer

    def clear(self):
        self.answer = ""

    def chat(self):
        '''
        cookies还可以提高
        :param ask:
        :return:
        '''
        #登录的主页面
        hosturl = 'http://ch2r.org/Chat/Login'
        #post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
        posturl = 'http://ch2r.org/Chat/Login/In'

        #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        #打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
        h = urllib2.urlopen(hosturl)	#使用cookie

        #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                   'Referer' : 'http://ch2r.org/Chat/Login'}
        #构造Post数据，他也是从抓大的包里分析得出的。
        postData = {
                    'Name' : '111',
                    'Gender' : 'Male',
                    }

        #需要给Post数据编码
        postData = urllib.urlencode(postData)

        #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
        request = urllib2.Request(posturl, postData, headers)
        # print request
        response = urllib2.urlopen(request)
        text = response.read()
        # print text

        while True:             #拒绝重新登陆
            if self.req == "":
                continue

            print "answer: " , self.answer
            #发送新消息 进行对话
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                       'Referer' : '"http://ch2r.org/Chat/CellPhone?Gender=Male&Age=0&GUID=aafc64d30c0741fa8b86e0ed1388d02d&Name=111"'}
            posturl = 'http://ch2r.org/Chat/CellPhone/Process'
            postData = {
                        'RawInput' : self.req,
                        'X-Requested-With' : 'XMLHttpRequest',
                        }

            #需要给Post数据编码
            postData = urllib.urlencode(postData)

            #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
            request = urllib2.Request(posturl, postData, headers)
            # print 'request: ' , request
            response = urllib2.urlopen(request)
            text = response.read()
            print text
            try:
                answer = re.search(".*(`ACTIVE`|`DAILYTALK`|`RECOMMEND`|`NOTFOUND`|`DETAIL`)", text, flags=0).group().replace("`ACTIVE`","").replace("`DAILYTALK`","").replace("`RECOMMEND`","").replace("`NOTFOUND`","").replace("`DETAIL`","")
                self.answer = answer
                self.req = ""

            except Exception:

                self.answer = "亲，别逗我逼啦~~~"
                self.req = ""