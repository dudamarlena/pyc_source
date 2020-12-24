# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dcp_common/middlewares/cookies.py
# Compiled at: 2018-09-28 07:51:59
import logging, requests, json

class CookiesMiddleware:

    def __init__(self, cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        self.logger.debug('Getting Cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            self.logger.debug(('Using Cookies {cookies}').format(cookies=json.dumps(cookies)))

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(cookies_url=settings.get('COOKIES_URL'))