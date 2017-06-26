# coding:utf-8
from django.contrib import admin
from pz_skill.models import PzSkill


# Register your models here.
class SkillAdmin(admin.ModelAdmin):
    list_display = ('s_title', 'usr', 's_read', 's_thumb', 's_release_time')
    search_fields = ('s_title', 's_content')
    list_filter = ('s_release_time',)
    date_hierarchy = 's_release_time'
    list_display_links = ('s_title', 'usr', 's_read', 's_thumb', 's_release_time')
    readonly_fields = ('s_title', 'usr', 's_read', 's_thumb', 's_release_time',
                       's_user', 's_content', 's_url')


admin.site.register(PzSkill, SkillAdmin)
