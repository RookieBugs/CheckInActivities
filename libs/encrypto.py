# -*- coding: utf-8 -*-
"""
#  encrypto.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/11
@Software   : PyCharm
"""
import random
import base64
import binascii
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from builtins import chr
from builtins import int
from builtins import range
from builtins import str


'''====ChinaUnicom 加密算法===='''
def pad_randomstr_CU(text, size=6):
    chars = '0123456789'
    randstr = ''.join(random.choice(chars) for _ in range(size))
    if isinstance(text, bytes):
        text = str(text, 'utf-8')
    return '{0}{1}'.format(text, randstr)


def rsa_encrypt_CU(pub_key, message):
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


'''====CloudMusic RSA AES加密算法===='''
def aesEncrypt_CM(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode()


def rsaEncrypt_CM(text, pubKey, modulus):
    text = text[::-1].encode()
    rs = int(binascii.hexlify(text), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


