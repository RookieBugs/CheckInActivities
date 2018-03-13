# -*- coding: utf-8 -*-
"""
#  ChinaUnicom.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/3
@Software   : PyCharm
"""
import requests
import time

class ChinaUnicomApp:
    def __init__(self):
        # super().__init__()
        self.session = requests.Session()
        self.headers = {
            'Host': 'm.client.10010.com',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'ChinaUnicom4.x/70 CFNetwork/811.5.4 Darwin/16.7.0',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate',
        }

    def login(self, username, password):
        cur_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.data = {
            'version': 'iphone_c@5.7',
            'mobile': username,
            'netWay': 'wifi',
            'isRemberPwd': 'true',
            'appId': '81740c90c669bda467dec2d09551b684e4e61006d6caebe41a45689995edc187',
            'deviceId': 'c65f20c8d6d2136065aa52a56ff80e8d325084b9d43aaa5d7a06e2f22894005d',
            'pip': '',
            'password': password,
            'deviceOS': '10.3.3',
            'deviceBrand': 'iphone',
            'deviceModel': 'iPhone',
            'keyVersion': '1',
            'deviceCode': 'EE0D86F7-79C1-42CF-8D63-543EC7F1DCC3',
        }

        login_url = 'http://m.client.10010.com/mobileService/login.htm'
        login_req = self.session.post(login_url, headers=self.headers, data=self.data)
        if login_req.json()['code'] == '0':
            content_login = cur_time1 + ' APP登陆成功...\n'
            return True, content_login
        else:
            print(cur_time1 + ' APP登陆失败...')
            content_login = cur_time1 + '  自动签到任务失败\n' + '错误原因：APP登陆失败...\n'
            return False, content_login

    def signin(self):
        try:
            cur_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.headers['Host'] = 'act.10010.com'
    #        cookie = self.session.cookies
            token = '?token=' + self.session.cookies.get('a_token', '')
            # 进入每日签到活动, cookies=self.session.cookies
            query_url = 'http://act.10010.com/SigninApp/signin/querySigninActivity.htm'
            self.session.get(url=query_url+token, headers=self.headers)
            # 检查是否已签到
            isSignin_url = 'http://act.10010.com/SigninApp/signin/rewardReminder.do'
            isSignin_req = self.session.post(url=isSignin_url, headers=self.headers)
            # 进行签到/取消签到
            signin_url = 'http://act.10010.com/SigninApp/signin/daySign.do'
            if int(isSignin_req.json()['todayIsSignin']):
                signin_req = self.session.post(url=signin_url)
                dailyCoin = signin_req.json()['prizeCount']
                print('今日获得金币：' + dailyCoin)
            else:
                dailyCoin = '今日已签到过'
                print(dailyCoin)
            # 获取总金币
            gold_url = 'http://act.10010.com/SigninApp/signin/goldTotal.do'
            gold_req = self.session.post(url=gold_url)
            totalCoin = gold_req.json()['goldTotal']
            # 获取签到历史
            querySignin_url = 'http://act.10010.com/SigninApp/mySignin/querySignin.do'
            querySignin_req = self.session.post(url=querySignin_url)
            continuCount = querySignin_req.json()['continuCount']
            signinDateList = ', '.join(querySignin_req.json()['signinDateList'])
            content_signin = '连续签到天数：' + continuCount + '\n' + '今日获得金币：' + dailyCoin + '\n' + '签到获得总金币：' + totalCoin + '\n' + '签到历史：' + signinDateList
            print(cur_time2 + ' APP签到成功...\n' + content_signin)
            return True, content_signin
        except Exception as err:
            print(cur_time2 + ' APP签到失败...\n失败原因：' + str(err))
            content_signin = 'APP签到失败' + str(err)
            return False, content_signin

