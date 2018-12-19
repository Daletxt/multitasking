import requests
import re
from bs4 import BeautifulSoup
import multiprocessing
import time


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


def get_content(url_list, queue):
    for url in url_list:
        response = requests.get(url, headers=headers)
        time.sleep(3)
        content = response.content.decode('gb2312', 'ignore')
        get_data(content, queue)


def get_data(content, queue):
    soup = BeautifulSoup(content)
    title_list = soup.find_all('a', class_='news14')
    title_str_list = []
    for title in title_list:
        title_str_list.append(title['title'])
        queue.put(title_str_list)


def down_data(queue):
    # print(title_list)

    if not queue.empty():
        title_list = queue.get()
        with open('processquestion.txt', 'a') as q:
            q.write('\n'.join(title_list))
        print('该页写入完毕')


def main():
    queue = multiprocessing.Queue()
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
    process_list = []
    for i in range(N):
        p1 = multiprocessing.Process(target=get_content, args=(xclist[i], queue))
        p1.start()
        process_list.append(p1)

    p2 = multiprocessing.Process(target=down_data, args=(queue, ))
    p2.start()
    process_list.append(p2)

    for pro in process_list:
        pro.join()


    # content = get_content(number)
    #
    # title_list = get_data(content)
    #
    # down_data(title_list)


if __name__ == '__main__':
    main()
