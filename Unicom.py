# -*- coding: utf-8 -*-
"""
Description :
@Author     : RookieBugs
@Date       : 2018/3/3
@Software   : PyCharm
"""
import os
import requests
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import time

mail_account = os.getenv('mail_account') or ''
mail_pwd = os.getenv('mail_pwd') or ''
mobile = os.getenv('Unicom_mobile') or ''
pwd = os.getenv('Unicom_pwd') or ''

def send_mail(mail_title='', mail_content=''):
    host_server = 'smtp.163.com'
    sender_mail = mail_account + '@163.com'
    receiver_mail = '85619217@qq.com'
    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(mail_account, mail_pwd)
    #发送邮件
    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_mail
    msg["To"] = receiver_mail
    smtp.sendmail(sender_mail, receiver_mail, msg.as_string())
    smtp.quit()
    return True

headers = {
    'Host': 'm.client.10010.com',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    # 'Cookie': 'clientid=51|620; Hm_lvt_9208c8c641bfb0560ce7884c36938d9d=1519813185; WT_FPC=id=20ac3a346b79ca023971519813184878:lv=1519813344656:ss=1519813184878',
    'User-Agent': 'ChinaUnicom4.x/70 CFNetwork/811.5.4 Darwin/16.7.0',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
}
data = {
    'version':	'iphone_c@5.7',
    'mobile': mobile,
    'netWay': 'wifi',
    'isRemberPwd': 'true',
    'appId': 'ChinaunicomMobileBusiness',
    'deviceId': 'c65f20c8d6d2136065aa52a56ff80e8d325084b9d43aaa5d7a06e2f22894005d',
    'pip': '',
    'password': pwd,
    'deviceOS': '10.3.3',
    'deviceBrand': 'iphone',
    'deviceModel': 'iPhone',
    'keyVersion': '1',
    'deviceCode': 'EE0D86F7-79C1-42CF-8D63-543EC7F1DCC3',
}

login_url = 'http://m.client.10010.com/mobileService/login.htm'
signin_url = 'http://m.client.10010.com/SigninApp/signin/querySigninActivity.htm'
isSignin_url = 'http://m.client.10010.com/SigninApp/signin/rewardReminder.do?vesion=0.8273173418467968'
daySignin_url = 'http://m.client.10010.com/SigninApp/signin/daySign.do'
gold_url = 'http://m.client.10010.com/SigninApp/signin/goldTotal.do?vesion=0.17079171583464015'

cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
cur_date = time.strftime('%Y-%m-%d',time.localtime())
session = requests.Session()

try:
    login_req = session.post(url=login_url, headers=headers, data=data)

    token = '?token=' + login_req.cookies['a_token']
    signin_req = session.get(url=signin_url + token)
    cur_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    isSignin_req = session.post(url=isSignin_url)
    ebcount = isSignin_req.json()['ebCount']
    if int(isSignin_req.json()['todayIsSignin']):
        cur_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dailySignin_req = session.post(url=daySignin_url)
        dailyCoin = dailySignin_req.json()['message']
        print('今日获得金币：' + dailyCoin)

    else:
        cur_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dailyCoin = 'unknown'
        print('今日已签到...')

    cur_time3 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gold_req = session.post(url=gold_url)
    totalCoin = gold_req.json()['goldTotal']
    print('总金币：' + totalCoin)

    mail_content = cur_time1 + '  连续签到天数：' + ebcount + '\n' + cur_time2 + '  今日获得金币：' + dailyCoin + '\n' + cur_time3 + '  签到获得总金币：' + totalCoin
    if send_mail(mail_content=mail_content, mail_title=cur_date + '：联通手机营业厅APP自动签到成功'):
        print('邮件发送成功')
    else:
        print('邮件发送失败')
except Exception as err:
    print('自动签到任务失败')
    if send_mail(mail_content=cur_time + '  自动签到任务失败\n' + '错误原因：' + str(err), mail_title=cur_date + '：联通手机营业厅APP自动签到失败'):
        print('邮件发送成功')
    else:
        print('邮件发送失败')