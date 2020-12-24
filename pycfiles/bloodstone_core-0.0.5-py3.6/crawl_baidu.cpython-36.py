# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/crawl_baidu.py
# Compiled at: 2019-09-19 03:18:45
# Size of source mod 2**32: 6207 bytes
"""
@author: Yan Liu
@file: crawl.py
@time: 2018/3/27 11:43
@desc: 爬取百度图片
"""
import requests, os

def crawl_img(keyword_list, page_num, img_dir):
    """
    爬虫入口函数
    :param keyword_list: 需要搜索的管检测列表
    :param page_num: 搜索几页
    :param img_dir: 保存图片的路径
    :return:
    """
    for name in keyword_list:
        dataList = getPages(name, page_num)
        download_img(name, dataList, img_dir)


def getPages(keyword, pages):
    params = []
    for i in range(30, 30 * pages + 30, 30):
        params.append({'tn':'resultjson_com', 
         'ipn':'rj', 
         'ct':201326592, 
         'is':'', 
         'fp':'result', 
         'queryWord':keyword, 
         'cl':2, 
         'lm':-1, 
         'ie':'utf-8', 
         'oe':'utf-8', 
         'adpicid':'', 
         'st':'', 
         'z':'', 
         'ic':'', 
         'word':keyword, 
         's':'', 
         'se':'', 
         'tab':'', 
         'width':'', 
         'height':'', 
         'face':'', 
         'istype':'', 
         'qc':'', 
         'nc':1, 
         'fr':'', 
         'pn':i, 
         'rn':30, 
         'gsm':'1e', 
         '1488942260214':''})

    url = 'https://image.baidu.com/search/acjson'
    urls = []
    fail_url_count = 0
    for i in params:
        response = requests.get(url, params=i)
        try:
            jsonObj = response.json()
            urls.append(jsonObj.get('data'))
        except Exception as e:
            print('json数据格式错误 ' + str(e))
            fail_url_count += 1

    print('提取图片url成功：%d 失败：%d' % (len(urls), fail_url_count))
    return urls


x = 0

def download_img(keyword, dataList, localPath):
    global x
    if not os.path.exists(localPath):
        os.mkdir(localPath)
    for list in dataList:
        for i in list:
            if i.get('hoverURL') != None:
                try:
                    print('正在下载：%s' % i.get('hoverURL'))
                    ir = requests.get(i.get('hoverURL'))
                    image_path = os.path.join(localPath, '%s_%d.jpg' % (keyword, x))
                    open(image_path, 'wb').write(ir.content)
                    x += 1
                except Exception as e:
                    print('图片下载失败' + i.get('hoverURL') + str(e))

    print('%s图片下载完成' % keyword)


if __name__ == '__main__':
    human_list = [
     '脖子', '颈']
    crawl_img(human_list, 30, 'D:/Dataset/asimg/download/human/')
    print('一共下载%d张图片' % x)