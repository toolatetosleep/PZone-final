# coding:utf-8
from django.db import connection
from django.utils import timezone
from pz_user.models import PzUser, PzComment


# 注册一个新用户
def new_user(username, password):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    init_user = PzUser(u_username=username, u_password=password, u_credit=5,
                       u_avatar='/upload/init/avatar/default_avatar.jpg', u_autograph='这家伙什么都没留下',
                       u_last_login_time=date)
    init_user.save()


# 获取一个用户
def get_user(username):
    my_user = PzUser.objects.get(u_username__exact=username)
    return my_user


# 获取多个用户
def get_users(username):
    my_user = PzUser.objects.filter(u_username__exact=username)
    return my_user


# 获取用户ID
def get_user_id(username):
    my_user = PzUser.objects.get(u_username__exact=username)
    return my_user.u_id


# 获取用户头像
def get_user_avatar(uid):
    my_user = PzUser.objects.get(u_id__exact=uid)
    return my_user.u_avatar


# 更新用户头像
def update_user_avatar(uid, path):
    my_user = PzUser.objects.get(u_id__exact=uid)
    my_user.u_avatar = str(path)
    my_user.save()
    return my_user.u_avatar


# 更新用户信息
def update_user_info(uid, desp, pwd):
    try:
        my_user = PzUser.objects.get(u_id__exact=uid)
        my_user.u_autograph = desp
        my_user.u_password = pwd
        my_user.save()
    except Exception as e:
        print e
        return None
    else:
        return my_user.u_autograph


# 获取用户名
def get_user_name(uid):
    my_user = PzUser.objects.get(u_id__exact=uid)
    return my_user.u_username


# 获取登陆的用户的信息
def get_user_info(username):
    if username:
        uid = get_user_id(username)
        uav = get_user_avatar(uid)
        msg = PzComment.objects.filter(c_read=0, c_user_recive__exact=int(uid)).count()
        u = {'uid': uid, 'ava': uav, 'msg': msg}
    else:
        u = None
    return u


# 获取登陆的用户的信息2
def get_user_info2(username):
    if username:
        my_user = get_user(username)
        uid = my_user.u_id
        uav = my_user.u_avatar
        msg = PzComment.objects.filter(c_read=0, c_user_recive__exact=int(uid)).count()
        dep = my_user.u_autograph
        crd = my_user.u_credit
        u = {'uid': uid, 'ava': uav, 'msg': msg, 'dep': dep, 'crd': crd, 'uname': username}
    else:
        u = None
    return u


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


# 获取评论数 .1
def get_com_count(qid, cat):
    # 评论的具体文章的种类（1头条、2技巧、3佳作、4器材）
    num = PzComment.objects.filter(c_category__exact=int(cat), c_item_id__exact=qid).count()
    return num


# 获取未读的回复的评论
def get_messages(uid):
    my_list = PzComment.objects.filter(c_read=0, c_user_recive__exact=int(uid))
    return my_list


# 用户消息的已读设置
def set_read(cid, uid):
    com = PzComment.objects.get(c_id__exact=int(cid))
    if com.c_user_recive == int(uid):
        com.c_read = 1
        com.save()
        return True
    else:
        return False


# 加积分
def add_credit(uid, points):
    user = PzUser.objects.get(u_id__exact=int(uid))
    user.u_credit = int(user.u_credit) + int(points)
    user.save()
