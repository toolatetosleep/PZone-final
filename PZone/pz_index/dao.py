# coding:utf-8
from django.db import connection
from django.utils import timezone
from pz_index.models import PzComment


# 获取自定的SQL语句结果并返回结果列表
def get_all_db(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        obj = []
        for x in row:
            obj.append(x)
    except Exception as e:
        print(e)
        return None
    else:
        return obj


# 获取自定的SQL语句结果并返回结果
def get_one_db(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
    except Exception as e:
        print(e)
        return None
    else:
        return row


# 发布评论
def post_com(u_give, u_rev, cat, item, c_rev, con):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    user_give = u_give
    user_recive = u_rev
    com_recive = c_rev
    content = con
    com = PzComment(c_read=0, c_time=date, c_user_recive=user_recive, c_user_give=user_give,
                    c_category=cat, c_item_id=item, c_com_recive=com_recive, c_content=content)
    com.save()


# 获取分页记录 .2
def get_com_page(cat, qid, page, count):
    i = page * count - count
    my_list = PzComment.objects.filter(c_category__exact=cat, c_item_id__exact=qid, c_com_recive__exact=0).order_by(
        "-c_time")[i: i + count]
    return my_list


# 获取分页记录 .2
def get_com_children_page(qid, page, count):
    i = page * count - count
    # my_list = PzCommon.objects.filter(c_com_recive__exact=qid).order_by("-c_time")[i: i + count]
    my_list = PzComment.objects.filter(c_com_recive__exact=qid).order_by("-c_time")
    return my_list


# 获取评论数 .
def count_com_page(cat, qid, count):
    c = int(cat)
    i = int(qid)
    my_list = PzComment.objects.filter(c_category__exact=c, c_item_id__exact=i, c_com_recive__exact=0).count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 获取评论数 .
def count_com_children_page(qid, count):
    i = int(qid)
    my_list = PzComment.objects.filter(c_com_recive__exact=qid).count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 获取回复评论的评论数
def count_com_reply(cat, qid, com):
    num = PzComment.objects.filter(c_category__exact=cat, c_item_id__exact=qid, c_com_recive__exact=com).count()
    return num


# 删除评论
def del_com(cid, uid):
    com = PzComment.objects.get(c_id__exact=cid)
    if com.c_user_give == uid:
        com.delete()


# 站点左侧的 全站最热
def the_most_hot():
    sql = """
        select t_id as id, t_title as title, (t_read + t_thumb) as hot, 'topic' as type from pz_topic union all
        select s_id as id, s_title as title, (s_read + s_thumb) as hot, 'skill' as type from pz_skill union all
        select p_id as id, p_title as title, (p_read + p_thumb) as hot, 'picture' as type from pz_picture union all
        select e_id as id, e_title as title, (e_read + e_thumb) as hot, 'equipment' as type from pz_equipment
        order by hot desc LIMIT 10;
    """
    my_list = get_all_db(sql)
    obj_list = []
    for x in my_list:
        if x[3] == 'topic':
            cat = 1
        elif x[3] == 'skill':
            cat = 2
        elif x[3] == 'picture':
            cat = 3
        elif x[3] == 'equipment':
            cat = 4
        else:
            cat = 0
        obj_list.append({'id': x[0], 'title': x[1], 'cat': cat})
    return obj_list


# 站点左侧的 随机阅读
def the_most_new():
    sql = """
        select t_id as id, t_title as title, 'topic' as type from pz_topic union all
        select s_id as id, s_title as title, 'skill' as type from pz_skill union all
        select p_id as id, p_title as title, 'picture' as type from pz_picture union all
        select e_id as id, e_title as title, 'equipment' as type from pz_equipment
        order by RAND() desc LIMIT 10;
    """
    my_list = get_all_db(sql)
    obj_list = []
    for x in my_list:
        if x[2] == 'topic':
            cat = 1
        elif x[2] == 'skill':
            cat = 2
        elif x[2] == 'picture':
            cat = 3
        elif x[2] == 'equipment':
            cat = 4
        else:
            cat = 0
        obj_list.append({'id': x[0], 'title': x[1], 'cat': cat})
    return obj_list
