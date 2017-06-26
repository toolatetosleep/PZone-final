# coding:utf-8
from django.contrib import admin
from pz_equipment.models import PzEquipment


# Register your models here.


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('e_title', 'usr', 'e_read', 'e_thumb', 'e_release_time')
    search_fields = ('e_title', 'e_content')
    list_filter = ('e_release_time',)
    date_hierarchy = 'e_release_time'
    list_display_links = ('e_title', 'usr', 'e_read', 'e_thumb', 'e_release_time')
    readonly_fields = ('e_title', 'usr', 'e_read', 'e_thumb', 'e_release_time',
                       'e_user', 'e_content', 'e_url')


admin.site.register(PzEquipment, EquipmentAdmin)
