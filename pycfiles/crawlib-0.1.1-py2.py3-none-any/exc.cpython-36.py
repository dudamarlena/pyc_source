# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/exc.py
# Compiled at: 2019-12-26 15:48:50
# Size of source mod 2**32: 2285 bytes
"""
Exceptions.
"""
from .status import Status

class CaptchaError(Exception):
    __doc__ = '\n    Encounter a captcha page.\n\n    http status code 403\n\n    **中文文档**\n\n    遭遇反爬虫验证页面。\n    '
    status_code = Status.S20_WrongPage.id


class ForbiddenError(Exception):
    __doc__ = '\n    Banned from server.\n\n    http status code 403\n\n    **中文文档**\n\n    被服务器禁止访问。\n    '
    status_code = Status.S20_WrongPage.id


class WrongHtmlError(Exception):
    __doc__ = '\n    The html is not the one we desired.\n\n    **中文文档**\n\n    页面不是我们想要的页面。有以下几种可能:\n\n    1. 服务器暂时连不上, 返回了404页面。\n    2. 服务器要求验证码, 返回了验证码页面。\n    3. 页面暂时因为各种奇怪的原因不是我们需要的页面。\n    '
    status_code = Status.S20_WrongPage.id


class DecodeError(Exception):
    __doc__ = '\n    Failed to decode binary response.\n    '
    status_code = Status.S25_DecodeError.id


class SoupError(Exception):
    __doc__ = '\n    Failed to convert html to beatifulsoup.\n\n    http status 200+\n\n    **中文文档**\n\n    html成功获得了, 但是格式有错误, 不能转化为soup。\n    '
    status_code = Status.S30_ParseError.id


class ParseError(Exception):
    __doc__ = '\n    Failed to parse data from html, may due to bug in your method.\n\n    **中文文档**\n\n    由于函数的设计失误, 解析页面信息发生了错误。\n    '
    code = Status.S30_ParseError.id


class IncompleteDataError(Exception):
    __doc__ = "\n    Successfully parse data from html, but we can't accept the result due to\n    missing data.\n    "
    status_code = Status.S40_InCompleteData.id


class ServerSideError(Exception):
    __doc__ = '\n    Server side problem.\n\n    code 404\n\n    **中文文档**\n\n    1. 因为服务器的缘故该页面无法正常访问, 也可能已经不存在了, 但以后可能会回来。\n    2. 因为服务器的缘故, 上面的数据不是我们想要的, 但是我们可以暂时用着, 以后可能要重新抓取。\n    '
    status_code = Status.S60_ServerSideError.id


class DownloadOversizeError(Exception):
    __doc__ = '\n    The download target are not falls in the size range you specified.\n    '