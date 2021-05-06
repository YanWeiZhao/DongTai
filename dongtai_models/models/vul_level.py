#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/4 上午11:54
# software: PyCharm
# project: dongtai-models
from django.db import models


class IastVulLevel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_value = models.CharField(max_length=255, blank=True, null=True)
    name_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_vul_level'
