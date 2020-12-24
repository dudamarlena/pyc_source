# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/Obsidian/ddspider.py
# Compiled at: 2018-01-07 08:54:27
# Size of source mod 2**32: 2731 bytes
import time, scrapy
from Obsidian.items import ObsidianItem
import logging
from scrapy import Spider
from scrapy.http import Request
logging.basicConfig(level=(logging.NOTSET))

class DDSpider(Spider):

    def juice(self, s, pipline, should_extract=1):
        selector = s
        command = 'selector'
        for pip in pipline:
            if 'type' not in pip:
                pass
            else:
                if pip['type'] != 're':
                    command = "%s.%s('%s')" % (command, pip['type'], pip['value'])
                else:
                    command = '%s.re(%s)' % (command, pip['value'])

        print('********************')
        print(command)
        print('********************')
        selector = self.eval(selector, command)
        if len(pipline) > 0:
            if pipline[(-1)]['type'] != 're':
                if should_extract:
                    selector = selector.extract()
                    if 'should_join' not in pipline[(-1)] or pipline[(-1)]['should_join'] != 0:
                        return ''.join(selector).strip()
        return selector

    def drink(self, content, regex='', index=1):
        return ''.join(content).strip()

    def eval(self, selector, code):
        return eval(code)

    def parse(self, response):
        if len(self.link_array_pipline) == 0:
            yield self.parse_page(response)
        else:
            if isinstance(self.link_array_pipline[0], list):
                for item in self.parse_step_generator()(response):
                    yield item

            else:
                for item in map(lambda x: self.prefix + x, self.juice(response, self.link_array_pipline)):
                    yield Request(url=item, callback=(self.parse_page))

    def parse_step_generator(self, i=0):

        def fun(response):
            if i >= len(self.link_array_pipline):
                yield self.parse_page(response)
            else:
                pipline = self.link_array_pipline[i]
                for item in map(lambda x: self.prefix + x, self.juice(response, pipline)):
                    yield Request(url=item, callback=(self.parse_step_generator(i + 1)))

        return fun

    def parse_page(self, response):
        main_content_selector = self.juice(response, self.main_content_pipline, 0)
        item = ObsidianItem()
        for key, value in self.item_pipline.items():
            if key not in ObsidianItem.fields:
                ObsidianItem.fields[key] = scrapy.Field()
            item[key] = self.juice(main_content_selector, value)

        item['url'] = response.url
        item['crawl_time'] = int(time.time())
        item['status'] = 1
        return item