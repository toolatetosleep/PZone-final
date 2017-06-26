# coding:utf-8

from django.conf.urls import url
from pz_skill import views as skill_view

urlpatterns = [

    # 技巧 - 首页
    url(r'^index$', skill_view.index_page1, name='skill_first'),

    url(r'^(\d+)$', skill_view.index, name='skill_index'),

    # 技巧 - 详情
    url(r'^item/(\d+)$', skill_view.detail, name='skill_detail'),






]
