from __future__ import unicode_literals

from django.db import models


class PzCacheTable(models.Model):
    cache_key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pz_cache_table'


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


class PzEquipment(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_user = models.IntegerField()
    e_title = models.CharField(max_length=255)
    e_content = models.CharField(max_length=5000)
    e_release_time = models.DateTimeField()
    e_url = models.CharField(max_length=255)
    e_read = models.IntegerField()
    e_thumb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pz_equipment'


class PzPicture(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_user = models.IntegerField()
    p_title = models.CharField(max_length=255)
    p_content = models.CharField(max_length=5000)
    p_release_time = models.DateTimeField()
    p_url = models.CharField(max_length=255)
    p_read = models.IntegerField()
    p_thumb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pz_picture'


class PzSkill(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_user = models.IntegerField()
    s_title = models.CharField(max_length=255)
    s_content = models.CharField(max_length=5000)
    s_release_time = models.DateTimeField()
    s_url = models.CharField(max_length=255)
    s_read = models.IntegerField()
    s_thumb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pz_skill'


class PzTopic(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_user = models.IntegerField()
    t_title = models.CharField(max_length=255)
    t_content = models.CharField(max_length=5000)
    t_release_time = models.DateTimeField()
    t_url = models.CharField(max_length=255)
    t_read = models.IntegerField()
    t_thumb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pz_topic'


class PzUser(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_username = models.CharField(max_length=255)
    u_password = models.CharField(max_length=255)
    u_credit = models.IntegerField()
    u_avatar = models.CharField(max_length=255)
    u_autograph = models.CharField(max_length=255)
    u_last_login_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pz_user'
