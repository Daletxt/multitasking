# -*- coding:utf-8 -*-
import re
import csv
import time
from random import choice
from xmlrpc.client import ServerProxy

from bs4 import BeautifulSoup


# 云服务端的ip:端口号
server_list = [
    "http://127.0.0.1:1234",
    "http://127.0.0.1:4321",
    # "http://x.x.x.x:1234",
]


def get_content(number):
    """
    用rpc调用云端服务器进行访问页面，返回的是str，不能返回request对象，
    所以r.url  r.status_code等方法 只能在云端使用然后返回给客户端，所以云端要处理这些问题
    """
    remote_addr = choice(server_list)
    print(remote_addr)
    server = ServerProxy(remote_addr)
    response = server.gb2312_requests('http://wz.sun0769.com/index.php/question/report?page=%d' % number)
    content = response
    re_str = '共(\d+)条记录'
    regex = re.compile(re_str)
    page = re.findall(regex, content)[0]
    time.sleep(3)
    return content, eval(page)


def get_data(content):
    """这以下部分是 普通 版本的方法"""
    soup = BeautifulSoup(content)
    # type_list = soup.find_all('a', class_="red14")
    title_list = soup.find_all('a', class_='news14')
    # type_str_list = []
    title_str_list = []
    # for type1 in type_list:
    #     print(type1)
    #     print('-'*50)
    #     type_str = type1.string.replace('[', '').replace(']', '')
    #     print(type_str)
    #     print('='*50)
    #     type_str_list.append(type_str)
    for title in title_list:
        title_str_list.append(title['title'])
    return title_str_list


def down_data(title):
    with open('question.csv', 'a') as q:
        csv_file = csv.writer(q)
        csv_file.writerow(title)
    print('该页写入完成')


def main():

    number = 0
    while True:
        content, page = get_content(number)
        title_list = get_data(content)
        down_data(title_list)
        number += 30
        if (number - page) > 0:
            break


if __name__ == '__main__':
    main()
