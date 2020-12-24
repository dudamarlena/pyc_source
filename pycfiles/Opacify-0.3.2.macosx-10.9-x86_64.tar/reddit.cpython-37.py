# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/opacify/reddit.py
# Compiled at: 2019-01-24 01:21:50
# Size of source mod 2**32: 1195 bytes
import requests, json, time, re

def reddit_get_links(count=50, sleep=5, giveup=600, filter_over18=True):
    cache = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    start = time.time()
    errors = 0
    count = int(count)
    giveup = int(giveup)
    while len(cache) < count and time.time() - start < giveup:
        r = requests.get('https://www.reddit.com/r/all/new.json', headers=headers)
        if r.status_code > 204:
            errors += 1
            if errors > 10:
                break
            time.sleep(sleep * 2)
            continue
        for i in r.json()['data']['children']:
            d = i['data']
            over_18 = d['over_18']
            if over_18 is True:
                continue
            if 'url' in d:
                url = d['url']
                if re.search('\\.(jpg|png|jpeg|gif|txt|pdf)$', url) and url not in cache:
                    cache.append(url)

        time.sleep(sleep)

    return cache


if __name__ == '__main__':
    for i in reddit_get_links():
        print(i)