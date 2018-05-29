# !/usr/bin/env python
# coding=utf-8
import requests
import json
import time
import sys
from common import get_token, get_seat_id, get_url, post_url

'''
如果有快到时间的预约，
1. 取消当前预约
2. 重新预约后面的时间
'''
max_retry = 5


def get_local_date():
    localtime = time.localtime(time.time())
    ans = str(localtime.tm_year) + '-' + \
        str(localtime.tm_mon) + '-' + str(localtime.tm_mday)
    return ans


nowDate = get_local_date()
# nowHour = int(time.strftime("%H", time.localtime()))
nowMinutes = time.localtime()[3] * 60 + time.localtime()[4]

'''
## 我的预约
http://seat.ujn.edu.cn/rest/v2/history/1/1000?token=K70M9XXYLL01204845

最多1000条记录
```json
{
    "status": "success",
    "data": {
        "reservations": [
            {
                "id": 3669317,
                "date": "2018-1-22",
                "begin": "07:00",
                "end": "11:00",
                "awayBegin": null,
                "awayEnd": null,
                "loc": "主校区2层213室区第一阅览室001号",
                "stat": "CANCEL"
            },
            {
                "id": 3669318,
                "date": "2018-1-22",
                "begin": "07:00",
                "end": "11:00",
                "awayBegin": null,
                "awayEnd": null,
                "loc": "主校区2层213室区第一阅览室001号",
                "stat": "CANCEL"
            }
            }
'''


def get_history(token):
    # 查看我的预约
    # 返回-1 则出错
    url = 'http://seat.ujn.edu.cn/rest/v2/history/1/1000?token=' + token
    r = get_url(url)
    resp = json.loads(r.text)
    if resp['status'] == 'fail':
        print('查看预约失败' + r.text)
        return -1
    # print(resp)
    need_free = False
    for raw in resp['data']['reservations']:
        minutes = int(raw['begin'][:2]) * 60 + int(raw['begin'][3:])
        # 预约状态+当天+预约开始15分钟内
        if raw['stat'] == 'RESERVE' and raw['date'] == nowDate and nowMinutes >= minutes and nowMinutes - minutes < 15:
            print('需要续约')
            need_free = True
            # cancle the reservation
            # http://seat.ujn.edu.cn/rest/v2/cancel/3669325?token=75FG9DTUZA01210118
            cancleUrl = 'http://seat.ujn.edu.cn/rest/v2/cancel/' + \
                str(raw['id']) + '?token=' + token
            r1 = get_url(cancleUrl)
            resp1 = json.loads(r1.text)
            if resp1['status'] == 'fail':
                print('取消当前预约失败' + r1.text)
                return -1
            # 预约后面的时间
            # http://seat.ujn.edu.cn/rest/v2/freeBook
            # POST `token=HLIU9P4HYW01214703&startTime=960&endTime=1200&seat=15343&date=2018-01-21`
            freeBookUrl = 'http://seat.ujn.edu.cn/rest/v2/freeBook'
            seat = get_seat_id(raw['loc'][10:-1], token)
            if seat == -1:
                print("查找座位" + raw['loc'] + '失败')
                return -1
            param = {
                'token': token,
                'startTime': str((int(raw['begin'][:2]) + 1) * 60 + int(raw['begin'][3:])),
                'endTime': str(int(raw['end'][:2]) * 60 + int(raw['end'][3:])),
                'seat': seat,
                'date': nowDate
            }
            r = post_url(freeBookUrl, param)
            resp2 = json.loads(r.text)
            if resp2['status'] == 'fail':
                print('续约失败  ，' + r.text)
                return -1
            print('续约成功 ' + r.text)
            break
    if not need_free:
        print("无需续约")
    return 1


if __name__ == '__main__':
    if sys.argv.__len__() <= 1:
        print("请传入配置文件名称")
        sys.exit()
    filename = sys.argv[1]
    # filename = "configSeatDaemon.log"
    # 打印开始时间
    start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + start + '-----------------------')
    f = open(sys.path[0] + '/' + filename, 'r', encoding='utf8')
    info = json.load(f)
    for i in info['stu']:
        token1 = get_token(i['username'], i['password'])
        if token1 != -1:
            print(i['username'] + '登陆成功')
            status = get_history(token1)
    # 打印结束时间
    end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('----------------------' + end + '-----------------------')
