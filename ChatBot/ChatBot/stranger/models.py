#coding: utf-8


from django.db import models

# Create your models here.

#app属于project project含有很多个app以及配置 app则只是程序
#使用python代码进行数据库操作，底层SQL语句被封装，通过python进行交互


#   无需显示定义主键，自动创建ID类
class history(models.Model):

    '''
    Publisher表
    '''
    # id = models.IntegerField(max_length=11)
    user_A = models.CharField(max_length=255)
    user_B = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now=True)
    message_type = models.CharField(max_length=255)
    message_content = models.CharField(max_length=255)
