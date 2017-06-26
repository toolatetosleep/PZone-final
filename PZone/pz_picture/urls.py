# coding:utf-8

from django.conf.urls import url
from pz_picture import views as picture_view

urlpatterns = [

    # 佳作 - 首页
    url(r'^index$', picture_view.index_page1, name='picture_first'),

    url(r'^(\d+)$', picture_view.index, name='picture_index'),

    # 佳作 - 详情
    url(r'^item/(\d+)$', picture_view.detail, name='picture_detail'),

]
