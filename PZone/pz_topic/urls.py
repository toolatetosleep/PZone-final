# coding:utf-8

from django.conf.urls import url
from pz_topic import views as topic_view

urlpatterns = [

    # 头条 - 首页
    url(r'^index$', topic_view.index_page1, name='topic_first'),

    url(r'^(\d+)$', topic_view.index, name='topic_index'),

    # 头条 - 详情
    url(r'^item/(\d+)$', topic_view.detail, name='topic_detail'),




]
