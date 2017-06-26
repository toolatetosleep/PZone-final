# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import Context
from django.urls import reverse
from io_stream import get_cookies, store_pic, download_file
from pz_index import dao
from pz_user import dao as user_dao
from pz_topic import dao as topic_dao
from pz_skill import dao as skill_dao
from pz_equipment import dao as equipment_dao
from pz_picture import dao as picture_dao
from django.conf import settings


# Create your views here.

# 首页
def index_first(req):
    return redirect("/index/1")


def index_page1(req):
    return index(req, 1)


def index(req, crt_page):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        u = user_dao.get_user_info(username)
        obj_hot = dao.the_most_hot()
        obj_new = dao.the_most_new()
        # 获取全部的信息的页面数
        sql = """
            SELECT
            (select count(*) from pz_topic) +
            (select count(*) from pz_skill) +
            (select count(*) from pz_picture) +
            (select count(*) from pz_equipment)
            AS data;
        """
        alpage = int(dao.get_one_db(sql)[0])
        # 获取首页的信息
        count = 5

        all_page = alpage / count
        temp = alpage % count
        if temp != 0:
            all_page += 1

        sql = """
            select t_id as id, t_url as url, t_title as title, t_content as content, t_read as read1,
            t_thumb as thumb, t_release_time as time, 'topic' as type from pz_topic union all
            select s_id as id, s_url as url, s_title as title, s_content as content, s_read as read1,
            s_thumb as thumb, s_release_time as time, 'skill' as type from pz_skill union all
            select p_id as id, p_url as url, p_title as title, p_content as content, p_read as read1,
            p_thumb as thumb, p_release_time as time, 'picture' as type from pz_picture union all
            select e_id as id, e_url as url, e_title as title, e_content as content, e_read as read1,
            e_thumb as thumb, e_release_time as time, 'equipment' as type from pz_equipment order by time desc LIMIT
        """ + str(count * (int(crt_page) - 1)) + ", " + str(count) + ";"
        my_list = dao.get_all_db(sql)
        obj_list = []
        for x in my_list:
            if x[7] == 'topic':
                cat = 1
                num = topic_dao.get_com_count(x[0])
            elif x[7] == 'skill':
                cat = 2
                num = skill_dao.get_com_count(x[0])
            elif x[7] == 'picture':
                cat = 3
                num = picture_dao.get_com_count(x[0])
            elif x[7] == 'equipment':
                cat = 4
                num = equipment_dao.get_com_count(x[0])
            else:
                cat = 0
            time = x[6].strftime('%Y-%m-%d %H:%M:%S')
            obj_list.append({'id': x[0], 'url': x[1], 'title': x[2],
                             'content': x[3], 'read': x[4], 'thumb': x[5],
                             'time': time, 'cat': cat, 'com_num': int(num)})
        con = Context(
                {'username': username, 'u': u, 'site_title': "首页",
                 'obj_hot': obj_hot, 'obj_new': obj_new, 'obj': obj_list,
                 'page_all': all_page, 'page_this': int(crt_page)})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return render(req, 'index.html', con)


# 发布页
def post(req):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        if username is None:
            return redirect('/index/')
        con = Context({'username': username})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return render(req, 'postin.html', con)


# 发布 - 二次发布（修改）
def posting(req):
    try:
        if req.method == "POST":
            title = req.POST['title']
            content = req.POST['content']
            kind = req.POST['kind']
            url = req.POST['url']
            aid = req.POST['set']
            if int(aid) == 0:
                # aid = 0 新文章
                uid = user_dao.get_user_id(get_cookies(req, 'username'))
                if int(kind) == 1:
                    # 头条
                    tid = topic_dao.new_article(title, content, uid, url)
                    u = reverse('topic_detail', args=(int(tid),))
                    user_dao.add_credit(uid, 15)
                    return HttpResponse(u)
                elif int(kind) == 3:
                    # 佳作
                    tid = picture_dao.new_article(title, content, uid, url)
                    u = reverse('picture_detail', args=(int(tid),))
                    user_dao.add_credit(uid, 15)
                    return HttpResponse(u)
                elif int(kind) == 2:
                    # 技巧
                    tid = skill_dao.new_article(title, content, uid, url)
                    u = reverse('skill_detail', args=(int(tid),))
                    user_dao.add_credit(uid, 15)
                    return HttpResponse(u)
                elif int(kind) == 4:
                    # 器材
                    tid = equipment_dao.new_article(title, content, uid, url)
                    u = reverse('equipment_detail', args=(int(tid),))
                    user_dao.add_credit(uid, 15)
                    return HttpResponse(u)
                return HttpResponse(reverse('site_index'))
            else:
                # aid ！= 0 修改文章
                # uid = user_dao.get_user_id(get_cookies(req, 'username'))
                if int(kind) == 1:
                    # 头条
                    tid = topic_dao.mod_article(aid, title, content, url)
                    u = reverse('topic_detail', args=(int(tid),))
                    return HttpResponse(u)
                elif int(kind) == 3:
                    # 佳作
                    tid = picture_dao.mod_article(aid, title, content, url)
                    u = reverse('picture_detail', args=(int(tid),))
                    return HttpResponse(u)
                elif int(kind) == 2:
                    # 技巧
                    tid = skill_dao.mod_article(aid, title, content, url)
                    u = reverse('skill_detail', args=(int(tid),))
                    return HttpResponse(u)
                elif int(kind) == 4:
                    # 器材
                    tid = equipment_dao.mod_article(aid, title, content, url)
                    u = reverse('equipment_detail', args=(int(tid),))
                    return HttpResponse(u)
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return HttpResponse(reverse('site_index'))


