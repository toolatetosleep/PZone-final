# encoding:utf-8
from __future__ import unicode_literals

from django.db import models

from pz_user.dao import get_user_name


# Create your models here.
class PzEquipment(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_user = models.IntegerField()
    e_title = models.CharField(u'文章标题', max_length=255)
    e_content = models.CharField(max_length=5000)
    e_release_time = models.DateTimeField(u'发布时间')
    e_url = models.CharField(max_length=255)
    e_read = models.IntegerField(u'阅读数')
    e_thumb = models.IntegerField(u'支持数')

    def usr(self):
        return get_user_name(self.e_user)

    usr.short_description = u'用户'

    class Meta:
        managed = False
        db_table = 'pz_equipment'
        ordering = ['e_release_time']
        verbose_name = '摄影器材'
        verbose_name_plural = '摄影器材'


class PzComment(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_user_give = models.IntegerField()
    c_user_recive = models.IntegerField()
    c_category = models.IntegerField()
    c_item_id = models.IntegerField()
    c_com_recive = models.IntegerField()
    c_content = models.CharField(max_length=1000)
    c_time = models.DateTimeField()
    c_read = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pz_comment'
