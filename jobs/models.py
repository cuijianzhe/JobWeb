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

    class Meta:
        verbose_name = u'职位'
        verbose_name_plural = u'职位列表'
    def __str__(self):
        return self.job_name


class Resume(models.Model):
    # Translators: 简历实体的翻译
    username = models.CharField(max_length=135, verbose_name='姓名')
    applicant = models.ForeignKey(User, verbose_name="申请人", null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=135, verbose_name='城市')
    phone = models.CharField(max_length=135, verbose_name='手机号码')
    email = models.EmailField(max_length=135, blank=True, verbose_name='邮箱')
    apply_position = models.CharField(max_length=135, blank=True, verbose_name='应聘职位')
    born_address = models.CharField(max_length=135, blank=True, verbose_name='生源地')
    gender = models.CharField(max_length=135, blank=True, verbose_name='性别')
    picture = models.ImageField(upload_to='images/', blank=True, verbose_name='个人照片')
    attachment = models.FileField(upload_to='file/', blank=True, verbose_name='简历附件')

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=135, blank=True, verbose_name='本科学校')
    master_school = models.CharField(max_length=135, blank=True, verbose_name='研究生学校')
    doctor_school = models.CharField(max_length=135, blank=True, verbose_name=u'博士生学校')
    major = models.CharField(max_length=135, blank=True, verbose_name='专业')
    degree = models.CharField(max_length=135, choices=DEGREE_TYPE, blank=True, verbose_name='学历')
    created_date = models.DateTimeField(verbose_name="创建日期", default=datetime.now)
    modified_date = models.DateTimeField(verbose_name="修改日期", auto_now=True)

    # 候选人自我介绍，工作经历，项目经历
    candidate_introduction = models.TextField(max_length=1024, blank=True, verbose_name=u'自我介绍')
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name=u'工作经历')
    project_experience = models.TextField(max_length=1024, blank=True, verbose_name=u'项目经历')

    class Meta:
        verbose_name = u'简历'
        verbose_name_plural = u'简历列表'

    def __str__(self):
        return self.username
