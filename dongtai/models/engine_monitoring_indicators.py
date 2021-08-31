######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : engine_monitoring_indicators
# @created     : Wednesday Aug 25, 2021 14:51:16 CST
#
# @description :
######################################################################

from django.db import models
from dongtai.utils.settings import get_managed


class IastEnginMonitoringIndicators(models.Model):
    key = models.CharField(max_length=100,
                           blank=True,
                           default='',
                           null=False,
                           unique=True)
    name = models.CharField(max_length=100, blank=True, default='', null=False)

    class Meta:
        managed = get_managed()
        db_table = 'engine_monitoring_indicators'
