# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\jobspider\zhilian.py
# Compiled at: 2016-03-20 20:41:26
__author__ = 'WHB'
from baseclass.base_spider import Base_Spider

class ZL_Spider(Base_Spider):
    """
    the website is qianchengwuyou,it is like lagou,
    no need ajax
    """

    def __init__(self, website, *args):
        super(ZL_Spider, self).__init__(website, args)

    def parse(self, url):
        soup = self.get_content(url)
        result = []
        tables = soup.find(id='newlist_list_content_table')
        if tables is not None:
            for table in list(tables.children):
                if table.name is None:
                    continue
                else:
                    item = {}
                    item['website'] = 'zhilian'
                    Trinfo = table.find('tr')
                    title = Trinfo.find('td', 'zwmc')
                    if title is not None:
                        item['link'] = title.find('a')['href']
                        item['title'] = title.find('a').text
                    Comp = Trinfo.find('td', 'gsmc')
                    if Comp is None:
                        continue
                    else:
                        item['homepage'] = Comp.find('a')['href']
                        item['company'] = Comp.find('a').text
                    intro = Trinfo.find('td', 'gzdd')
                    date = Trinfo.find('td', 'gxsj')
                    item['date'] = date.text if date is not None else ''
                    result.append(item)

        return [ item for item in result if item ]

    def pages_parse(self, keyword):
        for page in xrange(1, 2):
            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=&kw=%s&sm=0&sg=654c99887ed049479fb08d6530323db0&p=%d&isfilter=0&fl=530&isadv=0&sb=1' % (keyword, page)
            data = self.parse(url)
            yield data