import requests
import re
from gevent import monkey
import gevent
from bs4 import BeautifulSoup


monkey.patch_all()
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }


def get_page():
    response = requests.get('http://wz.sun0769.com/index.php/question/report?page=0', headers=headers)
    content = response.content.decode("gb2312", "ignore")
    re_str = '共(\d+)条记录'
    regex = re.compile(re_str)
    page = re.findall(regex, content)[0]
    return eval(page)


def get_content(url_list):
    for url in url_list:
        response = requests.get(url, headers=headers)
        gevent.sleep(3)
        content = response.content.decode('gb2312', 'ignore')
        get_data(content)


def get_data(content):
    soup = BeautifulSoup(content)
    title_list = soup.find_all('a', class_='news14')
    title_str_list = []
    for title in title_list:
        title_str_list.append(title['title'])
    down_data(title_str_list)


def down_data(title_list):
    # print(title_list)
    with open('geventquestion.txt', 'a') as q:
        q.write('\n'.join(title_list))
    print('该页写入完毕')


def main():
    page = get_page()
    url_list = []

    number = 0
    while True:
        url = 'http://wz.sun0769.com/index.php/question/report?page=%d' % number
        url_list.append(url)
        number += 30
        if (number - page) > 0:
            break

    xclist = [[], [], [], [], []]
    N = len(xclist)
    for i in range(len(url_list)):
        xclist[i % N].append(url_list[i])
    task_list = []
    for i in range(N):
        task_list.append(gevent.spawn(get_content, xclist[i]))
    gevent.joinall(task_list)


    # content = get_content(number)
    #
    # title_list = get_data(content)
    #
    # down_data(title_list)


if __name__ == '__main__':
    main()
