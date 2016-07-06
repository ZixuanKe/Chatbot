#coding:utf-8

import json
from Message import *

'''

        head        body
        message     (string)
        Login       Null
        Logout      Null
        alive       Null
        server      (string)
        file-request   (file-name: string)
        file-refuse    (file-name: string)
        file-content   (file-content: binary)
        file-accept    Null
        file-ok        (file-name: string)

'''


class Transfer():
    '''
    定义各种数据类型转换
    1、String的解码，译码 使用json封装为流（已经序列化为流）
    '''
    def __init__(self):
        pass

    def encodeMessage(self,message):
        return json.dumps(message,default=self.messageToDict)    #封装为json形式发出，需要作出一些自定义内容

    def decodeMessage(self,message):
        print message
        return json.loads(message,object_hook=self.dictToMessage)


    def messageToDict(self,message):    #自行封装并解码编码消息
        d = {'head': message.head,
             'body': message.body
             }
        return d

    def dictToMessage(self,d):


        head =  d.pop('head')
        body = d.pop('body')
        return Message(head,body)

