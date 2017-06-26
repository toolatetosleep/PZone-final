from django.contrib import admin
from pz_user.models import PzUser


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'u_last_login_time'
    list_display_links = ('u_id', 'u_username', 'u_credit', 'u_last_login_time')
    search_fields = ('u_id', 'u_username')
    list_display = ('u_id', 'u_username', 'u_credit', 'u_last_login_time')
    readonly_fields = ('u_id', 'u_username', 'u_credit', 'u_last_login_time',
                       'u_password', 'u_avatar', 'u_autograph')


admin.site.register(PzUser, UserAdmin)
