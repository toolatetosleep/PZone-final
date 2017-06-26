# coding:utf-8
from pz_skill.models import PzSkill, PzComment
from django.utils import timezone


# 获取分页记录 .2
def get_page(page, count):
    i = page * count - count
    my_list = PzSkill.objects.order_by("-s_id")[i: i + count]
    return my_list


# 获取分页记录 .2 用户
def get_page_u(page, count, uid):
    i = page * count - count
    my_list = PzSkill.objects.filter(s_user__exact=uid).order_by("-s_id")[i: i + count]
    return my_list


# 计算分页并返回总页面数 .1
def count_page(count):
    my_list = PzSkill.objects.all().count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 计算分页并返回总页面数 .1 用户
def count_page_u(count, uid):
    my_list = PzSkill.objects.filter(s_user__exact=uid).count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 获取评论数 .1
def get_com_count(qid):
    # 评论的具体文章的种类（1头条、2技巧、3佳作、4器材）
    num = PzComment.objects.filter(c_category__exact=2, c_item_id__exact=qid).count()
    return num


# 　获取文章详情 .2
def article_detail(qid):
    mid = int(qid)
    det = PzSkill.objects.get(s_id__exact=mid)
    return det


# 新增文章 .9
def new_article(title, content, qid, url):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    article = PzSkill(s_user=qid, s_title=title, s_content=content, s_release_time=date, s_url=url, s_read=0,
                      s_thumb=0)
    article.save()
    return article.s_id


# 修改文章 .7
def mod_article(aid, title, content, url):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    article = PzSkill.objects.get(s_id__exact=int(aid))
    article.s_title = title
    article.s_content = content
    article.s_url = url
    article.s_release_time = date
    article.save()
    return article.s_id


# 文章的支持 .4
def thumbup_add(item):
    obj = PzSkill.objects.get(s_id__exact=int(item))
    obj.s_thumb = int(obj.s_thumb) + 1
    obj.save()


# 文章的支持 .4
def thumbup_ant(item):
    obj = PzSkill.objects.get(s_id__exact=int(item))
    obj.s_thumb = int(obj.s_thumb) - 1
    obj.save()


# 阅读数 .4
def read_num(item):
    obj = PzSkill.objects.get(s_id__exact=int(item))
    obj.s_read = int(obj.s_read) + 1
    obj.save()


# 删除文章 .2
def deleting(item):
    PzSkill.objects.get(s_id__exact=int(item)).delete()


# 文章详情 .7
def get_detail(item):
    det = PzSkill.objects.get(s_id__exact=int(item))
    my_detail = {'a_id': det.s_id, 'a_title': det.s_title,
                 'a_content': det.s_content, 'a_cat': 2, 'a_url': det.s_url}
    return my_detail
