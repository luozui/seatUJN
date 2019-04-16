# !/usr/bin/env python
# coding=utf-8
__author__ = 'lepecoder'
__time__ = '2018-3-17'

import time
import requests
import json
import sys
from common import get_token, get_url


def checkin(token):
    url = 'http://seatlib.hpu.edu.cn/rest/v2/checkIn?token='
    checkin_url = url+token
    header = {'X-Forwarded-For': '10.167.135.34'}
    message = requests.get(checkin_url,headers=header)
    print(message.text)
    #r = get_url(url=url + token)
    # r = requests.get(url=url + token)
    #print(r.text + '\n')




if __name__ == '__main__':
    if sys.argv.__len__() <= 1:
        print("请传入配置文件名称")
        sys.exit()
    filename = sys.argv[1]
    # 打印开始时间
    start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + start + '-----------------------')
    f = open(sys.path[0] + '/' + filename, 'r', encoding='utf8')
    info = json.load(f)
    for i in info['stu']:
        print(i['name'])
        token1 = get_token(i['username'], i['password'])
        checkin(token1)
    # 打印结束时间
    end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + end + '-----------------------')
