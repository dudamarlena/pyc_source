# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/faya/lib/__nikkei.py
# Compiled at: 2018-06-29 02:12:40
# Size of source mod 2**32: 1261 bytes
import requests
from lxml import html

def get():
    content = []
    headers = {'authority':'www.nikkei.com', 
     'pragma':'no-cache', 
     'cache-control':'no-cache', 
     'upgrade-insecure-requests':'1', 
     'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36', 
     'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
     'referer':'https://www.nikkei.com/theme/list/', 
     'accept-encoding':'gzip, deflate, br', 
     'accept-language':'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
    response = requests.get('https://www.nikkei.com/access/', headers=headers).text
    dom = html.fromstring(response)
    titles = dom.xpath('//*[@id="CONTENTS_MAIN"]/div[2]/ul/li/h3/span[2]/span[1]/a/text()')
    links = dom.xpath('//*[@id="CONTENTS_MAIN"]/div[2]/ul/li/h3/span[2]/span[1]/a/@href')
    content.append('=======Rank=======\n')
    [content.append(titles[num] + '\n' + 'https://www.nikkei.com/' + links[num] + '\n') for num in range(len(titles))]
    return '\n'.join(content)


if __name__ == '__main__':
    print(get())