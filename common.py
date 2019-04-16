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
       {"status":"success","data":[{"roomId":12,"room":"一层大厅","floor":1,"reserved":0,"inUse":4,"away":0,"totalSeats":169,"free":165},{"roomId":11,"room":"朗读亭","floor":2,"reserved":0,"inUse":0,"away":0,"totalSeats":1,"free":1},{"roomId":3,"room":"三楼天井区","floor":3,"reserved":0,"inUse":40,"away":0,"totalSeats":40,"free":0},{"roomId":4,"room":"四楼天井区","floor":4,"reserved":1,"inUse":39,"away":0,"totalSeats":40,"free":0},{"roomId":1,"room":"五楼天井区","floor":5,"reserved":1,"inUse":74,"away":1,"totalSeats":80,"free":4},{"roomId":6,"room":"五楼教师研究生阅览室","floor":5,"reserved":0,"inUse":0,"away":0,"totalSeats":32,"free":0},{"roomId":2,"room":"五楼自习区","floor":5,"reserved":3,"inUse":242,"away":0,"totalSeats":256,"free":10},{"roomId":5,"room":"六楼自习区","floor":6,"reserved":1,"inUse":240,"away":0,"totalSeats":312,"free":70}],"message":"","code":"0"}
"""
ROOM = json.loads(ROOM)
ROOM = ROOM['data']
max_retry = 8  # 连接重试次数


def get_seat_id(loc, token):
    print("得到座位号ID...")
    local_room = loc[:-3]
    local_seat = loc[-3:]
    print(local_room, local_seat)
    room_id = [x for x in ROOM if x["room"] == local_room][0]['roomId']
    room_layer_url = 'http://seatlib.hpu.edu.cn/rest/v2/room/layoutByDate/' + str(room_id) + '/2017-01-2' \
                                                                                          '2?token=' + token
    r = get_url(room_layer_url)
    try:
        layer = json.loads(r.text)
    except:
        return -1
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
    url = 'http://seatlib.hpu.edu.cn/rest/auth'
    param = {
        'username': username,
        'password': password
    }
    r = get_url(url, param)

    try:
        resp = json.loads(r.text)
    except:
        return -1
    while resp['message'] == 'System Maintenance':
        print("系统维护中,等待10秒重试")
        time.sleep(10)
        r = get_url(url, param)

        try:
            resp = json.loads(r.text)
        except:
            return -1
    if resp['status'] == 'fail':
        print(username + '   ' + r.text)
        return -1
    else:
        return resp['data']['token']
