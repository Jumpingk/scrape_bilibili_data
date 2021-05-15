import requests
import re
import time
import os
import pandas as pd
from fake_useragent import UserAgent

'''
    获取某一视频的弹幕数据列表
    测试api_url: https://api.bilibili.com/x/v1/dm/list.so?oid=338815685
    # 灵笼·特别篇弹幕爬取
'''

def generate_oid(video_url):
    BV = os.path.basename(video_url)
    get_oid = 'https://api.bilibili.com/x/player/pagelist?bvid={BV}&jsonp=jsonp'
    info = requests.get(get_oid.format(BV=BV)).json()
    if info['code'] == 0:
        return info['data'][0]['cid']
    else:
        print(info['message'])

def bullet_screen(oid):
    # 单个弹幕信息: {'time': time, 'danmu': danmu}(还有一些其他信息可以继续扩充)
    # return pd.Dataframe([{}, {}, {}])
    #  time  danmu
    # 00:00 'danmu'
    api_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={oid}'
    headers = {
        'User-Agent': UserAgent(use_cache_server=False).random
    }
    print(headers)
    content = requests.get(url=api_url.format(oid=oid), headers=headers)
    content.encoding = 'utf-8'
    info = content.text
    rets_list = re.findall('<d p="(.*?)">(.*?)</d>', info, re.S)
    danmu_list = []
    for ret in rets_list:
        timeStamp = float(ret[0].split(',')[0])
        time_str = time.strftime('%M:%S', time.localtime(timeStamp))
        danmu = {
            'time': time_str,
            'danmu': ret[1]
        }
        danmu_list.append(danmu)
    return pd.DataFrame(danmu_list).sort_values(by='time')

if __name__ == '__main__':
    video_url = 'https://www.bilibili.com/video/BV1iv41157LQ'
    oid = generate_oid(video_url=video_url)
    # oid = '338815685'
    danmu_infos = bullet_screen(oid=oid)
    for index, row in danmu_infos.iterrows():
        print(row['time'] + ' ' + row['danmu'])
    print(danmu_infos.size)
