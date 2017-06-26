# coding:utf-8
from django.shortcuts import render
from django.template import Context

from pz_index import dao
from pz_equipment import dao as equipment_dao
from pz_index.io_stream import get_cookies
from pz_user import dao as user_dao


# Create your views here.
# 首页
def index_page1(req):
    return index(req, 1)


def index(req, crt_page):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        u = user_dao.get_user_info(username)
        obj_hot = dao.the_most_hot()
        obj_new = dao.the_most_new()
        # 查询所有头条
        list_obs = []
        page_all = equipment_dao.count_page(5)
        my_list = equipment_dao.get_page(int(crt_page), 5)
        for x in my_list:  # 内容
            com_num = equipment_dao.get_com_count(x.e_id)
            list_obs.append({'title': x.e_title, 'url': x.e_url, 'content': x.e_content, 'id': x.e_id,
                             'time': str(x.e_release_time), 'read': x.e_read, 'thumb': x.e_thumb, 'com_num': com_num})
        con = Context({'username': username, 'u': u, 'obj': list_obs, 'page_all': page_all, 'page_this': int(crt_page),
                       'site_title': "摄影器材", 'cat': 4, 'obj_hot': obj_hot, 'obj_new': obj_new})
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
        page_all = dao.count_com_page(4, mid, 10)
        # 获取具体记录并返回
        det = equipment_dao.article_detail(mid)
        equipment_dao.read_num(mid)
        my_detail = {'a_id': det.e_id, 'a_user': user_dao.get_user_name(det.e_user), 'a_title': det.e_title,
                     'a_content': det.e_content, 'a_kind': "摄影器材", 'a_cat': 4, 'u_id': det.e_user,
                     'a_time': det.e_release_time.strftime('%Y-%m-%d %H:%M:%S'), 'a_url': det.e_url,
                     'a_read': det.e_read,
                     'a_thumb': det.e_thumb, 'a_com': equipment_dao.get_com_count(det.e_id)}
        con = Context({'username': username, 'u': u, 'detail': my_detail, 'obj_hot': obj_hot,
                       'obj_new': obj_new, 'page_all': page_all, 'page_this': 1})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return render(req, 'detail.html', con)
