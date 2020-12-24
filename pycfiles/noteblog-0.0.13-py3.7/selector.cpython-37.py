# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/spider/selector.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 2503 bytes
"""
@author = super_fazai
@File    : selector.py
@connect : superonesfazai@gmail.com
"""
import re
from scrapy.selector import Selector
from ..common_utils import _print
__all__ = [
 'parse_field',
 'async_parse_field']

def parse_field(parser: dict, target_obj: (str, dict), is_first=True, logger=None, is_print_error=True) -> (str, list):
    """
    ** 异步根据类型解析字段
    :param parser: 解析对象 eg: {'method': 'css', 'selector': '.sss'}
    :param target_obj: 待处理的目标对象
    :param is_first: bool 是否re/css/xpath只提取第一个
    :param is_print_error: bool 是否打印error info
    :return:
    """
    res = ''
    if parser is not None:
        if parser == {}:
            _print(msg='遇到错误:', logger=logger, log_level=2, exception=(AssertionError('传入的parser为空dict!')))
            return res
        parser_method = parser.get('method', '')
        parser_selector = parser.get('selector')
        try:
            if parser_method == 're':
                _ = re.compile(parser_selector).findall(target_obj)
                if is_first:
                    res = _[0]
                else:
                    res = _
            elif parser_method == 'css':
                _ = Selector(text=target_obj).css(parser_selector).extract() or []
                if is_first:
                    res = _[0]
                else:
                    res = _
            elif parser_method == 'xpath':
                _ = Selector(text=target_obj).xpath(parser_selector).extract() or []
                if is_first:
                    res = _[0]
                else:
                    res = _
            elif parser_method == 'dict_path':
                res = parser_selector
            else:
                raise ValueError('解析该字段的method值未知!')
        except IndexError as e:
            try:
                if is_print_error:
                    _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
            finally:
                e = None
                del e

    return res


async def async_parse_field(*params, **kwargs) -> (
 str, list):
    """
    ** 异步根据类型解析字段
    :param parser: 解析对象 eg: {'method': 'css', 'selector': '.sss'}
    :param target_obj: 待处理的目标对象
    :param re_is_first: bool 是否re只提取第一个
    :return:
    """
    return parse_field(*params, **kwargs)