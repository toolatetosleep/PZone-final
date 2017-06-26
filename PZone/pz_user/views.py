# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from django.template import Context
from django import forms
from django.urls import reverse
from pz_user import dao as user_dao
from pz_topic import dao as topic_dao
from pz_skill import dao as skill_dao
from pz_picture import dao as picture_dao
from pz_equipment import dao as equipment_dao
from pz_user.io_stream import store_pic
from pz_index.encryption import rc4encode
from pz_index.io_stream import get_cookies


# Create your views here.
# 表单
class UserForm(forms.Form):
    username = forms.CharField(max_length=16, min_length=6)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=16, min_length=6)


# 登陆
def login(req, url):
    try:
        # response = redirect(url)
        response = HttpResponse("<script>window.history.back(-1);</script>")
        # 判断是否有Cookies存在，有则清空
        if get_cookies(req, 'username') is not None:
            response.delete_cookie('username')
        # 接收Post信息并判断是否可以登陆
        if req.method == 'POST':
            uf = UserForm(req.POST)
            if uf.is_valid():
                # 获得表单数据
                username = uf.cleaned_data['username']
                password = uf.cleaned_data['password']
                # 查询判断
                my_user = user_dao.get_users(username)
                if my_user:
                    db_pwd = user_dao.get_user(username).u_password
                    if check_password(password, db_pwd):
                        # 比较成功
                        # 将username写入浏览器cookie,失效时间为3600 * 3
                        response.set_cookie('username', rc4encode(username), 10800)
                        user_dao.add_credit(user_dao.get_user_id(username), 5)
                        return response
                # 不可以登陆则自动注册
                # pbkdf2_sha256加密算法
                str_pwd = make_password(password, 'pbkdf2_sha256')
                # 添加到数据库
                user_dao.new_user(username, str_pwd)
                # 将username写入浏览器cookie,失效时间为3600 * 3
                response.set_cookie('username', rc4encode(username), 10800)
                return response
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        # print response, url
        return response


