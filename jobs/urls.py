#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: cuijianzhe
# @Date  : 2020/12/10
# @Desc  :

from django.conf.urls import url
from jobs import views
from django.urls import path

urlpatterns = [
    #职位列表
    url(r"^joblist",views.joblist,name='joblist'),
    #职位详情
    url(r"^job/(?P<job_id>\d+)/$",views.detail,name='detail'),
    #提交简历
    path('resume/add/',views.ResumeCreateView.as_view(),name='resume-add')
]