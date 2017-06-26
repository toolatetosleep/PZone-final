# coding:utf-8
from django.shortcuts import render
from django.template import Context

from pz_index import dao
from pz_index.io_stream import get_cookies
from pz_user import dao as user_dao
from pz_picture import dao as picture_dao


# Create your views here.
# 首页
def index_page1(req):
    return index(req, 1)


# 首页
def index(req, crt_page):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        u = user_dao.get_user_info(username)
        obj_hot = dao.the_most_hot()
        obj_new = dao.the_most_new()
        # 查询所有头条
        list_obs = []
        page_all = picture_dao.count_page(5)
        my_list = picture_dao.get_page(int(crt_page), 5)
        for x in my_list:  # 内容
            com_num = picture_dao.get_com_count(x.p_id)
            list_obs.append({'title': x.p_title, 'url': x.p_url, 'content': x.p_content, 'id': x.p_id,
                             'time': str(x.p_release_time), 'read': x.p_read, 'thumb': x.p_thumb, 'com_num': com_num})
        con = Context({'username': username, 'u': u, 'obj': list_obs, 'page_all': page_all, 'page_this': int(crt_page),
                       'site_title': "摄影佳作", 'cat': 3, 'obj_hot': obj_hot, 'obj_new': obj_new})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return render(req, 'index.html', con)


def detail(req, mid):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        u = user_dao.get_user_info(username)
        obj_hot = dao.the_most_hot()
        obj_new = dao.the_most_new()
        page_all = dao.count_com_page(3, mid, 10)
        # 获取具体记录并返回
        det = picture_dao.article_detail(mid)
        picture_dao.read_num(mid)
        my_detail = {'a_id': det.p_id, 'a_user': user_dao.get_user_name(det.p_user), 'a_title': det.p_title,
                     'a_content': det.p_content, 'a_kind': "摄影佳作", 'a_cat': 3, 'u_id': det.p_user,
                     'a_time': det.p_release_time.strftime('%Y-%m-%d %H:%M:%S'), 'a_url': det.p_url,
                     'a_read': det.p_read,
                     'a_thumb': det.p_thumb, 'a_com': picture_dao.get_com_count(det.p_id)}
        con = Context({'username': username, 'u': u, 'detail': my_detail, 'obj_hot': obj_hot,
                       'obj_new': obj_new, 'page_all': page_all, 'page_this': 1})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return render(req, 'detail.html', con)