# 修改
def modifing(req, cat, item):
    return render(req, 'postin.html', Context({'fun': 1, '1cat': cat, '1item': item}))


def modifing_json(req, cat, item):
    try:
        c = int(cat)
        if c == 1:
            det = topic_dao.get_detail(item)
        elif c == 2:
            det = skill_dao.get_detail(item)
        elif c == 3:
            det = picture_dao.get_detail(item)
        elif c == 4:
            det = equipment_dao.get_detail(item)
        else:
            det = {}
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return JsonResponse(det, safe=False)


# 删除
def delete_article(req, cat, item):
    try:
        c = int(cat)
        if c == 1:
            topic_dao.deleting(item)
        elif c == 2:
            skill_dao.deleting(item)
        elif c == 3:
            picture_dao.deleting(item)
        elif c == 4:
            equipment_dao.deleting(item)
        else:
            pass
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return HttpResponse(1)


# 上传图片
def upload(req):
    try:
        if req.method == "POST":
            pic = req.FILES.get("myPic", None)
            path = store_pic(pic, 'image')
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        # return HttpResponse(settings.SITE_URL + path[2:])
        print path
        return HttpResponse(path[1:])


# 下载图片
def download(req, src):
    # my_file = get_cookies(req, 'file')
    # if my_file is not None:
    if src is not None:
        # print src
        return download_file(src)
        # return download_file(my_file)
    return HttpResponse(0)


# 获取评论
def get_com(req, cat, qid, page):
    try:
        com_list = dao.get_com_page(cat, qid, int(page), 10)
        obj_list = []
        page_all = dao.count_com_page(cat, qid, 10)
        for x in com_list:
            ava = user_dao.get_user_avatar(x.c_user_give)
            name = user_dao.get_user_name(x.c_user_give)
            time = x.c_time.strftime('%Y-%m-%d %H:%M:%S')
            rep = dao.count_com_reply(cat, qid, x.c_id)
            c_link = str(reverse('com_children', args=(x.c_id, 1)))
            u_link = str(reverse('user_other', args=(x.c_user_give,)))
            obj_list.append({'c_ava': ava, 'c_id': x.c_user_give, 'c_name': name, 'c_rep': rep,
                             'c_time': time, 'c_flt': 1, 'c_con': x.c_content, 'c_com_id': int(x.c_id),
                             'page_all': int(page_all), 'page_this': int(page), 'com_link': c_link,
                             'user_link': u_link})
        obj_list.reverse()
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return JsonResponse(obj_list, safe=False)


# 获取评论
def get_com_children(req, qid, page):
    try:
        com_list = dao.get_com_children_page(qid, int(page), 10)
        obj_list = []
        page_all = dao.count_com_children_page(qid, 10)
        for x in com_list:
            cid = x.c_id
            con = x.c_content
            ava = user_dao.get_user_avatar(x.c_user_give)
            user = user_dao.get_user_name(x.c_user_give)
            urev = user_dao.get_user_name(x.c_user_recive)
            time = x.c_time.strftime('%Y-%m-%d %H:%M:%S')
            give_link = reverse('user_other', args=(x.c_user_give,))
            recv_link = reverse('user_other', args=(x.c_user_recive,))
            obj_list.append({'c_ava': ava, 'c_uid': user, 'c_time': time, 'c_id': cid, 'u_give': x.c_user_give,
                             'c_con': con, 'c_rid': urev, 'p_all': page_all, 'p_this': int(page),
                             'glink': give_link, 'rlink': recv_link})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return JsonResponse(obj_list, safe=False)


# 发布评论
def give_com(req, cat, item):
    try:
        if req.method == 'POST':
            user_give = user_dao.get_user_id(get_cookies(req, 'username'))
            user_recive = req.POST['u_rev']
            category = int(cat)
            it = int(item)
            com_recive = req.POST['c_rev']
            content = req.POST['content']
            dao.post_com(user_give, user_recive, category, it, com_recive, content)
            user_dao.add_credit(user_give, 3)
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return HttpResponse(1)


