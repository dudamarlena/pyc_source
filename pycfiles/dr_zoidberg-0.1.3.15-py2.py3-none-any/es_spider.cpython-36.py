# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ginopalazzo/Magic/zoidberg/zoidberg/scraper/spiders/es_spider.py
# Compiled at: 2018-03-15 10:39:46
# Size of source mod 2**32: 3487 bytes
import scrapy
from . import zoidberg_spider

class ElatletacomSpider(zoidberg_spider.ZoidbergSpider):
    __doc__ = '\n    Extends Zoidberg Base Spider for elatleta.com domain/source\n    '
    name = 'elatleta.com'

    def __init__(self, doctor_regex=None, urls=None, path='default', *args, **kwargs):
        (super(ElatletacomSpider, self).__init__)(args, doctor_regex=doctor_regex, urls=urls, path=path, name=self.name, **kwargs)

    def parse(self, response):
        """
        :param response: response of the web page
        :return: item and next page to parse
        """
        message_list = response.xpath('//li[@class="postbit postbitim postcontainer old"]')
        for m in message_list:
            author = m.xpath('.//a[@class="username offline popupctrl"]/strong/text()').extract_first()
            date = m.xpath('.//span[@class="date"]/text()').extract()[0]
            text = m.xpath('.//blockquote[@class="postcontent restore"]/text()')[0]
            find = text.re(self.doctor_regex)
            if len(find) > 0:
                yield {'author':author,  'text':text.extract(), 
                 'source':self.name, 
                 'date':date, 
                 'url':response.url}

        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=(self.parse))


class FemedeesSpider(zoidberg_spider.ZoidbergSpider):
    __doc__ = '\n    Extends Zoidberg Base Spider for femede.es domain/source\n    '
    name = 'femede.es'

    def __init__(self, doctor_regex=None, urls=None, path='default', *args, **kwargs):
        (super(FemedeesSpider, self).__init__)(args, doctor_regex=doctor_regex, urls=urls, path=path, name=self.name, **kwargs)

    def parse(self, response):
        """
        :param response: response of the web page
        :return: item and next page to parse
        """
        text_list = response.xpath('//span[@class="postbody"]')
        author_list = response.xpath('//span[@class="name"]/b/text()').extract()
        info_list = response.xpath('//span[@class="postdetails"]/text()').extract()
        date_list = [i.replace('Publicado: ', '') for i in info_list if 'Publicado' in i]
        for i in range(0, len(text_list)):
            text = text_list[i].xpath('.//text()')
            find = text.re(self.doctor_regex)
            if len(find) > 0:
                yield {'author':author_list[i],  'text':''.join(text.extract()), 
                 'source':self.name, 
                 'date':date_list[i], 
                 'url':response.url}

        next_page = response.xpath('//a[text()="Siguiente"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=(self.parse))