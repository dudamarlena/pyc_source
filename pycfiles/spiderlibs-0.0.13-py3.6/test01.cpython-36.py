# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\spiderlib\test01.py
# Compiled at: 2020-03-25 07:19:52
# Size of source mod 2**32: 4083 bytes
import sys
from spiderlib import *

def test_FilePipeline1():
    """
    结果写入到一个文件a.txt中
    :return:
    """
    spider = Spider('博客园精华', pipeline=(FilePipeline('/tmp/bbbbb')))
    spider.list(urls=['https://www.cnblogs.com/#p1', 'https://www.cnblogs.com/#p2', 'https://www.cnblogs.com/#p3'], expresses={'text':"//a[@class='titlelnk']//text()",  'link':"//a[@class='titlelnk']//@href"}, next='link', fields={'标题':'text',  '网址':'link'})
    spider.page(expresses={'title':"//a[@id='cb_post_title_url']//text()",  'content':"//div[@id='cnblogs_post_body']//text()"}, fields={'标题':'title',  '正文':'content'})
    spider.run()


def test_FilePipeline2():
    """
    结果写入到两个文件a1.txt和a2.txt中
    todo 输出pid，只有最后一个有，很奇怪
    :return:
    """
    spider = Spider('博客园精华', downloader=(RenderDownloader()), pipeline=(FilePipeline('../a21.txt')))
    spider.page(urls='https://www.cnblogs.com/pick/', expresses={'link': "//a[@class='titlelnk']//@href"}, next='link', fields={'网址':'title',  '网址':'link'}, is_list=True)
    spider.page(expresses={'title':"//a[@id='cb_post_title_url']//text()",  'content':"//div[@id='cnblogs_post_body']//text()"}, fields_tag='../a22.txt', fields={'标题':'title',  '正文':'content',  '上级索引':'pid'}, is_list=False)
    spider.run()


def test_FilePipeline3():
    """
    测试常量表达式，结果写入到一个文件a3.txt
    :return:
    """
    spider = Spider('博客园精华', pipeline=FilePipeline('../a3.txt', sep='\t\t'))
    print(spider)
    spider.page(urls='https://www.cnblogs.com/pick/', expresses={'link':"//a[@class='titlelnk']//@href",  '时间戳':5656567567567}, fields={'网址':'link',  '时间戳':'时间戳'}, is_list=True)
    spider.run()


def test_FilePipeline4():
    """
    测试常量保存值，结果写入到一个文件a4.txt
    :return:
    """
    spider = Spider('博客园精华', pipeline=FilePipeline('../a4.txt', sep='\t\t'))
    cur = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    spider.page(urls='https://www.cnblogs.com/pick/', expresses={'link': "//a[@class='titlelnk']//@href"}, fields={'网址':'link',  '时间戳':cur}, is_list=True)
    spider.run()


def test_MySQLPipeline1():
    """
    结果写入到
    :return:
    """
    spider = Spider('博客园精华', pipeline=(MySQLPipeline()))
    spider.page(urls='https://www.cnblogs.com/pick/', expresses={'link': "//a[@class='titlelnk']//@href"}, next='link', is_list=True)
    spider.page(expresses={'title':"//a[@id='cb_post_title_url']//text()",  'content':"//div[@id='cnblogs_post_body']//text()"}, fields={'title':'title',  'text':'content',  'url':'pid'}, is_list=False)
    spider.run()


def test_WordPressPipeline1():
    """
    结果写入到
    :return:
    """
    spider = Spider('博客园精华', pipeline=WordPressPipeline(host='192.168.1.88:84'))
    spider.page(urls='https://www.cnblogs.com/pick/', expresses={'link': "//a[@class='titlelnk']//@href"}, next='link', is_list=True)
    spider.page(expresses={'title':"//a[@id='cb_post_title_url']//text()",  'content':"//div[@id='cnblogs_post_body']//text()"}, fields={'title':'title',  'content':'content'}, is_list=False)
    spider.run()


def test_aaa():
    spider = Spider('博客园')
    spider.list(urls='https://www.cnblogs.com/', expresses={'title':"//a[@class='titlelnk']//text()",  'link':"//a[@class='titlelnk']//@href"}, fields={'标题':'title',  '链接':'link'})
    spider.run()