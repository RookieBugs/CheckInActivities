# -*- coding: utf-8 -*-
"""
#  SMZDMApp.py
Description :
@Author     : Jianfeng
@Date       : 2018/2/28
@Software   : PyCharm
"""
import requests
import time


class SmzdmAPP:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'smzdm_android_V8.3.2 rv:415 (MI MAX;Android7.0;zh)smzdmapp',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 抽奖需要使用这个Referer
            'Referer': 'https://h5.smzdm.com/user/lottery/checkin'
        }

    def smzdm(self, sess):
        hosts = 'https://api.smzdm.com'
        checkin_url = hosts + '/v1/user/checkin'
        userinfo_url = hosts + '/v1/user/info'
        lottery_url = 'https://h5.smzdm.com/user/lottery/ajax_draw'

        cookies_ = {
            'sess': sess,
            'device_smzdm_version': '8.3.2',
            'device_smzdm': 'android'
        }

        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies_)
        try:
            checkin_req = self.session.post(checkin_url, headers=self.headers)
            checkin_msg = '签到结果：' + checkin_req.json()['error_msg'] + '\n'
            lottery_req = self.session.post(lottery_url, headers=self.headers)
            lottery_msg = '抽奖结果：' + lottery_req.json()['error_msg'] + '\n'
            userinfo_req = self.session.post(userinfo_url, headers=self.headers)
            old_jf = userinfo_req.json()['data']['meta']['cpoints']
            old_jy = userinfo_req.json()['data']['meta']['cexperience']
            old_jb = userinfo_req.json()['data']['meta']['cgold']
            userinfo = '金币：' + old_jb + '\n经验：' + old_jy + '\n积分：' + old_jf + '\n'
            # cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            content = checkin_msg + lottery_msg + userinfo
            print(content)
            return content
        except requests.exceptions.RequestException as e:
            content = 'SMZDM签到失败：' + str(e) + '\n'
            print(content)
            return content