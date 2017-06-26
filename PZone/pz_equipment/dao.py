# coding:utf-8
from pz_equipment.models import PzEquipment, PzComment
from django.utils import timezone


# 获取分页记录 .2
def get_page(page, count):
    i = page * count - count
    my_list = PzEquipment.objects.order_by("-e_id")[i: i + count]
    return my_list


# 获取分页记录 .2 用户
def get_page_u(page, count, uid):
    i = page * count - count
    my_list = PzEquipment.objects.filter(e_user__exact=uid).order_by("-e_id")[i: i + count]
    return my_list


# 计算分页并返回总页面数 .1
def count_page(count):
    my_list = PzEquipment.objects.all().count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 计算分页并返回总页面数 .1 用户
def count_page_u(count, uid):
    my_list = PzEquipment.objects.filter(e_user__exact=uid).count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 获取评论数 .1
def get_com_count(qid):
    # 评论的具体文章的种类（1头条、2技巧、3佳作、4器材）
    num = PzComment.objects.filter(c_category__exact=4, c_item_id__exact=qid).count()
    return num


# 　获取文章详情 .2
def article_detail(qid):
    mid = int(qid)
    det = PzEquipment.objects.get(e_id__exact=mid)
    return det


# 新增文章 .9
def new_article(title, content, qid, url):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    article = PzEquipment(e_user=qid, e_title=title, e_content=content, e_release_time=date, e_url=url, e_read=0,
                          e_thumb=0)
    article.save()
    return article.e_id


# 修改文章 .7
def mod_article(aid, title, content, url):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    article = PzEquipment.objects.get(e_id__exact=int(aid))
    article.e_title = title
    article.e_content = content
    article.e_url = url
    article.e_release_time = date
    article.save()
    return article.e_id


# 文章的支持 .4
def thumbup_add(item):
    obj = PzEquipment.objects.get(e_id__exact=int(item))
    obj.e_thumb = int(obj.e_thumb) + 1
    obj.save()


# 文章的支持 .4
def thumbup_ant(item):
    obj = PzEquipment.objects.get(e_id__exact=int(item))
    obj.e_thumb = int(obj.e_thumb) - 1
    obj.save()


# 阅读数 .4
def read_num(item):
    obj = PzEquipment.objects.get(e_id__exact=int(item))
    obj.e_read = int(obj.e_read) + 1
    obj.save()


# 删除文章 .2
def deleting(item):
    PzEquipment.objects.get(e_id__exact=int(item)).delete()


# 文章详情 .7
def get_detail(item):
    det = PzEquipment.objects.get(e_id__exact=int(item))
    my_detail = {'a_id': det.e_id, 'a_title': det.e_title,
                 'a_content': det.e_content, 'a_cat': 4, 'a_url': det.e_url}
    return my_detail
