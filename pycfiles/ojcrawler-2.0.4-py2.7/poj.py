# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ojcrawler/crawlers/poj.py
# Compiled at: 2018-12-29 11:19:40
from __future__ import absolute_import, division, print_function, unicode_literals
from socket import timeout
from bs4 import BeautifulSoup
from six.moves.urllib import request, parse
from six.moves.urllib.error import HTTPError, URLError
from six.moves.http_cookiejar import CookieJar
from ojcrawler.crawlers.base import OJ
from ojcrawler.crawlers.config import logger, save_image
from ojcrawler.crawlers.config import HTTP_METHOD_TIMEOUT

class POJ(OJ):

    def __init__(self, handle, password, image_func=save_image):
        super(POJ, self).__init__(handle, password, image_func)
        cookie = CookieJar()
        handler = request.HTTPCookieProcessor(cookie)
        self.opener = request.build_opener(handler)

    @property
    def browser(self):
        return self.opener

    @property
    def url_home(self):
        return b'http://poj.org/'

    def url_problem(self, pid):
        return self.url_home + (b'problem?id={}').format(pid)

    @property
    def url_login(self):
        return self.url_home + b'login?'

    @property
    def url_submit(self):
        return self.url_home + b'submit?'

    @property
    def url_status(self):
        return self.url_home + b'status?'

    @property
    def http_headers(self):
        return {b'User-Agent': b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36', 
           b'Origin': b'http://poj.org', 
           b'Host': b'poj.org', 
           b'Content-Type': b'application/x-www-form-urlencoded', 
           b'Connection': b'keep-alive'}

    @property
    def uncertain_result_status(self):
        return [
         b'running & judging', b'compiling', b'waiting']

    def post(self, url, data):
        post_data = parse.urlencode(data).encode()
        req = request.Request(url, post_data, self.http_headers)
        try:
            return self.opener.open(req, timeout=HTTP_METHOD_TIMEOUT)
        except (HTTPError, URLError) as error:
            logger.error(b'Data not retrieved because %s\nURL: %s', error, url)
        except timeout:
            logger.error(b'socket timed out\nURL: %s', url)

    @staticmethod
    def get_languages():
        return {b'G++': b'0', 
           b'GCC': b'1', 
           b'JAVA': b'2', 
           b'PASCAL': b'3', 
           b'C++': b'4', 
           b'C': b'5', 
           b'FORTRAN': b'6'}

    def login(self):
        data = dict(user_id1=self.handle, password1=self.password, B1=b'login', url=b'.')
        ret = self.post(self.url_login, data)
        if ret:
            html = ret.read().decode(b'utf-8')
            if html.find(b'loginlog') > 0:
                return (True, b'')
            return (False, b'账号密码不匹配')
        else:
            return (
             False, b'登陆：http方法错误，请检查网络后重试')

    def is_login(self):
        ret = self.get(self.url_home)
        if ret:
            html = ret.read().decode(b'utf-8')
            if html.find(b'loginlog') > 0:
                return True
            return False
        return False

    def replace_image(self, html):
        pos = html.find(b'<img src=')
        if pos == -1:
            return html
        end_pos = html[pos:].find(b'>')
        left = pos + 10
        right = pos + end_pos - 2
        image_url = self.url_home + html[left:right]
        saved_url = self.image_func(image_url, self.oj_name)
        return html[:left] + saved_url + self.replace_image(html[right:])

    def get_problem(self, pid):
        ret = self.get(self.url_problem(pid))
        if ret:
            html = ret.read().decode(b'utf-8')
            soup = BeautifulSoup(html, b'html5lib')
            title = soup.find(b'title').text
            if title == b'Error':
                return (False, soup.find(b'li').text)
            title = soup.find(b'div', {b'class': b'ptt'}).text
            plm = soup.find(b'div', {b'class': b'plm'})
            limits = plm.find_all(b'td')
            problem_type = b'special judge' if b'Special Judge' in [ x.text for x in limits ] else b'regular'
            origin = self.url_problem(pid)
            limits = {b'default': (
                          int(limits[0].contents[1].strip()[:-2]),
                          int(limits[2].contents[1].strip()[:-1])), 
               b'java': (
                       3 * int(limits[0].contents[1].strip()[:-2]),
                       int(limits[2].contents[1].strip()[:-1]))}
            samples_input = []
            samples_output = []
            samples = {}
            descriptions = []
            category = b''
            tags = []
            append_html = b''
            items = plm.find_next_siblings()
            n = len(items)
            assert n % 2 == 0
            for i in range(0, n, 2):
                sub_title = items[i].text.strip()
                sub_content = items[(i + 1)]
                if sub_title == b'Sample Input':
                    samples_input.append(sub_content.text)
                elif sub_title == b'Sample Output':
                    samples_output.append(sub_content.text)
                elif sub_title == b'Source':
                    category = sub_content.text
                else:
                    descriptions.append((
                     sub_title,
                     self.replace_image(str(sub_content))))

            assert len(samples_input) == len(samples_output)
            n = len(samples_input)
            for i in range(n):
                samples[i + 1] = (
                 samples_input[i], samples_output[i])

            compatible_data = {}
            for key in self.compatible_problem_fields:
                compatible_data[key] = eval(key)

            return (
             True, compatible_data)
        else:
            return (
             False, b'获取题目：http方法错误，请检查网络后重试')

    def submit_code(self, source, lang, pid):
        if not self.is_login():
            success, info = self.login()
            if not success:
                return (False, info)
        data = dict(problem_id=pid, language=self.get_languages()[lang.upper()], source=source, submit=b'Submit', encoded=b'0')
        ret = self.post(self.url_submit, data)
        if ret:
            if ret.url == self.url_status[:-1]:
                ok, info = self.get_result()
                if ok:
                    return (True, info[b'rid'])
                return (False, b'提交代码（获取提交id）：' + info)
            else:
                html = ret.read().decode(b'utf-8')
                soup = BeautifulSoup(html, b'html5lib')
                err = soup.find(b'font', {b'size': 4})
                if err and err.text == b'Error Occurred':
                    return (False, soup.find(b'li').text)
                return (False, b'提交代码：未知错误')

        else:
            return (
             False, b'提交代码：http方法错误，请检查网络后重试')

    def _get_result(self, url_result):
        ret = self.get(url_result)
        if ret:
            html = ret.read().decode(b'utf-8')
            soup = BeautifulSoup(html, b'html5lib')
            table = soup.find(b'table', {b'class': b'a'})
            trs = table.find_all(b'tr')
            if len(trs) <= 1:
                return (False, b'没有结果')
            data = {b'rid': trs[1].contents[0].text.strip(), 
               b'status': trs[1].contents[3].text.strip(), 
               b'memory': trs[1].contents[4].text.strip(), 
               b'time': trs[1].contents[5].text.strip(), 
               b'ce_info': b''}
            if data[b'status'] == b'Compile Error':
                ret, info = self.get_compile_error_info(data[b'rid'])
                data[b'ce_info'] = info if ret else b''
            return (
             True, data)
        else:
            return (
             False, b'获取结果：http方法错误，请检查网络后重试')

    def get_result(self):
        return self.get_result_by_user(self.handle)

    def get_result_by_user(self, handle):
        url = self.url_status + (b'user_id={}').format(handle)
        return self._get_result(url)

    def get_result_by_rid(self, rid):
        rid = int(rid)
        url = self.url_status + (b'top={}').format(rid + 1)
        return self._get_result(url)

    def get_compile_error_info(self, rid):
        url = self.url_home + (b'showcompileinfo?solution_id={}').format(rid)
        ret = self.get(url)
        if ret:
            html = ret.read().decode(b'utf-8')
            soup = BeautifulSoup(html, b'html5lib')
            pre = soup.find(b'pre')
            if pre:
                return (True, pre.text)
            return (True, None)
        else:
            return (
             False, b'获取编译错误信息：http方法错误，请检查网络后重试')
        return