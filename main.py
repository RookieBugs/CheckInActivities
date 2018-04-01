# -*- coding: utf-8 -*-
"""
#  main.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/11
@Software   : PyCharm
"""

import os
import sys
import time
from libs.sendmail import SendEmail
from apps.ChinaUnicom import ChinaUnicomApp
from apps.NetEaseCloudMusic import CloudMusic
from apps.SMZDMApp import SmzdmAPP


receiver_mail = os.getenv('receive')
mobile = os.getenv('Unicom_mobile')
mobilepwd = os.getenv('Unicom_pwd')
NetEaseAccount = os.getenv('NetEase_account')
NetEasePwd = os.getenv('NetEase_pwd')
SMZDMsess = os.getenv('SMZDM_sess')


def unicomCheckin():
    unicom = ChinaUnicomApp()
    loginFlag, loginContent = unicom.login_CU(mobile, mobilepwd)
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
    mailcontent_CM = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())\
                     + ' 网易云音乐签到：\n' +  signinContentMo + signinContentPC +'\n'
    return mailcontent_CM


def smzdmCheckin():
    content_SMZDM = SmzdmAPP().smzdm(SMZDMsess)
    content_SMZDM = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'SMZDM签到：\n' + content_SMZDM
    return content_SMZDM

if __name__=='__main__':
    try:
        date = time.strftime("%Y-%m-%d", time.localtime())
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 开始网易云音乐签到任务：\n')
        mailcontent_CM = cloudmusicCheckin()

        time.sleep(10)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 开始联通手机APP签到任务：\n')
        mailcontent_CU = unicomCheckin()

        time.sleep(10)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 开始什么值得买签到：\n')
        mailcontent_SM = smzdmCheckin()

        mailtitle = date + ' 自动签到任务报告'
        mailcontent = mailcontent_CU + mailcontent_CM + mailcontent_SM
        exitCode = 0
    except Exception as e:
        mailtitle = date + ' 自动签到任务出错'
        mailcontent = '签到异常，请查看travis-ci log\n' + str(e)
        exitCode = 1
        

    # 发送邮件
    SendEmail.send_mail(mailtitle, mailcontent)
    print('任务结束, exit code: ', exitCode)
    sys.exit(exitCode)
