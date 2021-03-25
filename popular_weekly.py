import requests

'''
B站每周必看网页数据：
WEB URL: https://www.bilibili.com/v/popular/weekly
'''
base_url = 'https://www.bilibili.com/v/popular/weekly'
api_url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number=104'

proxies = {
    'http': '116.117.134.134:80',
    'http': '112.80.248.75:80'
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

response = requests.get(url=api_url, headers=headers, proxies=proxies)
print(response.status_code)

datas = response.json()['data']['list']
for data in datas:
    print(data['title'])