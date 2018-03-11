# -*- coding: utf-8 -*-
"""
#  encrypto.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/11
@Software   : PyCharm
"""
import random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

def pad_randomstr(text, size=6):
    chars = '0123456789'
    randstr = ''.join(random.choice(chars) for _ in range(size))
    if isinstance(text, bytes):
        text = str(text, 'utf-8')
    return '{0}{1}'.format(text, randstr)


def rsa_encrypt(pub_key, message):
    if isinstance(message, str):
        message = bytes(message, 'utf-8')
    # RSA/ECB/PKCS1Padding
    # 128字节一次
    ret = list()
    input_text = message[:128]
    while input_text:
        key = RSA.importKey(pub_key)
        cipher = PKCS1_v1_5.new(key)
        ret.append(cipher.encrypt(input_text))
        message = message[128:]
        input_text = message[:128]
    return b''.join(ret)