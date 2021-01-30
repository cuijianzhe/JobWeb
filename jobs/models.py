from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

# 候选人学历
DEGREE_TYPE = ((u'本科', u'本科'), (u'硕士', u'硕士'), (u'博士', u'博士'))

JobTypes = [
    (0,'产品类'),
    (1,'技术类'),
    (2,'运营类'),
    (3,'设计类'),
]
cities = [
    (1,'北京'),
    (2,'上海'),
    (3,'广州'),
    (4,'深圳')
]

class Job(models.Model):  #这个model是继承的Django的model
    job_type = models.SmallIntegerField(blank=False,choices=JobTypes,verbose_name='职位类别')
    job_name = models.CharField(max_length=250,blank=False,verbose_name='职位名称')
    job_city = models.SmallIntegerField(blank=False,choices=cities,verbose_name='工作地点')
    job_responsibility = models.TextField(max_length=2014,verbose_name='工作职责')
    job_requirement = models.TextField(max_length=1024,blank=False,verbose_name='职位要求')
    creator = models.ForeignKey(User,verbose_name='创建人',null=True, on_delete=models.SET_NULL)   #User的外键引用
    create_date = models.DateTimeField(verbose_name='创建日期',default=datetime.now)
    modified_date = models.DateTimeField(verbose_name='修改时间',default=datetime.now)