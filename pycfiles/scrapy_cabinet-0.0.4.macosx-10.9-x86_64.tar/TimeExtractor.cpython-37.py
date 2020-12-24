# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/libs/sle/extractor/TimeExtractor.py
# Compiled at: 2019-11-18 00:40:08
# Size of source mod 2**32: 3752 bytes
import re
from typing import Union, List, Dict, AnyStr
from jsonpath import jsonpath
from lxml.html import HtmlElement, fromstring
from scrapy_cabinet.utils import LOGGER
from scrapy_cabinet.libs.utils import pre_parse
from scrapy_cabinet.libs.defaults import DATETIME_PATTERN, DATETIME_PATTERN_XPATH
import datetime

class TimeExtractor(object):

    def __init__(self, time_key: str='', time_lambda: list=list()):
        self.time_pattern = DATETIME_PATTERN
        self.time_xpath_pattern = DATETIME_PATTERN_XPATH
        self.time_key = time_key
        self.time_lambda = time_lambda

    def _json_extractor(self, json_dict: Union[(Dict, List)]):
        text = ''
        if self.time_key:
            text = ''.join(jsonpath(json_dict, self.time_key))
            LOGGER.info('PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}'.format('time_args', self.time_key, text))
        else:
            r_list = set(map(lambda x: str(x), filter(lambda x: isinstance(x, str) or isinstance(x, int) or isinstance(x, float), jsonpath(json_dict, '$..*'))))
            _ = ''.join(r_list)
            for dt in self.time_pattern:
                tmp = re.findall(dt, _)
                if tmp:
                    text = tmp[0]
                    LOGGER.info('PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}'.format('time_default', dt, text))
                    return text

        return text

    def _xpath_extractor(self, element: HtmlElement):
        if self.time_key:
            text = ''.join(element.xpath(self.time_key))
            LOGGER.info('PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}'.format('time_args', self.time_key, text))
            return text
        for xpath_str in self.time_xpath_pattern:
            text = ''.join(element.xpath(xpath_str))
            if text:
                LOGGER.info('PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}'.format('time_default', self.time_key, text))
                return text

        _ = ''.join(element.xpath('.//text()'))
        for dt in self.time_pattern:
            text = re.search(dt, _)
            if text:
                text = text.group(1)
                LOGGER.info('PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}'.format('time_default', dt, text))
                return text

    def _extractor(self, source: Union[(Dict, List, HtmlElement, AnyStr)]) -> str:
        if isinstance(source, (HtmlElement, str)):
            source = pre_parse(source)
            return self._xpath_extractor(source)
        return self._json_extractor(source)

    def extractor(self, source: Union[(Dict, List, HtmlElement, AnyStr)]) -> str:
        _ = self._extractor(source)
        for fn in self.time_lambda:
            temp = list()
            temp.extend(_) if isinstance(_, list) else temp.append(_)
            _ = (eval(fn))(*temp)

        return _


if __name__ == '__main__':
    a = '\n    <div>\n        <a class="url">aaaaa</a>\n        <span>09-12</span>\n    </div>\n    '
    extractor = TimeExtractor('//p/text()', ["lambda x,y:f'2019-{x}'", ''])
    r = extractor.extractor(fromstring(a))
    print(r)