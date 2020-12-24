# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notetool/crawler/movies.py
# Compiled at: 2020-01-06 03:23:12
# Size of source mod 2**32: 3273 bytes
import re, requests
from lxml import html

def get_html(keywd, url):
    param = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
    Url = url % keywd
    html = requests.get(Url, params=param).content.decode('utf8')
    return html


def get_movielink(text):
    tree = html.fromstring(text)
    ctree = tree.xpath('//div[@class="clearfix search-item"]')
    link = []
    for item in ctree:
        print(item.xpath('em/text()')[0], item.xpath('div[2]/div/a/strong/text()')[0], ':', item.xpath('div[2]/div/a/@href')[0])
        link.append((item.xpath('div[2]/div/a/@href')[0], item.xpath('em/text()')[0]))

    return link


def get_downloadlink(link):
    if type_link == '电视剧':
        from_url = 'http://www.zimuzu.tv/resource/index_json/rid/%s/channel/tv' % link.split('/')[(-1)]
    else:
        from_url = 'http://www.zimuzu.tv/resource/index_json/rid/%s/channel/movie' % link.split('/')[(-1)]
    param = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', 
     'Referer':'http://www.zimuzu.tv%s' % link}
    data = requests.get(from_url, params=param).content.decode('utf8')
    data = ''.join(data.split('=')[1:])
    print(data)
    pattern = '<h3><a href(.*?) target'
    url = re.findall(pattern, data)[0].replace('\\', '').replace('"', '').strip()
    return url


def get_download(url):
    if 'zmz' not in url:
        print('非下载页面：', url)
    param = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
    res = requests.get(url, params=param).content.decode('utf-8')
    tree = html.fromstring(res)
    tree1 = tree.xpath('//div[@class="tab-content info-content"]//div[@class="tab-content info-content"]')
    if tree1:
        downloadList = []
        for item in tree1:
            ed2k = item.xpath('div[2]//ul[@class="down-links"]/li[2]/a/@href')
            name = item.xpath('div[1]//div[@class="title"]/span[1]/text()')
            bdy = item.xpath('div[1]//div[@class="title"]/ul/li[2]/a/@href')
            for i, j, k in zip(name, bdy, ed2k):
                downloadList.append(dict(name=i, bdy=j, ed2k=k))

    print(downloadList)


get_download('http://got001.com/resource.html?code=WasT62')