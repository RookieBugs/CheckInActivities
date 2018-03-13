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
from libs.encrypto import rsa_encrypt_CU,pad_randomstr_CU
from libs.sendmail import SendEmail
from apps.ChinaUnicom import ChinaUnicomApp
from apps.NetEaseCloudMusic import CloudMusic


receiver_mail = os.getenv('receive')
mobile = os.getenv('Unicom_mobile')
mobilepwd = os.getenv('Unicom_pwd')
NetEaseAccount = os.getenv('NetEase_account')
NetEasePwd = os.getenv('NetEase_pwd')


def unicomCheckin():
    pubKey_CU = ('-----BEGIN PUBLIC KEY-----\n'
                 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6'
                 'FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9'
                 'NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0Srctg'
                 'aqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB\n'
                 '-----END PUBLIC KEY-----')
    username_CU = b64encode(rsa_encrypt_CU(pubKey_CU, pad_randomstr_CU(mobile, size=6)))
    password_CU = b64encode(rsa_encrypt_CU(pubKey_CU, pad_randomstr_CU(mobilepwd, size=6)))

    unicom = ChinaUnicomApp()
    loginFlag, loginContent = unicom.login_CU(username_CU, password_CU)
    signininFlag, signinContent = unicom.signin_CU()
    mailcontent_CU = loginContent + signinContent + '\n\n'
    return mailcontent_CU


def cloudmusicCheckin():
    cloudmusic = CloudMusic()
    cloudmusic.login_CM(NetEaseAccount, NetEasePwd)
    time.sleep(1)
    # 移动端签到 0
    signinContentMo = cloudmusic.daily_signin_CM(0)
    time.sleep(1)
    # PC端签到 1
    signinContentPC = cloudmusic.daily_signin_CM(1)
    mailcontent_CM = date + ' 网易云音乐签到：\n' +  signinContentMo + signinContentPC
    return mailcontent_CM


date = time.strftime("%Y-%m-%d", time.localtime())
print(date + ' 开始网易云音乐签到任务：\n')
mailcontent_CM = cloudmusicCheckin()
time.sleep(10)
print(date + ' 开始联通手机APP签到任务：\n')
mailcontent_CU = unicomCheckin()
# 发送邮件
mailtitle = date + ' 自动签到任务报告'
mailcontent = mailcontent_CU + mailcontent_CM
# print('邮件内容')
# print(mailtitle)
# print(mailcontent)
SendEmail.send_mail(mailtitle, mailcontent)
print('任务结束')

