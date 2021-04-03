import requests
import csv
from tqdm import tqdm
import time
import random
from fake_useragent import UserAgent
ua = UserAgent()

'''
B站综合热门网页数据：
WEB URL: https://www.bilibili.com/v/popular/all
'''


def scrape_info(file_project, url, headers, proxies):
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies)
        if response.status_code != 200:
            print(f'{url} Appear {response.status_code} error !')
            exit()
    except:
        print(f'{url} Appear some other errors !')
        exit()
    datas = response.json()['data']
    data_list = datas['list']
    # 要获取的信息如下：
    #  标题  | 作品发布日期 |  up主  | 播放量 | 点赞  | 投币 |   收藏   |  转发  |  弹幕量  |  评论数  | 视频链接
    #  title |    ctime    |  name |  view  | like | coin | favorite | share | danmaku  |  reply  | short_link
    for d in data_list:
        file_project.writerow([
            d['title'],  # title
            d['ctime'],  # ctime
            d['owner']['name'],  # name
            d['stat']['view'],  #  view
            d['stat']['like'],  #  like
            d['stat']['coin'], # coin
            d['stat']['favorite'],  # favorite
            d['stat']['share'], # share
            d['stat']['danmaku'],  # danmaku
            d['stat']['reply'],  # reply
            d['short_link']  # video_link
        ])
        print(d['title'])


def main():
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://www.bilibili.com',
        'pragma': 'no-cache',
        'referer': 'https://www.bilibili.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': ua.random
    }
    proxies = {
        # 'http': '61.135.169.121:80',
        'http': '202.108.22.5:80'
    }
    total_pn = 10
    f = open('./data/Comprehensive_hot_data.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['title', 'ctime', 'name', 'view', 'like', 'coin', 'favorite', 'share', 'danmaku', 'reply', 'short_link'])
    for i in tqdm(range(10), desc='Processing:'):
        api_url = f'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={i+1}'
        scrape_info(file_project=csv_writer, url=api_url, headers=headers, proxies=proxies)
    f.close()

if __name__ == "__main__":
    main()