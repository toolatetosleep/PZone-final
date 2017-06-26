# coding:utf-8

from django.conf.urls import url
from pz_equipment import views as equipment_view

urlpatterns = [

    # 器材 - 首页
    url(r'^index$', equipment_view.index_page1, name='equipment_first'),

    url(r'^(\d+)$', equipment_view.index, name='equipment_index'),

    # 器材 - 详情
    url(r'^item/(\d+)$', equipment_view.detail, name='equipment_detail'),

]
