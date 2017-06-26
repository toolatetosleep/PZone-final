# coding:utf-8
from django.http import HttpResponse
from encryption import rc4decode
import imghdr
import datetime
import random
import string
import os
import Image
import re


# 获取cookies中的username ，如果没有就返回None
def get_cookies(req, my_str):
    c_str = req.COOKIES.get(my_str, None)
    if c_str != "" and c_str is not None:
        username = rc4decode(c_str)
        return username
    return None


# 验证图片
def exam_pic(pic):
    # 验证图片的格式是不是JPG, PNG, GIF中的一种
    if pic:
        if imghdr.what(pic) != 'jpeg' and imghdr.what(pic) != 'gif' and imghdr.what(pic) != 'png':
            return False
        return True
    else:
        return False


# 重新命名图片
def name_pic():
    # 以当时时间加5位随机字母的形式返回文件名
    now_time = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    rmd_str = ''.join(random.sample(string.ascii_lowercase, 12))
    new_name = now_time + '_' + rmd_str
    return new_name


# 图片大小处理
def resize_pic(sort, infile, outfile):
    if sort == 1:
        # 1 为头像，0 为图像
        im = Image.open(infile)
        out = im.resize((130, 130), Image.ANTIALIAS)
        out.save(infile)
    else:
        im = Image.open(infile)
        (x, y) = im.size
        if x <= 750:
            outfile = infile
        else:
            x_s = 750
            y_s = y * x_s / x
            out = im.resize((x_s, y_s), Image.ANTIALIAS)
            out.save(outfile)
    return outfile


# 保存文件到服务器并返回文件路径
def store_pic(pic, path):
    if exam_pic(pic):
        name = name_pic()
        if pic and path and name:
            # 确定文件存放的路径
            if path == 'avatar':
                file_path = './upload/avatar/' + name + '.' + imghdr.what(pic)
                destination = open(os.path.join(file_path), 'wb+')
                # 分块写入文件
                for chunk in pic.chunks():
                    destination.write(chunk)
                destination.close()
                # 后处理，图片大小
                return resize_pic(1, file_path, file_path)
            else:
                file_path = './upload/images/' + name + '.' + imghdr.what(pic)
                file_path_original = './upload/origins/' + name + '_original.' + imghdr.what(pic)
                destination = open(os.path.join(file_path_original), 'wb+')
                # 分块写入文件
                for chunk in pic.chunks():
                    destination.write(chunk)
                destination.close()
                # 后处理，图片大小
                return resize_pic(0, file_path_original, file_path)
                # return file_path
        else:
            return None


# 用户下载文件
def download_file(src):
    def read_file(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    if re.findall(r'(.+)original(.+)', src):
        # print "original"
        pass
    else:
        # print "compressed"
        u = src.split("/")
        t = u[-1].split(".")
        del u[-1]
        u.append(t[0] + "_original." + t[1])
        n = "/".join(u)
        n = re.sub("images", "origins", n)
        response = HttpResponse(read_file('.' + n))
        response['Content-Type'] = 'application/octet-stream'
        return response
