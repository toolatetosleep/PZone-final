# coding:utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class PzUser(models.Model):
    u_id = models.AutoField(u'用户ID', primary_key=True)
    u_username = models.CharField(u'用户名', max_length=255)
    u_password = models.CharField(max_length=255)
    u_credit = models.IntegerField(u'用户积分')
    u_avatar = models.CharField(max_length=255)
    u_autograph = models.CharField(max_length=255)
    u_last_login_time = models.DateTimeField(u'最后登入时间')

    class Meta:
        managed = False
        db_table = 'pz_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


class PzComment(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_user_give = models.IntegerField()
    c_user_recive = models.IntegerField()
    c_category = models.IntegerField()
    c_item_id = models.IntegerField()
    c_com_recive = models.IntegerField(default=0)
    c_content = models.CharField(max_length=1000)
    c_time = models.DateTimeField()
    c_read = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pz_comment'
