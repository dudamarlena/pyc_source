# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\spider_auto_repair\data_extractor_scrapy.py
# Compiled at: 2018-08-13 06:01:22
# Size of source mod 2**32: 2087 bytes
import scrapy, os, json

class LoginSpider(scrapy.Spider):
    name = 'data_extractor_scrapy'

    def read_file(self, path):
        with open(path) as (f):
            read_data = f.read()
        return read_data

    def get_base_url(self, url):
        l = []
        n = len(url)
        for i in range(n - 1, -1, -1):
            l.append(url[i])
            x = len(l)
            if len(l) >= 3:
                if l[(x - 1)] + l[(x - 2)] + l[(x - 3)] == 'www':
                    break

        if len(l) > 0:
            if l[0] == '/':
                l.pop(0)
        l.reverse()
        s = ''.join(l)
        if ':' in s:
            s = s[:s.index(':')]
        return s

    def start_requests(self):
        path = 'C:/Users/Viral Mehta/Desktop/Scrapy-Spider-Autorepair/top500domains.csv'
        lst_urls = self.read_file(path).split('\n')
        urls = []
        n = len(lst_urls)
        for i in range(n):
            for j in range(1996, 2019):
                url = 'http://archive.org/wayback/available?url=' + lst_urls[i] + '&timestamp=' + str(j)
                urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=(self.parse))

    def parse(self, res):
        body = res.body
        dic = json.loads(body.strip())
        if dic['archived_snapshots'] == {}:
            return
        else:
            url_of_snapshot = dic['archived_snapshots']['closest']['url']
            return [scrapy.Request(url_of_snapshot, callback=(self.parse2))]

    def parse2(self, res):
        base_url = self.get_base_url(res.url)
        print('base_url =', base_url)
        timestamp = res.url[27:31]
        directory = 'C:/Users/Viral Mehta/Desktop/Scrapy-Spider-Autorepair/Dataset/' + base_url
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = directory + '/' + base_url + '_' + timestamp + '.html'
        with open(filename, 'wb') as (f):
            f.write(res.body)
        self.log('Saved file %s' % filename)