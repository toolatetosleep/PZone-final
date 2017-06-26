# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import random
from pz_topic.models import PzTopic
from pz_skill.models import PzSkill
from pz_picture.models import PzPicture
from pz_equipment.models import PzEquipment
from pz_user.models import PzUser, PzComment

# Create your views here.
DONE = """
<h1 style="font-size: 5em;text-align: center;">
DONE!
</h>
<script>
window.setTimeout("window.location='/index/'",2000);
</script>
"""


def init(req):
    try:
        # print u'清除旧记录中'
        # 清除用户的全部记录
        PzUser.objects.all().delete()
        # 清除四大板块的全部记录
        PzTopic.objects.all().delete()
        PzPicture.objects.all().delete()
        PzSkill.objects.all().delete()
        PzEquipment.objects.all().delete()
        # 清除评论的全部记录
        PzComment.objects.all().delete()
        # print u'清除旧记录完成\n'
        # print u'初始化用户信息'
        # 初始化用户
        i = 0
        name, avatar, user_list = [], [], []
        while i < 5:
            name.append(u'testuser' + str(i + 1))
            avatar.append(u'/upload/init/avatar/avatar' + str(i + 1) + u'.jpg')
            password = make_password(name[i], 'pbkdf2_sha256')
            date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            user = PzUser(u_autograph=u'这家伙什么都没留下', u_avatar=avatar[i], u_last_login_time=date,
                          u_username=name[i], u_password=password, u_credit=5)
            user.save()
            user_list.append(user.u_id)
            i += 1
        # print u'初始化用户信息完成\n'
        i = 1
        img_list = []
        while i <= 8:
            img_list.append(u'/upload/init/Images/img (' + str(i) + u').jpg')
            i += 1
        # print u'初始化 头条/技巧/佳作/器材'
        i = 0
        while i <= 10:
            # 初始化头条
            user_id = random.choice(user_list)
            title = u'头条测试 ' + str(i) + u' '
            date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            cont = "<p>" + title * 50 + "</p>"
            topic = PzTopic(t_user=user_id, t_title=title, t_content=cont, t_release_time=date,
                            t_url=random.choice(img_list), t_read=random.randint(0, 100),
                            t_thumb=random.randint(0, 50))
            topic.save()
            # 随机数量的评论
            k = 0
            l = random.randint(0, 5)
            while k < l:
                item = topic.t_id
                user_id = random.choice(user_list)
                user_rc = random.choice(user_list)
                date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                com = PzComment(c_item_id=item, c_user_give=user_id, c_user_recive=user_rc,
                                c_content=u'评论测试' + str(k + 1),
                                c_time=date, c_category=1, c_read=random.choice([1, 0]))
                com.save()
                k += 1

            # 初始化技巧
            user_id = random.choice(user_list)
            title = u'技巧测试 ' + str(i) + u' '
            date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            cont = "<p>" + title * 50 + "</p>"
            skill = PzSkill(s_user=user_id, s_title=title, s_content=cont, s_release_time=date,
                            s_url=random.choice(img_list), s_read=random.randint(0, 100),
                            s_thumb=random.randint(0, 50))
            skill.save()
            # 随机数量的评论
            k = 0
            l = random.randint(0, 5)
            while k < l:
                item = skill.s_id
                user_id = random.choice(user_list)
                user_rc = random.choice(user_list)
                date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                com = PzComment(c_item_id=item, c_user_give=user_id, c_user_recive=user_rc,
                                c_content=u'评论测试' + str(k + 1),
                                c_time=date, c_category=2, c_read=random.choice([1, 0]))
                com.save()
                k += 1

            # 初始化佳作
            user_id = random.choice(user_list)
            title = u'佳作测试 ' + str(i) + u' '
            date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            cont = "<p>" + title * 50 + "</p>"
            picture = PzPicture(p_user=user_id, p_title=title, p_content=cont, p_release_time=date,
                                p_url=random.choice(img_list), p_read=random.randint(0, 100),
                                p_thumb=random.randint(0, 50))
            picture.save()
            # 随机数量的评论
            k = 0
            l = random.randint(0, 5)
            while k < l:
                item = picture.p_id
                user_id = random.choice(user_list)
                user_rc = random.choice(user_list)
                date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                com = PzComment(c_item_id=item, c_user_give=user_id, c_user_recive=user_rc,
                                c_content=u'评论测试' + str(k + 1),
                                c_time=date, c_category=3, c_read=random.choice([1, 0]))
                com.save()
                k += 1

            # 初始化器材
            user_id = random.choice(user_list)
            title = u'器材测试 ' + str(i) + u' '
            date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            cont = "<p>" + title * 50 + "</p>"
            equipment = PzEquipment(e_user=user_id, e_title=title, e_content=cont, e_release_time=date,
                                    e_url=random.choice(img_list), e_read=random.randint(0, 100),
                                    e_thumb=random.randint(0, 50))
            equipment.save()
            # 随机数量的评论
            k = 0
            l = random.randint(0, 5)
            while k < l:
                item = equipment.e_id
                user_id = random.choice(user_list)
                user_rc = random.choice(user_list)
                date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                com = PzComment(c_item_id=item, c_user_give=user_id, c_user_recive=user_rc,
                                c_content=u'评论测试' + str(k + 1),
                                c_time=date, c_category=4, c_read=random.choice([1, 0]))
                com.save()
                k += 1
            i += 1

        # print u'初始化 头条/技巧/佳作/器材 完成\n'

    except Exception as e:
        # print u'初始化失败'
        print(e)
        return render(req, 'error.html')
    else:
        # print u'初始化成功'
        return HttpResponse(DONE)
