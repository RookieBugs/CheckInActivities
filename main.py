# -*- coding: utf-8 -*-
"""
#  main.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/11
@Software   : PyCharm
"""

import os
import time
from base64 import b64encode
from libs.encrypto import pad_randomstr, rsa_encrypt
from libs.sendmail import SendEmail
from apps.ChinaUnicom import ChinaUnicomApp

receiver_mail = os.getenv('receive')
mobile = os.getenv('Unicom_mobile')
mobilepwd = os.getenv('Unicom_pwd')

PUB_KEY = ('-----BEGIN PUBLIC KEY-----\n'
           'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6'
           'FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9'
           'NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0Srctg'
           'aqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB\n'
           '-----END PUBLIC KEY-----')

username = b64encode(rsa_encrypt(PUB_KEY, pad_randomstr(mobile, size=6)))
password = b64encode(rsa_encrypt(PUB_KEY, pad_randomstr(mobilepwd, size=6)))

unicom = ChinaUnicomApp()
print('进行登陆...')
loginFlag, loginContent = unicom.login(username, password)
print('进行签到...')
signininFlag, signinContent = unicom.signin()

date = time.strftime("%Y-%m-%d", time.localtime())
# 发送邮件
if loginFlag and signininFlag:
    mailtitle = date + '联通APP自动签到任务成功'
else:
    mailtitle = date + '联通APP自动签到任务失败'
mailcontent = loginContent + signinContent
SendEmail.send_mail(mailtitle, mailcontent)
print('签到完成')

