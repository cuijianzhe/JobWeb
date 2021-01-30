#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : local.py
# @Author: cuijianzhe
# @Date  : 2021/1/8
# @Desc  :

from .base import *
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

## 务必修改以下值，确保运行时系统安全:
SECRET_KEY = "8t!nm@z7wk5*z!tpb^#lj+9bk*vi^0ja8vq*3al)w==2qy=d(f"

## 如果仅使用数据库中的账号，以下 LDAP 配置可忽略
## 替换这里的配置为正确的域服务器配置，同时可能需要修改 base.py 中的 LDAP 服务器相关配置:
LDAP_AUTH_URL = "ldap://172.16.16.4:389"
LDAP_AUTH_CONNECTION_USERNAME = "cuijianzhe"
LDAP_AUTH_CONNECTION_PASSWORD = "598941324"

INSTALLED_APPS += (
    # other apps for production site
)


## 钉钉群的 WEB_HOOK， 用于发送钉钉消息
# DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxxxx"