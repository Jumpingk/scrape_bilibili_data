import requests
import csv
from tqdm import tqdm
import time
import random

'''
B站每周必看网页数据：
WEB URL: https://www.bilibili.com/v/popular/weekly
'''

def scrape_info(file_object, periods, url, headers, proxies):
    try:
        response = requests.get(url=url.format(periods=periods), headers=headers, proxies=proxies)
        if response.status_code != 200:
            print(f'{periods} periods: Appear {response.status_code} error !')
            exit()
    except:
        print(f'{periods} periods: Appear some other errors !')
        exit()

    datas =  response.json()['data']
    datas_config = datas['config']
    datas_list = datas['list']

    # 要获取的信息如下：
    # 期数  | 期刊发布日期 | 标题  | 作品发布日期 | up主   | 播放量       | 点赞   | 弹幕量               | 视频标签     | 视频链接
    # priods | priods_date | title | works_date | author | view_counts | like | bullet_screen_counts | video_label | video_link
    
    for d in datas_list:
        file_object.writerow([
            datas_config['number'],  # priods
            datas_config['stime'],  # priods_date
            d['title'],  #  title
            d['ctime'],  # works_date
            d['owner']['name'],  #  author
            d['stat']['view'],  #  view_counts
            d['stat']['like'],  #  like
            d['stat']['danmaku'],  # bullet_screen_counts
            d['rcmd_reason'],  # video_label
            d['short_link']  # video_link
        ])

        print(d['title'])

def main():
    proxies = {
    'http': '116.117.134.134:80',
    # 'http': '202.108.22.5:80'
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://www.bilibili.com',
        'pragma': 'no-cache',
        'referer': 'https://www.bilibili.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    last_periods = 106  # 最新期数
    api_url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={periods}'
    f = open(f'./data/all_periods_data.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['priods', 'priods_date', 'title', 'works_date', 'author', 'view_counts', 'like', 'bullet_screen_counts', 'video_label', 'video_link'])
    for i in tqdm(range(1, last_periods + 1), desc='Processing:'):
        scrape_info(file_object=csv_writer, periods=i, url=api_url, headers=headers, proxies=proxies)
        time.sleep(random.randint(1, 4))
    f.close()


if __name__ == '__main__':
    main()


