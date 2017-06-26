# coding:utf-8
from django.contrib import admin
from pz_index.models import PzComment


# Register your models here.

class CommonAdmin(admin.ModelAdmin):
    list_display = ('content', 'user_give', 'user_recv',
                    'category', 'is_reply', 'read', 'c_time')
    search_fields = ('content', 'category', 'is_reply')
    list_filter = ('c_time',)
    date_hierarchy = 'c_time'
    list_display_links = ('content', 'user_give', 'user_recv',
                          'category', 'is_reply', 'c_time', 'read')
    readonly_fields = ('content', 'user_give', 'user_recv',
                       'category', 'is_reply', 'read', 'c_time',
                       'c_user_give', 'c_user_recive', 'c_category',
                       'c_item_id', 'c_com_recive', 'c_read', 'c_content')


admin.site.register(PzComment, CommonAdmin)
