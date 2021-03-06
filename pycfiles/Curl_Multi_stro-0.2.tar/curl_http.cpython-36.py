# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\curl_http\curl_http.py
# Compiled at: 2018-07-07 03:45:12
# Size of source mod 2**32: 3335 bytes
import curl, pycurl, chardet

class HTTP:

    def __init__(self):
        self.http = curl.Curl()
        self.http.set_option(pycurl.CONNECTTIMEOUT, 15)
        self.content = ''
        self.response_header = ''
        self.response_code = ''
        self.timeout = 30
        self.cookie_list = {}
        self.cookie_str = ''
        self.request_proxy = None
        self.header = {}
        self.request_header = []
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'

    def set_header(self, name, value=''):
        if name is not None or name != '':
            self.request_header.append('{}:{}'.format(name, value))
        self.http.set_option(pycurl.HTTPHEADER, self.request_header)

    def set_foreign_ip(self, ip):
        self.set_header('CLIENT-IP', ip)
        self.set_header('X-FORWARDED-FOR', ip)

    def set_timeout(self, timeout):
        self.timeout = timeout
        self.http.set_timeout(self.timeout)

    def set_user_agent(self, user_agent):
        self.user_agent = user_agent
        self.http.set_option(pycurl.USERAGENT, user_agent)

    def set_proxy(self, host, port, protocol='http', username='', password=''):
        self.http.set_option(pycurl.PROXY, '{}://{}:{}'.format(protocol, host, port))
        if username:
            self.http.set_option(pycurl.PROXYUSERPWD, '{}:{}'.format(username, password))

    def set_cookie(self, key, value):
        self.cookie_list[key] = value
        self.cookie_str += '{}={};'.format(key, value)
        self.http.set_option(pycurl.COOKIE, self.cookie_str)

    def get_cookie(self, key=None):
        if key:
            return self.cookie_list.get(key)
        else:
            return self.cookie_list

    def get_code(self):
        return self.response_code

    def get_header(self, key=''):
        if key == '':
            return self.header
        else:
            return self.header.get(key, None)

    def __http_request(self, url, post_data, referer=''):
        if referer:
            self.http.set_option(pycurl.REFERER, referer)
        else:
            if post_data:
                self.http.post(url, post_data)
            else:
                self.http.get(url)
        temp_header = self.http.header().split('\r\n')
        for x in temp_header:
            x = x.strip().split(':')
            if len(x) < 2:
                continue
            self.header[x[0]] = x[1]
            if x[0] == 'Set-Cookie':
                cookies = x[1].split(';')
                for cookie in cookies:
                    cookie = cookie.strip().split('=')
                    if len(cookie) < 2:
                        pass
                    else:
                        self.set_cookie(cookie[0], cookie[1])

        self.response_code = self.http.get_info(pycurl.RESPONSE_CODE)
        encoding = chardet.detect(self.http.body()).get('encoding')
        self.content = self.http.body().decode(encoding=encoding, errors='ignore')
        return self.content

    def request(self, url, params=None, referer=''):
        return self._HTTP__http_request(url, params, referer)