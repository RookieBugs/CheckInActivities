# -*- coding: utf-8 -*-
"""
#  NetEaseCloudMusic.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/13
@Software   : PyCharm
"""
import re
import os
import requests
import json
import hashlib
import time
from libs.encrypto import aesEncrypt_CM, rsaEncrypt_CM


def createSecretKey(size):
    return ''.join([hex(x)[2:] for x in os.urandom(size)])[0:16]


def encrypted_request(text):
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7' \
              'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280' \
              '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932' \
              '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b' \
              '3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey_CM = '010001'
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt_CM(aesEncrypt_CM(text, nonce), secKey)
    encSecKey = rsaEncrypt_CM(secKey, pubKey_CM, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    return data


class CloudMusic:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }
        self.session.cookies = {'appver': '1.5.2'}
        self.session = requests.Session()


    #登陆
    def login_CM(self, username, password):
        pattern = re.compile(r'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$')
        if pattern.match(username):
            return self.phone_login_CM(username, password)
        web_url = 'http://music.163.com/weapi/login?csrf_token='
        text = {
            'username': username,
            'password': password,
            'rememberLogin': 'true'
        }
        data = encrypted_request(text)
        try:
            web_req = self.session.post(url=web_url, headers=self.headers, data=data, timeout=10)
            print('PC登陆成功\n')
            return web_req
        except requests.exceptions.RequestException as e:
            print('PC登陆失败： ' + str(e) + '\n')
            return {'code': 501}


    # 手机登录
    def phone_login_CM(self, username, password):
        phone_url = 'http://music.163.com/weapi/login/cellphone'
        text = {
            'phone': username,
            'password': hashlib.md5(password.encode()).hexdigest(),
            'rememberLogin': 'true'
        }
        data = encrypted_request(text)
        try:
            phone_req = self.session.post(url=phone_url, headers=self.headers, data=data, timeout=10)
            print('手机登陆成功')
            return phone_req
        except requests.exceptions.RequestException as e:
            print('手机登陆失败： ' + str(e) + '\n')
            return {'code': 501}


    # 每日签到
    def daily_signin_CM(self, type):
        #  PC:type = 1, mobile: type = 0
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        devices = '手机端', '移动端'
        sigin_url = 'http://music.163.com/weapi/point/dailyTask'
        text = {'type': type}
        data = encrypted_request(text)
        try:
            signin_req = self.session.post(url=sigin_url, headers=self.headers, data=data, timeout=10)
            code = signin_req.json()['code']
            if code not in (-2, 301):
                signinContent = cur_time + ' 网易云音乐' + devices[type] + '签到成功\n'
                print(signinContent)
            else:
                signinContent = cur_time + ' 网易云音乐' + devices[type] + '重复签到\n'
                print(signinContent)
        except requests.exceptions.RequestException as e:
            signinContent = cur_time + ' 网易云音乐' + devices[type] + '签到失败\n' + e + '\n'
            print(signinContent)
        return signinContent

