#!/usr/bin/env python3 -u
# coding=utf-8
import requests
import json
import requests.exceptions
import time

max_retry = 8  # 最大重试次数


def post_url(url, para, t_out=3):
    """
    构造post请求
    :param url:
    :param data:
    :param t_out:
    :return:
    """
    t = 0
    while t < max_retry:
        if t != 0:
            time.sleep(1)
        try:
            r = requests.post(url, data=para, timeout=4)
        except requests.exceptions.Timeout as e:
            print("freebook连接超时....")
            # print(str(e))
            t += 1
        except requests.exceptions.ConnectionError as e:
            print("网络异常")
            # print(str(e))
            t += 1
        except requests.exceptions.HTTPError as e:
            print("返回了不成功的状态码")
            # print(str(e))
            t += 1
        except Exception as e:
            print("出现了意料之外的错误")
            print(str(e))
            t += 1
        else:
            t = max_retry + 1
    if t == max_retry:
        print("超过最大重试次数")
        return -1
    else:
        return r


def get_url(url, parameters={}, t_out=3):
    """
    :param url:     get请求的连接
    :param t_out:   超时时间，默认3秒
    :param parameters: 参数
    :return:        response
    """

    t = 0
    while t < max_retry:
        if t != 0:
            time.sleep(1)
        try:
            r = requests.get(url, params=parameters, timeout=t_out)
        except requests.exceptions.Timeout as e:
            print("连接超时....")
            # print(str(e))
            t += 1
        except requests.exceptions.ConnectionError as e:
            print("网络异常")
            # print(str(e))
            t += 1
        except requests.exceptions.HTTPError as e:
            print("返回了不成功的状态码")
            # print(str(e))
            t += 1
        except Exception as e:
            print("出现了意料之外的错误")
            print(str(e))
            t += 1
        else:
            t = max_retry + 1
    if t == max_retry:
        print("超过最大重试次数")
        return -1
    else:
        return r

    # 座位转换


# from '第一阅览室001' to seat-id = 22558
ROOM = """ 
       {"status":"success","data":[{"roomId":41,"room":"第一阅览室","floor":2,"reserved":0,"inUse":0,"away":0,"totalSeats":136,"free":136},{"roomId":12,"room":"第二阅览室中区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":11,"room":"第二阅览室北区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":196,"free":196},{"roomId":13,"room":"第二阅览室南区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":172,"free":172},{"roomId":15,"room":"第十一阅览室中区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":14,"room":"第十一阅览室北区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":188,"free":188},{"roomId":16,"room":"第十一阅览室南区","floor":3,"reserved":0,"inUse":0,"away":0,"totalSeats":156,"free":156},{"roomId":18,"room":"第三阅览室中区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":17,"room":"第三阅览室北区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":148,"free":148},{"roomId":19,"room":"第三阅览室南区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":120,"free":120},{"roomId":21,"room":"第十阅览室中区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":22,"room":"第十阅览室南区","floor":4,"reserved":0,"inUse":0,"away":0,"totalSeats":164,"free":164},{"roomId":35,"room":"第九阅览室中区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":34,"room":"第九阅览室北区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":195,"free":195},{"roomId":36,"room":"第九阅览室南区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":172,"free":172},{"roomId":32,"room":"第四阅览室中区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":31,"room":"第四阅览室北区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":148,"free":148},{"roomId":33,"room":"第四阅览室南区","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":164,"free":164},{"roomId":38,"room":"第五阅览室中区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":8,"room":"第五阅览室北区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":59,"free":59},{"roomId":37,"room":"第五阅览室南区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":173,"free":173},{"roomId":47,"room":"第八阅览室中区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":9,"room":"第八阅览室北区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":204,"free":204},{"roomId":40,"room":"第八阅览室南区","floor":6,"reserved":0,"inUse":0,"away":0,"totalSeats":176,"free":176},{"roomId":27,"room":"第七阅览室中区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":46,"room":"第七阅览室北区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":132,"free":132},{"roomId":28,"room":"第七阅览室南区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":108,"free":108},{"roomId":24,"room":"第六阅览室中区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":48,"free":48},{"roomId":23,"room":"第六阅览室北区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":132,"free":132},{"roomId":25,"room":"第六阅览室南区","floor":7,"reserved":0,"inUse":0,"away":0,"totalSeats":108,"free":108}],"message":"","code":"0"}
"""
ROOM = json.loads(ROOM)
ROOM = ROOM['data']
max_retry = 8  # 连接重试次数


def get_seat_id(loc, token):
    print("得到座位号ID...")
    local_room = loc[:-3]
    local_seat = loc[-3:]
    room_id = [x for x in ROOM if x["room"] == local_room][0]['roomId']
    room_layer_url = 'http://seat.ujn.edu.cn/rest/v2/room/layoutByDate/' + str(room_id) + '/2017-01-2' \
                                                                                          '2?token=' + token
    r = get_url(room_layer_url)
    layer = json.loads(r.text)
    layer = layer['data']['layout']

    seat_id = [x for x in layer if layer[x]['type']
               == 'seat' and layer[x]['name'] == local_seat]
    if seat_id.__len__() == 0:
        print('找不到' + loc)
        return -1
    else:
        seat_id = layer[seat_id[0]]['id']
        return seat_id


def get_token(username, password):
    # 登录获取token
    print("正在登陆...")
    url = 'http://seat.ujn.edu.cn/rest/auth'
    param = {
        'username': username,
        'password': password
    }
    r = get_url(url, param)
    resp = json.loads(r.text)

    while resp['message'] == 'System Maintenance':
        print("系统维护中,等待10秒重试")
        time.sleep(10)
        r = get_url(url, param)
        resp = json.loads(r.text)

    if resp['status'] == 'fail':
        print(username + '   ' + r.text)
        return -1
    else:
        return resp['data']['token']
