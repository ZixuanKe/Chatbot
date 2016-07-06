#coding: utf-8

class Message():
    '''
    定义消息体，消息头
    '''
    def __init__(self,head,body):
        self.head  = head   #数据大小，数据类型，即定义一份协议。，
        self.body  = body   #应该转换为二进制流传送

