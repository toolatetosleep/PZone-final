# coding:utf-8
from django.shortcuts import render
from django.template import Context

from pz_index import dao
from pz_index.io_stream import get_cookies
from pz_user import dao as user_dao
from pz_skill import dao as skill_dao


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
        page_all = skill_dao.count_page(5)
        my_list = skill_dao.get_page(int(crt_page), 5)
        for x in my_list:  # 内容
            com_num = skill_dao.get_com_count(x.s_id)
            list_obs.append({'title': x.s_title, 'url': x.s_url, 'content': x.s_content, 'id': x.s_id,
                             'time': str(x.s_release_time), 'read': x.s_read, 'thumb': x.s_thumb, 'com_num': com_num})
        con = Context({'username': username, 'u': u, 'obj': list_obs, 'page_all': page_all, 'page_this': int(crt_page),
                       'site_title': "摄影技巧", 'cat': 2, 'obj_hot': obj_hot, 'obj_new': obj_new})
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
        page_all = dao.count_com_page(2, mid, 10)
        # 获取具体记录并返回
        det = skill_dao.article_detail(mid)
        skill_dao.read_num(mid)
        my_detail = {'a_id': det.s_id, 'a_user': user_dao.get_user_name(det.s_user), 'a_title': det.s_title,
                     'a_content': det.s_content, 'a_kind': "摄影技巧", 'a_cat': 2, 'u_id': det.s_user,
                     'a_time': det.s_release_time.strftime('%Y-%m-%d %H:%M:%S'), 'a_url': det.s_url,
                     'a_read': det.s_read,
                     'a_thumb': det.s_thumb, 'a_com': skill_dao.get_com_count(det.s_id)}
        con = Context({'username': username, 'u': u, 'detail': my_detail, 'obj_hot': obj_hot,
                       'obj_new': obj_new, 'page_all': page_all, 'page_this': 1})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return render(req, 'detail.html', con)