# 删除评论
def del_com(req, qid):
    try:
        user_id = user_dao.get_user_id(get_cookies(req, 'username'))
        dao.del_com(qid, user_id)
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return HttpResponse(1)


# 文章的支持 加
def thumbup_add(req, cat, item):
    try:
        c = int(cat)
        if c == 1:
            topic_dao.thumbup_add(int(item))
        elif c == 2:
            skill_dao.thumbup_add(int(item))
        elif c == 3:
            picture_dao.thumbup_add(int(item))
        elif c == 4:
            equipment_dao.thumbup_add(int(item))
        else:
            pass
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return HttpResponse(1)


# 文章的支持 减
def thumbup_ant(req, cat, item):
    try:
        c = int(cat)
        if c == 1:
            topic_dao.thumbup_ant(int(item))
        elif c == 2:
            skill_dao.thumbup_ant(int(item))
        elif c == 3:
            picture_dao.thumbup_ant(int(item))
        elif c == 4:
            equipment_dao.thumbup_ant(int(item))
        else:
            pass
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return HttpResponse(1)


# 全站搜索
def search_first(req, q):
    return search_all(req, 1, q)


def search_all(req, crt_page, q):
    try:
        # 获取Cookies判断用户是否已登陆
        username = get_cookies(req, 'username')
        u = user_dao.get_user_info(username)
        obj_hot = dao.the_most_hot()
        obj_new = dao.the_most_new()
        # 获取全部的信息的页面数
        sql = """
            SELECT
            (SELECT COUNT(*) FROM pz_topic WHERE t_title LIKE '%""" + str(
                q.encode('utf-8')) + """%' OR t_content LIKE '%""" + str(q.encode('utf-8')) + """%') +
            (SELECT COUNT(*) FROM pz_skill WHERE s_title LIKE '%""" + str(
                q.encode('utf-8')) + """%' OR s_content LIKE '%""" + str(q.encode('utf-8')) + """%') +
            (SELECT COUNT(*) FROM pz_picture WHERE p_title LIKE '%""" + str(
                q.encode('utf-8')) + """%' OR p_content LIKE '%""" + str(q.encode('utf-8')) + """%') +
            (SELECT COUNT(*) FROM pz_equipment WHERE e_title LIKE '%""" + str(
                q.encode('utf-8')) + """%' OR e_content LIKE '%""" + str(q.encode('utf-8')) + """%')
            AS data;
        """
        alpage = int(dao.get_one_db(sql)[0])
        # 获取首页的信息
        count = 20

        all_page = alpage / count
        temp = alpage % count
        if temp != 0:
            all_page += 1

        sql = """
            SELECT * FROM (
            select t_id as id, t_title as title, t_content as content, t_read as read1,
            t_thumb as thumb, t_release_time as time, 'topic' as type from pz_topic union all
            select s_id as id, s_title as title, s_content as content, s_read as read1,
            s_thumb as thumb, s_release_time as time, 'skill' as type from pz_skill union all
            select p_id as id, p_title as title, p_content as content, p_read as read1,
            p_thumb as thumb, p_release_time as time, 'picture' as type from pz_picture union all
            select e_id as id, e_title as title, e_content as content, e_read as read1,
            e_thumb as thumb, e_release_time as time, 'equipment' as type from pz_equipment
            ) AS T WHERE title LIKE '%""" + str(q.encode('utf-8')) + """%' OR content LIKE '%""" + str(
                q.encode('utf-8')) + """
            %' ORDER BY time DESC LIMIT """ + str(count * (int(crt_page) - 1)) + ", " + str(count) + ";"
        my_list = dao.get_all_db(sql)
        obj_list = []
        for x in my_list:
            if x[6] == 'topic':
                cat = 1
                num = topic_dao.get_com_count(x[0])
            elif x[6] == 'skill':
                cat = 2
                num = skill_dao.get_com_count(x[0])
            elif x[6] == 'picture':
                cat = 3
                num = picture_dao.get_com_count(x[0])
            elif x[6] == 'equipment':
                cat = 4
                num = equipment_dao.get_com_count(x[0])
            else:
                cat = 0
            time = x[5].strftime('%Y-%m-%d %H:%M:%S')
            obj_list.append({'id': x[0], 'title': x[1],
                             'content': x[2], 'read': x[3], 'thumb': x[4],
                             'time': time, 'cat': cat, 'com_num': int(num)})
        con = Context({'username': username, 'u': u, 'site_title': "首页", 'q': q,
                       'obj_hot': obj_hot, 'obj_new': obj_new, 'obj': obj_list, 'qn': alpage,
                       'page_all': all_page, 'page_this': int(crt_page)})
    except Exception as e:
        print(e)
        return render(req, 'error.html')
    else:
        return render(req, 'search.html', con)
