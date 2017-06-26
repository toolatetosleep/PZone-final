# coding:utf-8
from django.contrib import admin
from pz_topic.models import PzTopic


# Register your models here.


class TopicAdmin(admin.ModelAdmin):
    list_display = ('t_title', 'usr', 't_read', 't_thumb', 't_release_time')
    search_fields = ('t_title', 't_content')
    list_filter = ('t_release_time',)
    date_hierarchy = 't_release_time'
    list_display_links = ('t_title', 'usr', 't_read', 't_thumb', 't_release_time')
    readonly_fields = ('t_title', 'usr', 't_read', 't_thumb', 't_release_time',
                       't_user', 't_content', 't_url')

admin.site.register(PzTopic, TopicAdmin)
