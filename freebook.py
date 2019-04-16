# !/usr/bin/env python3 -u
# coding=utf-8

import json
import time
import sys
from common import get_seat_id, get_token, post_url

# 配置文件作为参数传入预约第二天的座位


max_retry = 5  # 连接重试次数
early_times = 0  # 未到系统开放时间尝试预约次数计数器
'''
http://seat.ujn.edu.cn/rest/auth?username=xxx&password=xxx
获取token

{"status":"success","data":{"token":"T58UTCARF601204212"},"code":"0","message":""}
{"status":"fail","code":"13","message":"登录失败: 密码不正确","data":null}

http://seat.ujn.edu.cn/rest/v2/freeBook
POST `token=HLIU9P4HYW01214703&startTime=960&endTime=1200&seat=15343&date=2018-01-21`
'''


def freeBook(token, startTime, endTime, seat):
    # 预约座位
    print("预约座位")
    tomorrow = time.strftime("%Y-%m-%d", time.localtime(86400 + time.time()))
    url = 'http://seatlib.hpu.edu.cn/rest/v2/freeBook'
    para = {
        'token': token,
        'startTime': startTime,
        'endTime': endTime,
        'seat': seat,
        'date': tomorrow
    }

    r = post_url(url, para)

    try:
        resp = json.loads(r.text)
    except:
        return -1

    early_times = 0
    while resp['message'] == '系统可预约时间为 05:00 ~ 23:00':
        print(resp['message'])
        print('还未到预定时间，请等待 2秒')
        time.sleep(2)
        early_times += 1
        print('已经尝试重连 %d 次' % early_times)
        r = post_url(url, para)
        try:
            resp = json.loads(r.text)
        except:
            return -1

    if resp['status'] == 'fail':

        print("预约失败#############" + resp['message'])
        return -1

    else:
        return 1


if __name__ == '__main__':
    if sys.argv.__len__() <= 1:
        print("请传入配置文件名称")
        sys.exit()
    filename = sys.argv[1]
    # 打印开始时间
    start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + start + '----start-------------------')
    f = open(sys.path[0] + '/' + filename, 'r', encoding='utf8')
    info = json.load(f)
    # print(info)
    # print(len(info['stu']))
    for i in info['stu']:
        if i['enable'] == 'false':
            continue
        print("正在为 %s 预约 %s" % (i['name'], i['seat']))
        time.sleep(3)
        token = get_token(i['username'], i['password'])
        status = 0
        if token != -1:
            seat_id = get_seat_id(i['seat'], token)
            if seat_id != -1:
                status = freeBook(token, i['startTime'], i['endTime'], seat_id)
            else:
                status = -1
                print("得到座位号失败")
                continue
        else:
            print("登录失败")
            continue
        if token != -1 and status != -1:
            print(i['name'] + ' 成功预约 ' + i['seat'])
            print("")
        else:
            print(i['name'] + ' 预约失败')
            print("")

            # 打印结束时间
    end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + end + '----end-------------------\n\n\n')
