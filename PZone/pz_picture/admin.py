# coding:utf-8
from django.contrib import admin
from pz_picture.models import PzPicture


# Register your models here.

class PictureAdmin(admin.ModelAdmin):
    list_display = ('p_title', 'usr', 'p_read', 'p_thumb', 'p_release_time')
    search_fields = ('p_title', 'p_content')
    list_filter = ('p_release_time',)
    date_hierarchy = 'p_release_time'
    list_display_links = ('p_title', 'usr', 'p_read', 'p_thumb', 'p_release_time')
    readonly_fields = ('p_title', 'usr', 'p_read', 'p_thumb', 'p_release_time',
                       'p_user', 'p_content', 'p_url')


admin.site.register(PzPicture, PictureAdmin)
