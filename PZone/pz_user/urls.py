# coding:utf-8

from django.conf.urls import url
from pz_user import views as user_view

urlpatterns = [
    # 用户登陆
    url(r'^login(.+)/$', user_view.login, name='site_login'),
    url(r'^ajax/check/user/$', user_view.ajax_user_check, name='ajax_user_check'),
    # 用户登出
    url(r'^logout(.+)/$', user_view.logout, name='site_logout'),

    # 用户首页
    url(r'^index/$', user_view.index, name='user_index'),
    # 用户消息
    url(r'^message/$', user_view.user_message, name='user_message'),
    # 以往发布
    url(r'^post/$', user_view.user_post, name='user_post'),
    # 以往发布 - Json
    url(r'^post/json/(\d+)/(\d+)$', user_view.user_post_json, name='user_post_json'),
    # 以往发布 - 其他用户 - Json
    url(r'^post/json/(\d+)/(\d+)/(\d+)$', user_view.user_other_json, name='user_other_json'),
    # 用户资料
    url(r'^info/$', user_view.user_info, name='user_info'),
    # 其他用户
    url(r'^index/(\d+)$', user_view.user_other, name='user_other'),

    # 用户消息的已读设置
    url(r'^com/read/$', user_view.mark_read, name='mark_com_read'),
    # 用户上传头像
    url(r'^upload/avatar/$', user_view.avatar_change, name='avatar_upload'),
    # 用户更新信息
    url(r'^upload/info/$', user_view.fetch_user_info, name='info_update'),
    # 根据Cookies查用户ID
    url(r'^get/username/$', user_view.get_username, name='get_user_name'),
    # 删除指定Cookies
    url(r'^get/delcookies/(.+)$', user_view.get_del_cookies, name='get_del_cookies'),

]
