#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : import_candidates.py
# @Author: cuijianzhe
# @Date  : 2020/12/24
# @Desc  :

import csv

from django.core.management import BaseCommand
from interview.models import Candidate

#执行命令
#python manager.py import_candidates --path


class Command(BaseCommand):
    help = '从一个CSV文件的内容中读取候选人列表，导入到数据库中'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding="gbk") as f:
            reader = csv.reader(f, dialect='excel', delimiter=';')
            for row in reader:
                # 创建候选人，把属性传进来
                candidate = Candidate.objects.create(
                    username=row[0],
                    city=row[1],
                    phone=row[2],
                    bachelor_school=row[3],
                    major=row[4],
                    degree=row[5],
                    test_score_of_general_ability=row[6],
                    paper_score=row[7]
                )

                print(candidate)