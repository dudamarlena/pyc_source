# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ojcrawler/crawlers/base.py
# Compiled at: 2018-12-27 10:28:16
from __future__ import absolute_import, division, print_function
from socket import timeout
from six.moves.urllib.error import HTTPError, URLError
from ojcrawler.crawlers.config import logger
from ojcrawler.crawlers.config import HTTP_METHOD_TIMEOUT

class NetWorkException(RuntimeError):
    pass


class CrawlerException(SystemError):
    pass


class OJ(object):

    def __init__(self, handle, password, image_func):
        self.handle = handle
        self.password = password
        self.image_func = image_func

    def __str__(self):
        return ('{}({})').format(self.oj_name, self.handle)

    @property
    def oj_name(self):
        return self.__class__.__name__.lower()

    @property
    def browser(self):
        raise NotImplementedError

    @property
    def url_home(self):
        raise NotImplementedError

    def url_problem(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def url_login(self):
        raise NotImplementedError

    @property
    def url_submit(self):
        raise NotImplementedError

    @property
    def url_status(self):
        raise NotImplementedError

    @property
    def http_headers(self):
        raise NotImplementedError

    @property
    def uncertain_result_status(self):
        raise NotImplementedError

    @property
    def compatible_problem_fields(self):
        return [
         'title', 'problem_type', 'origin',
         'limits',
         'samples',
         'descriptions',
         'category',
         'tags',
         'append_html']

    def get(self, url):
        try:
            return self.browser.open(url, timeout=HTTP_METHOD_TIMEOUT)
        except (HTTPError, URLError) as error:
            logger.error('Data not retrieved because %s\nURL: %s', error, url)
            return
        except timeout:
            logger.error('socket timed out\nURL: %s', url)
            return

        return

    def post(self, url, data):
        raise NotImplementedError

    @staticmethod
    def http_status_code(response):
        if response:
            return response.status
        else:
            return

    def ping(self):
        response = self.get(self.url_home)
        return self.http_status_code(response) == 200

    @staticmethod
    def get_languages():
        raise NotImplementedError

    def login(self):
        raise NotImplementedError

    def is_login(self):
        raise NotImplementedError

    def replace_image(self, html):
        raise NotImplementedError

    def get_problem(self, *args, **kwargs):
        raise NotImplementedError

    def submit_code(self, *args, **kwargs):
        raise NotImplementedError

    def get_result(self):
        raise NotImplementedError

    def get_result_by_rid(self, rid):
        pass

    def get_compile_error_info(self, rid):
        pass