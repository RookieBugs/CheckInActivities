# -*- coding: utf-8 -*-
"""
#  sendmail.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/11
@Software   : PyCharm
"""
import os
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

mail_account = os.getenv('mail_account')
mail_pwd = os.getenv('mail_pwd')
receiver_mail = os.getenv('receive')


class SendEmail:
    def send_mail(mail_title=' ', mail_content=' '):
        try:
            host_server = 'smtp.zoho.com'
            sender_mail = mail_account + '@zoho.com'
            # ssl登录
            smtp = SMTP_SSL(host_server, 465)
            # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
            smtp.set_debuglevel(0)
            smtp.ehlo(host_server)
            smtp.login(mail_account, mail_pwd)
            # 发送邮件
            msg = MIMEText(mail_content, "plain", 'utf-8')
            msg["Subject"] = Header(mail_title, 'utf-8')
            msg["From"] = sender_mail
            msg["To"] = receiver_mail
            smtp.sendmail(sender_mail, receiver_mail, msg.as_string())
            smtp.quit()
            return True
        except Exception as err:
            print(err)
            return False
