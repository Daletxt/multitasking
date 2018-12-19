import multiprocessing.managers
import requests
from bs4 import BeautifulSoup
import time


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }


def get_content(url_str):
    response = requests.get(url_str, headers=headers)
    time.sleep(3)
    content = response.content.decode('gb2312', 'ignore')
    return get_data(content)


def get_data(content):
    soup = BeautifulSoup(content)
    title_list = soup.find_all('a', class_='news14')
    title_str_list = []
    for title in title_list:
        title_str_list.append(title['title'])
    return title_str_list


def down_data(queue):
    # print(title_list)

    if not queue.empty():
        title_list = queue.get()
        with open('processquestion.txt', 'a') as q:
            q.write('\n'.join(title_list))
        print('该页写入完毕')


class QueueManger(multiprocessing.managers.BaseManager):
    pass


QueueManger.register('get_task') # 注册函数调用服务器
QueueManger.register('get_result')
manger = QueueManger(address=('192.168.2.60', 8866), authkey=321321)
manger.connect() # 连接服务器
task, result = manger.get_task(), manger.get_result()
for i in range(20):
    try:
        url = task.get()
        print('client', url)
        tit_list = get_content(url)

        result.put(tit_list)
    except:
        print('error')
