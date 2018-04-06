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
from base64 import b64encode
from libs.encrypto import rsa_encrypt_CU,pad_randomstr_CU


pubKey_CU = ('-----BEGIN PUBLIC KEY-----\n'
                 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6'
                 'FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9'
                 'NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0Srctg'
                 'aqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB\n'
                 '-----END PUBLIC KEY-----')


class ChinaUnicomApp:
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'ChinaUnicom4.x/70 CFNetwork/811.5.4 Darwin/16.7.0',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate',
        }
        self.token = ''
        self.phoneNum = ''
        self.areaCode = ''
        

    def login_CU(self, username, password):
        self.phoneNum = username
        username_CU = b64encode(rsa_encrypt_CU(pubKey_CU, pad_randomstr_CU(username, size=6)))
        password_CU = b64encode(rsa_encrypt_CU(pubKey_CU, pad_randomstr_CU(password, size=6)))
        cur_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.headers['Host'] = 'm.client.10010.com'
        self.data = {
            'version': 'iphone_c@5.7',
            'mobile': username_CU,
            'netWay': 'wifi',
            'isRemberPwd': 'true',
            'appId': '81740c90c669bda467dec2d09551b684e4e61006d6caebe41a45689995edc187',
            'deviceId': 'c65f20c8d6d2136065aa52a56ff80e8d325084b9d43aaa5d7a06e2f22894005d',
            'pip': '',
            'password': password_CU,
            'deviceOS': '10.3.3',
            'deviceBrand': 'iphone',
            'deviceModel': 'iPhone',
            'keyVersion': '1',
            'deviceCode': 'EE0D86F7-79C1-42CF-8D63-543EC7F1DCC3',
        }

        login_url = 'http://m.client.10010.com/mobileService/login.htm'
        # Host 请求尝试次数
        n = 2
        while n:
            try:
                login_req = self.session.post(login_url, headers=self.headers, data=self.data)
                if login_req.json()['code'] == '0':
                    self.token = self.session.cookies.get('a_token', '')
                    self.areaCode = self.session.cookies.get('u_areaCode', '')
                    content_login = cur_time1 + ' 联通APP签到：\n'
                    return 1, content_login
                else:
                    print(cur_time1 + ' 联通APP登陆失败...')
                    content_login = cur_time1 + '  自动签到任务失败\n' + '错误原因：APP登陆失败...\n'
                    return 0, content_login
            except Exception as err:
                print(err)
                time.sleep(5)
                n -= 1
                print('尝试重复请求...')
                continue
        content_login = cur_time1 + '  自动签到任务失败\n' + '错误原因：二次 Host 请求失败...\n'
        return -1, content_login

    def signin_CU(self):
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
          
    def woTree(self):
        times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.headers['Host'] = 'm.client.10010.com'
        getAct_url = 'http://m.client.10010.com/mactivity/arborday/index'  # GET
        getAct = self.session.get(url=getAct_url, headers=self.headers)
        # TODO 分析html中的 <div class="jingyanzhi">

        data = {
            'url': getAct_url,
            'serviceCode': 'takeActivityInfo',
            'channel': 'mobileClient',
            'city': self.areaCode,
            'transId': times,
            'phoneNum': self.phoneNum,
        }
        takeAct_url = 'http://m.client.10010.com/freegift-interface/appUrlShare/takeActivityInfo'  # POST
        takeAct = self.session.post(url=takeAct_url, headers=self.headers, data=data)
        watering_url = 'http://m.client.10010.com/mactivity/arborday/arbor/1/0/1/grow'  # POST
        weed_url = 'http://m.client.10010.com/mactivity/arborday/arbor/1/1/1/grow'
        deinsec_url = 'http://m.client.10010.com/mactivity/arborday/arbor/1/2/1/grow'
        watering = self.session.post(url=watering_url, headers=self.headers)
        wateringStates = watering .json()['addedValue']
        weed = self.session.post(url=weed_url, headers=self.headers)
        weedStates = weed.json()['addedValue']
        deinsec = self.session.post(url=deinsec_url, headers=self.headers)
        deinsecStates = deinsec.json()['addedValue']

        content = "{} 沃之树：\n    浇水：{}次\n    除草：{}次\n    除虫：{}次\n".format(
            cur_time, wateringStates, weedStates, deinsecStates)
        print(content)
        return 1, content
