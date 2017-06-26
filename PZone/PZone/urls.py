# coding:utf-8
"""PZone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from pz_initialization import views as init
import pz_index.views as site_index
import pz_index.tests as tests
from pz_user import urls as user_url
from pz_topic import urls as topic_url
from pz_picture import urls as picture_url
from pz_skill import urls as skill_url
from pz_equipment import urls as equipment_url

urlpatterns = [
    # 管理页
    url(r'^admin/', admin.site.urls),

    # 网站首页
    url(r'^$', site_index.index_first),
    url(r'^index/$', site_index.index_page1, name='site_index'),
    url(r'^index/(\d+)$', site_index.index),

    # 用户相关
    url(r'^user/', include(user_url)),

    # 头条相关
    url(r'^topic/', include(topic_url)),

    # 佳作相关
    url(r'^picture/', include(picture_url)),

    # 技巧相关
    url(r'^skill/', include(skill_url)),

    # 器材相关
    url(r'^equipment/', include(equipment_url)),

    # 初始化数据库
    url(r'^initdb/', init.init),

    # 获取具体评论
    url(r'^com/(\d+)/(\d+)/(\d+)$', site_index.get_com, name='site_com'),
    # 获取评论的回复
    url(r'^com/reply/(\d+)/(\d+)$', site_index.get_com_children, name='com_children'),
    # 发布评论
    url(r'^com/(\d+)/(\d+)$', site_index.give_com, name='give_com'),
    # 删除评论
    url(r'^com/(\d+)$', site_index.del_com, name='del_com'),

    # 文章的支持
    url(r'^thumbup/add/(\d+)/(\d+)$', site_index.thumbup_add, name='thumbup_add'),
    url(r'^thumbup/ant/(\d+)/(\d+)$', site_index.thumbup_ant, name='thumbup_ant'),
    # 删除文章
    url(r'delete/(\d+)/(\d+)$', site_index.delete_article, name='article_delete'),
    # 修改文章
    url(r'modify/(\d+)/(\d+)$', site_index.modifing, name='article_modify'),
    url(r'modify/json/(\d+)/(\d+)$', site_index.modifing_json, name='article_modify_json'),

    # 发布页
    url(r'^post/$', site_index.post, name='site_post'),
    # 发布
    url(r'^posting/$', site_index.posting, name='site_posting'),

    # 上传图片
    url(r'^upfile/$', site_index.upload, name='site_upload'),
    # url(r'^upfile$', tests.test, name='site_upload'),
    # 下载图片
    url(r'^download/(.+)$', site_index.download, name='site_download'),

    # 全站搜索
    url(r'^search/(.+)$', site_index.search_first, name='search_first'),
    url(r'^search/(\d+)/(.+)$', site_index.search_all, name='search_all'),

    # 测试
    url(r'^test/$', tests.test, name='test'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
