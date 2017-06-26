# coding:utf-8
from pz_picture.models import PzPicture, PzComment
from django.utils import timezone


# 获取分页记录 .2
def get_page(page, count):
    i = page * count - count
    my_list = PzPicture.objects.order_by("-p_id")[i: i + count]
    return my_list


# 获取分页记录 .2 用户
def get_page_u(page, count, uid):
    i = page * count - count
    my_list = PzPicture.objects.filter(p_user__exact=uid).order_by("-p_id")[i: i + count]
    return my_list


# 计算分页并返回总页面数 .1
def count_page(count):
    my_list = PzPicture.objects.all().count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 计算分页并返回总页面数 .1 用户
def count_page_u(count, uid):
    my_list = PzPicture.objects.filter(p_user__exact=uid).count()
    my_all_page = my_list / count
    temp = my_list % count
    if temp != 0:
        my_all_page += 1
    return my_all_page


# 获取评论数 .1
def get_com_count(qid):
    # 评论的具体文章的种类（1头条、2技巧、3佳作、4器材）
    num = PzComment.objects.filter(c_category__exact=3, c_item_id__exact=qid).count()
    return num


# 　获取文章详情 .2
def article_detail(qid):
    mid = int(qid)
    det = PzPicture.objects.get(p_id__exact=mid)
    return det


# 新增文章 .9
def new_article(title, content, qid, url):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    article = PzPicture(p_user=qid, p_title=title, p_content=content, p_release_time=date, p_url=url, p_read=0,
                        p_thumb=0)
    article.save()
    return article.p_id


# 修改文章 .7
def mod_article(aid, title, content, url):
    date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    article = PzPicture.objects.get(p_id__exact=int(aid))
    article.p_title = title
    article.p_content = content
    article.p_url = url
    article.p_release_time = date
    article.save()
    return article.p_id


# 文章的支持 .4
def thumbup_add(item):
    obj = PzPicture.objects.get(p_id__exact=int(item))
    obj.p_thumb = int(obj.p_thumb) + 1
    obj.save()


# 文章的支持 .4
def thumbup_ant(item):
    obj = PzPicture.objects.get(p_id__exact=int(item))
    obj.p_thumb = int(obj.p_thumb) - 1
    obj.save()


# 阅读数 .4
def read_num(item):
    obj = PzPicture.objects.get(p_id__exact=int(item))
    obj.p_read = int(obj.p_read) + 1
    obj.save()


# 删除文章 .2
def deleting(item):
    PzPicture.objects.get(p_id__exact=int(item)).delete()


# 文章详情 .7
def get_detail(item):
    det = PzPicture.objects.get(p_id__exact=int(item))
    my_detail = {'a_id': det.p_id, 'a_title': det.p_title,
                 'a_content': det.p_content, 'a_cat': 3, 'a_url': det.p_url}
    return my_detail
