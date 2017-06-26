# -*- coding: utf-8 -*-
import random, base64
from hashlib import sha1


def crypt(data, key):
    """RC4 algorithm"""
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))

    return ''.join(out)


def tencode(data, key, encode=base64.b64encode, salt_length=16):
    """RC4 encryption with random salt and final encoding"""
    salt = ''
    for n in range(salt_length):
        salt += chr(random.randrange(256))
    data = salt + crypt(data, sha1(key + salt).digest())
    if encode:
        data = encode(data)
    return data


def tdecode(data, key, decode=base64.b64decode, salt_length=16):
    """RC4 decryption of encoded data"""
    if decode:
        data = decode(data)
    salt = data[:salt_length]
    return crypt(data[salt_length:], sha1(key + salt).digest())


#定义好的RC4加解密函数：
def rc4encode(data):
    if data != None and data != '':
        key = "pzone23748218946"
        return tencode(data=data, key=key)
    return None

def rc4decode(data):
    if data != None and data != '':
        key = "pzone23748218946"
        return tdecode(data=data, key=key)
    return None


    # if __name__=='__main__':
    #     # 需要加密的数据
    #     data = 'hello python 爱的实打实大师大师大师的发送到发送到'
    #     # 密钥
    #     key = '123456'

    #     # 加码
    #     encoded_data = tencode(data=data, key=key)
    #     print encoded_data
    #     # 解码
    #     decoded_data = tdecode(data=encoded_data, key=key)
    #     print decoded_data
