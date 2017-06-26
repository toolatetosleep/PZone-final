# encoding:utf-8
from __future__ import unicode_literals

from django.db import models

import re

from pz_user.dao import get_user_name


# Create your models here.
class PzComment(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_user_give = models.IntegerField()
    c_user_recive = models.IntegerField()
    c_category = models.IntegerField()
    c_item_id = models.IntegerField()
    c_com_recive = models.IntegerField()
    c_content = models.CharField(u'评论内容', max_length=1000)
    c_time = models.DateTimeField(u'发布时间')
    c_read = models.IntegerField()

    def content(self):
        html = self.c_content
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html)
        return dd[:10]

    content.short_description = u'评论内容'

    def user_give(self):
        return get_user_name(self.c_user_give)

    user_give.short_description = u'发布人'

    def user_recv(self):
        return get_user_name(self.c_user_recive)

    user_recv.short_description = u'接收人'

    def category(self):
        cat = "???"
        if int(self.c_category) == 1:
            cat = "摄影头条"
        elif int(self.c_category) == 2:
            cat = "摄影技巧"
        elif int(self.c_category) == 3:
            cat = "摄影佳作"
        elif int(self.c_category) == 4:
            cat = "摄影器材"
        return cat

    category.short_description = u'评论板块'

    def is_reply(self):
        flag = True
        if int(self.c_com_recive) == 0:
            flag = False
        return flag

    is_reply.admin_order_field = 'c_com_recive'
    is_reply.short_description = u'是否回复其他评论'
    is_reply.boolean = True

    def read(self):
        if int(self.c_read) == 0:
            return False
        else:
            return True

    read.admin_order_field = 'c_read'
    read.short_description = u'是否已读'
    read.boolean = True

    class Meta:
        managed = False
        db_table = 'pz_comment'
        ordering = ['c_time']
        verbose_name = '全站评论'
        verbose_name_plural = '全站评论'