# ajax用户查询
def ajax_user_check(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # 获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 查询判断
            my_user = user_dao.get_users(username)
            if my_user:
                db_pwd = user_dao.get_user(username).u_password
                if check_password(password, db_pwd):
                    # 有此用户且比对成功
                    return HttpResponse(1)
                else:
                    # 有此用户但密码错误
                    return HttpResponse(0)
            else:
                # 没有此用户
                return HttpResponse(1)
    # 非POST提交
    return HttpResponse(0)


# 登出
def logout(req, url):
    # response = redirect(url)
    response = HttpResponse("<script>window.history.back(-1);</script>")
    response.delete_cookie('username')
    return response


# 用户首页
def index(req):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        if username:
            u = user_dao.get_user_info2(username)
            # 获取首页的信息
            count = 10
            sql = """
                 select t_id as id, t_title as title, t_read as read1, t_thumb as thumb, t_release_time as time, 'topic'
                 as type from pz_topic where t_user = """ + str(u['uid']) + """ union all
                 select s_id as id, s_title as title, s_read as read1, s_thumb as thumb, s_release_time as time, 'skill'
                 as type from pz_skill where s_user = """ + str(u['uid']) + """ union all
                 select p_id as id, p_title as title, p_read as read1, p_thumb as thumb, p_release_time as time, 'picture'
                 as type from pz_picture where p_user = """ + str(u['uid']) + """ union all
                 select e_id as id, e_title as title, e_read as read1, e_thumb as thumb, e_release_time as time, 'equipment'
                 as type from pz_equipment where e_user = """ + str(u['uid']) + """
                 order by time desc LIMIT
            """ + str(count) + ";"
            my_list = user_dao.get_all_db(sql)
            obj_list = []
            for x in my_list:
                if x[5] == 'topic':
                    cat = 1
                    num = user_dao.get_com_count(x[0], cat)
                elif x[5] == 'skill':
                    cat = 2
                    num = user_dao.get_com_count(x[0], cat)
                elif x[5] == 'picture':
                    cat = 3
                    num = user_dao.get_com_count(x[0], cat)
                elif x[5] == 'equipment':
                    cat = 4
                    num = user_dao.get_com_count(x[0], cat)
                else:
                    cat = 0
                time = x[4].strftime('%Y-%m-%d %H:%M:%S')
                obj_list.append({'id': x[0], 'title': x[1], 'read': x[2], 'thumb': x[3],
                                 'time': time, 'cat': cat, 'com_num': int(num)})
            con = Context({'username': username, 'u': u, 'obj': obj_list})
            return render(req, 'center.html', con)
        else:
            return redirect('/index/')
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


# 根据Cookies查用户ID
def get_username(req):
    username = get_cookies(req, 'username')
    if username is not None:
        uid = user_dao.get_user_id(username)
        return HttpResponse(uid)
    return HttpResponse(0)


# 删除指定Cookies
def get_del_cookies(req, q):
    response = HttpResponse(0)
    response.delete_cookie(str(q))
    return response


# 用户消息
def user_message(req):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        if username:
            my_list = user_dao.get_messages(user_dao.get_user_id(username))
            obj_list = []
            i = 0
            # 获取未读的信息
            for x in my_list:
                name = user_dao.get_user_name(x.c_user_give)
                ava = user_dao.get_user_avatar(x.c_user_give)
                time = x.c_time.strftime('%Y-%m-%d %H:%M:%S')
                obj_list.append({'id': x.c_id, 'name': name, 'ava': ava, 'con': x.c_content, 'uid': x.c_user_give,
                                 'time': time, 'cat': int(x.c_category), 'item': x.c_item_id})
                i += 1
            con = Context({'username': username, 'obj': obj_list, 'count': i})
            return render(req, 'message.html', con)
        else:
            return redirect('/index/')
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


# 用户消息的已读设置
def mark_read(req):
    try:
        if req.method == "POST":
            username = get_cookies(req, 'username')
            qid = req.POST['id']
            if username and user_dao.set_read(int(qid), user_dao.get_user_id(username)):
                return HttpResponse(1)
            else:
                return HttpResponse(0)
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


# 以往发布
def user_post(req):
    try:
        username = get_cookies(req, 'username')
        if username:
            list_obs = []
            page_all = topic_dao.count_page_u(10, user_dao.get_user_id(username))
            my_list = topic_dao.get_page_u(1, 10, user_dao.get_user_id(username))
            for x in my_list:  # 内容
                com_num = topic_dao.get_com_count(x.t_id)
                list_obs.append({'title': x.t_title, 'id': x.t_id, 'time': str(x.t_release_time),
                                 'read': x.t_read, 'thumb': x.t_thumb, 'com_num': com_num, 'cat': 1})
            con = Context({'username': username, 'obj': list_obs, 'page_all': page_all, 'page_this': 1})
            return render(req, 'post.html', con)
        else:
            return redirect('/index/')
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


# 以往发布 JSON
def user_post_json(req, cat, page):
    try:
        username = get_cookies(req, 'username')
        if username:
            list_obs = []
            p = int(page)
            if int(cat) == 1:
                page_all = topic_dao.count_page_u(10, user_dao.get_user_id(username))
                my_list = topic_dao.get_page_u(p, 10, user_dao.get_user_id(username))
            elif int(cat) == 2:
                page_all = picture_dao.count_page_u(10, user_dao.get_user_id(username))
                my_list = picture_dao.get_page_u(p, 10, user_dao.get_user_id(username))
            elif int(cat) == 3:
                page_all = skill_dao.count_page_u(10, user_dao.get_user_id(username))
                my_list = skill_dao.get_page_u(p, 10, user_dao.get_user_id(username))
            elif int(cat) == 4:
                page_all = equipment_dao.count_page_u(10, user_dao.get_user_id(username))
                my_list = equipment_dao.get_page_u(p, 10, user_dao.get_user_id(username))
            else:
                pass
            for x in my_list:  # 内容
                if int(cat) == 1:
                    com_num = topic_dao.get_com_count(x.t_id)
                    list_obs.append({'title': x.t_title, 'id': x.t_id, 'time': str(x.t_release_time),
                                     'read': x.t_read, 'thumb': x.t_thumb, 'com_num': com_num, 'cat': 1,
                                     'page_all': page_all, 'page_this': int(page)})
                elif int(cat) == 2:
                    com_num = picture_dao.get_com_count(x.p_id)
                    list_obs.append({'title': x.p_title, 'id': x.p_id, 'time': str(x.p_release_time),
                                     'read': x.p_read, 'thumb': x.p_thumb, 'com_num': com_num, 'cat': 2,
                                     'page_all': page_all, 'page_this': int(page)})
                elif int(cat) == 3:
                    com_num = skill_dao.get_com_count(x.s_id)
                    list_obs.append({'title': x.s_title, 'id': x.s_id, 'time': str(x.s_release_time),
                                     'read': x.s_read, 'thumb': x.s_thumb, 'com_num': com_num, 'cat': 3,
                                     'page_all': page_all, 'page_this': int(page)})
                elif int(cat) == 4:
                    com_num = equipment_dao.get_com_count(x.e_id)
                    list_obs.append({'title': x.e_title, 'id': x.e_id, 'time': str(x.e_release_time),
                                     'read': x.e_read, 'thumb': x.e_thumb, 'com_num': com_num, 'cat': 4,
                                     'page_all': page_all, 'page_this': int(page)})
                else:
                    pass
            return JsonResponse(list_obs, safe=False)
        else:
            return redirect('/index/')
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


# 以往发布 其他用户 JSON
def user_other_json(req, uid, cat, page):
    try:
        username = user_dao.get_user_name(int(uid))
        list_obs = []
        p = int(page)
        if int(cat) == 1:
            page_all = topic_dao.count_page_u(10, user_dao.get_user_id(username))
            my_list = topic_dao.get_page_u(p, 10, user_dao.get_user_id(username))
        elif int(cat) == 2:
            page_all = picture_dao.count_page_u(10, user_dao.get_user_id(username))
            my_list = picture_dao.get_page_u(p, 10, user_dao.get_user_id(username))
        elif int(cat) == 3:
            page_all = skill_dao.count_page_u(10, user_dao.get_user_id(username))
            my_list = skill_dao.get_page_u(p, 10, user_dao.get_user_id(username))
        elif int(cat) == 4:
            page_all = equipment_dao.count_page_u(10, user_dao.get_user_id(username))
            my_list = equipment_dao.get_page_u(p, 10, user_dao.get_user_id(username))
        else:
            pass
        for x in my_list:  # 内容
            if int(cat) == 1:
                com_num = topic_dao.get_com_count(x.t_id)
                list_obs.append({'title': x.t_title, 'id': x.t_id, 'time': str(x.t_release_time),
                                 'read': x.t_read, 'thumb': x.t_thumb, 'com_num': com_num, 'cat': 1,
                                 'page_all': page_all, 'page_this': int(page)})
            elif int(cat) == 2:
                com_num = picture_dao.get_com_count(x.p_id)
                list_obs.append({'title': x.p_title, 'id': x.p_id, 'time': str(x.p_release_time),
                                 'read': x.p_read, 'thumb': x.p_thumb, 'com_num': com_num, 'cat': 2,
                                 'page_all': page_all, 'page_this': int(page)})
            elif int(cat) == 3:
                com_num = skill_dao.get_com_count(x.s_id)
                list_obs.append({'title': x.s_title, 'id': x.s_id, 'time': str(x.s_release_time),
                                 'read': x.s_read, 'thumb': x.s_thumb, 'com_num': com_num, 'cat': 3,
                                 'page_all': page_all, 'page_this': int(page)})
            elif int(cat) == 4:
                com_num = equipment_dao.get_com_count(x.e_id)
                list_obs.append({'title': x.e_title, 'id': x.e_id, 'time': str(x.e_release_time),
                                 'read': x.e_read, 'thumb': x.e_thumb, 'com_num': com_num, 'cat': 4,
                                 'page_all': page_all, 'page_this': int(page)})
            else:
                pass
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return JsonResponse(list_obs, safe=False)


# 用户资料
def user_info(req):
    try:
        username = get_cookies(req, 'username')
        if username:
            meta = user_dao.get_user_info2(username)
            obj_dict = {
                'id': meta['uid'],
                'ava': meta['ava'],
                'name': username,
                'desp': meta['dep']
            }
            con = Context({'username': username, 'obj': obj_dict})
            return render(req, 'info.html', con)
        else:
            return redirect('/index/')
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


# 用户资料 - 更新后
def fetch_user_info(req):
    try:
        username = get_cookies(req, 'username')
        if username:
            desp = req.POST['description']
            pwd = req.POST['password']
            pwd2 = req.POST['password2']
            # print(desp, pwd, pwd2)
            if pwd == pwd2:
                p = make_password(pwd, 'pbkdf2_sha256')
                d = user_dao.update_user_info(user_dao.get_user_id(username), desp, p)
                # print(d)
                return HttpResponse(d)
            meta = user_dao.get_user_info2(username)
            return HttpResponse(meta['dep'])
        else:
            return redirect('/index/')
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


# 更换头像
def avatar_change(req):
    try:
        username = get_cookies(req, 'username')
        if username:
            if req.method == "POST":
                pic = req.FILES.get("pic", None)
                path = store_pic(pic, 'avatar')
                img = user_dao.update_user_avatar(user_dao.get_user_id(username), path[1:])
                response = HttpResponse(0)
                response.set_cookie("img", img)
            return response
        else:
            return user_info(req)
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass


def user_other(req, uid):
    try:
        u = user_dao.get_user_info2(user_dao.get_user_name(int(uid)))
        list_obs = []
        my_list = topic_dao.get_page_u(1, 10, int(uid))
        for x in my_list:  # 内容
            com_num = topic_dao.get_com_count(x.t_id)
            list_obs.append({'title': x.t_title, 'id': x.t_id, 'time': str(x.t_release_time),
                             'read': x.t_read, 'thumb': x.t_thumb, 'com_num': com_num, 'cat': 1})
        con = Context({'u': u, 'obj': list_obs})
        return render(req, 'other.html', con)
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        pass
