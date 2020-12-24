# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\cet.py
# Compiled at: 2015-08-20 09:06:49
import urllib, urllib2, re, string

def setRequestData():
    xm = raw_input('请输入您的姓名：')
    zkzh = raw_input('请输入准考证号：')
    return {'zkzh': zkzh, 'xm': xm}


def getHtmlCode(request_data):
    url = 'http://www.chsi.com.cn/cet/query?' + urllib.urlencode(request_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40 Safari/537.36', 'Host': 'www.chsi.com.cn', 'Referer': 'http://www.chsi.com.cn/cet/', 'Upgrade-Insecure-Requests': '1', 'X-FirePHP-Version': '0.0.6', 'Connection': 'keep-alive'}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    return response.read()


def parseHtmlCode(html_code):
    html_table = re.findall('<table(.*?)</table', html_code, re.S)
    html_td = re.findall('>(.*?)<', html_table[1], re.S)
    score_list = []
    for x in html_td:
        x = x.strip()
        x = x.rstrip('：')
        if x:
            score_list.append(x)

    return score_list


def output(score_list):
    try:
        for x in xrange(0, 17, 2):
            if x % 2 == 0:
                print '\t' + score_list[x] + '\t\t' + score_list[(x + 1)] + '\n'

    except IndexError as e:
        print 'Sorry, 获取失败'


def go():
    request_data = setRequestData()
    html_code = getHtmlCode(request_data)
    score_list = parseHtmlCode(html_code)
    output(score_list)


go()