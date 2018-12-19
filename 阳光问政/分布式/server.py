import multiprocessing.managers
import queue
import requests
import re


task_queue = queue.Queue()
result_queue = queue.Queue()

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


def down_data(data):
    # print(title_list)

    with open('dispersedquestion.txt', 'a') as q:
        q.write('\n'.join(data))
        q.flush()
    print('该页写入完毕')


def return_task():
    return task_queue


def return_result():
    return result_queue


class QueueManger(multiprocessing.managers.BaseManager): # 继承 进程管理系统
    pass


if __name__ == '__main__':

    page = get_page()
    url_list = []
    number = 0
    while True:
        url = 'http://wz.sun0769.com/index.php/question/report?page=%d' % number
        url_list.append(url)
        number += 30
        if (number - page) > 0:
            break

    QueueManger.register('get_task', callable=return_task) # 注册函数给客户端调用
    QueueManger.register('get_result', callable=return_result)
    manger = QueueManger(address=('192.168.2.60', 8866), authkey=321321) # 创建一个管理器，设置地址密码
    manger.start() # 开启
    task, result = manger.get_task(), manger.get_result()
    for url in url_list:
        print('task', url)
        task.put(url)
    for i in range(100):
        ret = result.get()
        print('result', ret)
        down_data(ret)
