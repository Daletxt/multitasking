import requests
from bs4 import BeautifulSoup
import re
import csv
import time


def get_content(number):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    response = requests.get('http://wz.sun0769.com/index.php/question/report?page=%d' % number, headers=headers)
    content = response.content.decode("gb2312", "ignore")
    re_str = '共(\d+)条记录'
    regex = re.compile(re_str)
    page = re.findall(regex, content)[0]
    time.sleep(3)
    return content, eval(page)


def get_data(content):
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
