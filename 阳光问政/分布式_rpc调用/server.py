# -*- coding:utf-8 -*-
"""这是通用云服务端爬虫"""
import time
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

import requests

header = {
            'User-Agent': 'googlespider',
            'Content-Encoding': 'gzip',
            'X-Forwarded-For': '202.101.43.22',
        }

# 网络请求最大超时时间
TIMEOUT = 100
# 网络请求间隔时间 秒
TIME_SLEEP = 1


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def text_requests(url):
    """定义爬虫网络请求方法"""
    time.sleep(TIME_SLEEP)
    r = requests.get(
        url=url,
        headers=header,
        timeout=TIMEOUT
    )
    if r.status_code != 200:
        raise Exception('状态码{}'.format(r.status_code))
    else:
        pass

    return r.text


def gb2312_requests(url):
    """定义爬虫gb2312解码网页"""
    r = requests.get(
        url=url,
        headers=header,
        timeout=TIMEOUT
    )
    return r.content.decode("gb2312", "ignore")


if __name__ == '__main__':
    # 使用这个会让add函数始终只能同时处理一件事，必须等前一件事情做完才能接新任务
    # rpc_server = SimpleXMLRPCServer(('0.0.0.0', 1234))

    # 支持异步并行接受任务
    rpc_server = ThreadXMLRPCServer(('0.0.0.0', 1234))
    print("Listening on port 1234...")
    rpc_server.register_function(text_requests)
    rpc_server.register_function(gb2312_requests)
    rpc_server.serve_forever()



