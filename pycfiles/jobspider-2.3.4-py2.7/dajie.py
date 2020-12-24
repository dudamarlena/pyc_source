# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\jobspider\dajie.py
# Compiled at: 2016-04-13 21:04:26
from baseclass.base_spider import Base_Spider
from baseclass.utils.get_cookies import get_cookie

class DJ_Spider(Base_Spider):

    def __init__(self, website, *args):
        super(DJ_Spider, self).__init__(website, args)

    def parse(self, url):
        """
        :param url:
        :return:json data
        to get data from the data url,we must firstlt get response cookie,so
        we must get cookie from url:http://so.dajie.com/job/search?keyword=python&f=nav
        then we can get data normally
        """
        try:
            json_str = self.get_content(url, url_type='json')
        except ValueError:
            Cookie = get_cookie('http://so.dajie.com/job/search?keyword=python&f=nav')
            combin_cookie = [ ('=').join([key, value]) for key, value in Cookie ]
            self.headers['Cookie'] = (';').join(combin_cookie)
            json_str = self.get_content(url, url_type='json')

        metadata = json_str['data']['list']
        data = []
        for md in metadata:
            item = {}
            try:
                item['website'] = 'dajie'
                item['link'] = md['liHref']
                item['title'] = md['jobName']
                item['company'] = md['compName']
                item['date'] = md['time']
                item['homepage'] = md['compHref']
            except KeyError as e:
                print str(e)

            data.append(item)

        return [ item for item in data if item ]

    def pages_parse(self, keyword):
        for page in xrange(1, 2):
            url = 'http://so.dajie.com/job/ajax/search/filter?jobsearch=0&pagereferer=blank&ajax=1&keyword=%s&page=%d' % (keyword, page) + '&order=0&from=user&salary=&recruitType=3%2C4&city=110000&positionIndustry=&positionFunction=&degree=&quality=&experience=&internshipDays=&partTimeCategory=&_CSRFToken='
            data = self.parse(url)
            yield data


if __name__ == '__main__':
    dj = DJ_Spider('dajie', 'X-Requested-With', 'Host', 'Referer', 'Cookie')
    for item in dj.pages_parse('python'):
        print item