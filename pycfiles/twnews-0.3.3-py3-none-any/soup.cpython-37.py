# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/soup.py
# Compiled at: 2019-08-13 04:42:15
# Size of source mod 2**32: 15077 bytes
"""
新聞分解模組
"""
import io, re, copy, lzma, hashlib, os, os.path
from datetime import datetime
import requests, requests.exceptions
from bs4 import BeautifulSoup
import twnews.common

def get_cache_filepath(channel, uri):
    """
    取得快取檔案路徑
    """
    cache_id = hashlib.md5(uri.encode('ascii')).hexdigest()
    path = '{}/{}.html.xz'.format(twnews.common.get_cache_dir(channel), cache_id)
    return path


def url_follow_redirection(url, proxy_first):
    """
    取得轉址後的 URL
    """
    logger = twnews.common.get_logger()
    session = twnews.common.get_session(proxy_first)
    old_url = url
    new_url = ''
    done = False
    while not done:
        try:
            resp = session.head(old_url)
            status = resp.status_code
            if status in (301, 302):
                dest = resp.headers['Location']
                if dest.startswith('//'):
                    new_url = 'https:' + dest
                else:
                    if dest.startswith('/'):
                        new_url = old_url[0:old_url.find('/', 10)] + dest
                    else:
                        new_url = dest
                logger.debug('===== 轉址細節 =====')
                logger.debug('HTTP Status: %d', status)
                logger.debug('Location: %s', dest)
                logger.debug('原始 URL: %s', old_url)
                logger.debug('變更 URL: %s', new_url)
                logger.debug('====================')
                old_url = new_url
            else:
                if status == 200:
                    done = True
                else:
                    logger.error('檢查轉址過程發生錯誤')
                    logger.error('HTTP Status: %d，', status)
                    logger.error('URL: %s，', old_url)
                    done = True
        except requests.exceptions.ConnectionError as ex:
            try:
                logger.error('檢查轉址過程連線失敗: %s', ex)
                done = True
            finally:
                ex = None
                del ex

    return old_url


def url_force_https(url):
    """
    強制使用 https
    """
    logger = twnews.common.get_logger()
    if url.startswith('http://'):
        new_url = 'https://' + url[7:]
        logger.debug('原始 URL: %s', url)
        logger.debug('變更 URL: %s', new_url)
    else:
        new_url = url
    if new_url.startswith('https://home.appledaily.com.tw'):
        new_url = 'http://home.appledaily.com.tw' + new_url[30:]
    return new_url


def url_force_ltn_mobile(url):
    """
    強制使用自由時報行動版
    """
    logger = twnews.common.get_logger()
    new_url = url
    sub_chanels = '^https://(3c|auto|ec|ent|food|istyle|market|playing|sports).ltn.com.tw/[^m].+'
    if url.startswith('https://news.ltn.com.tw'):
        new_url = 'https://m.ltn.com.tw' + url[len('https://news.ltn.com.tw'):]
        logger.debug('原始 URL: %s', url)
        logger.debug('變更 URL: %s', new_url)
    else:
        if re.match(sub_chanels, url):
            uri_pos = url.find('/', 10)
            new_url = url[:uri_pos] + '/m' + url[uri_pos:]
            logger.debug('原始 URL: %s', url)
            logger.debug('變更 URL: %s', new_url)
    return new_url


def soup_from_website(url, channel, refresh, proxy_first):
    """
    網址轉換成 BeautifulSoup 4 物件
    """
    logger = twnews.common.get_logger()
    session = twnews.common.get_session(proxy_first)
    soup = None
    rawlen = 0
    uri = url[url.find('/', 10):]
    path = get_cache_filepath(channel, uri)
    if os.path.isfile(path):
        if not refresh:
            logger.debug('發現快取, URL: %s', url)
            logger.debug('載入快取, PATH: %s', path)
            soup, rawlen = soup_from_file(path)
    if soup is None:
        logger.debug('GET URL: %s', url)
        try:
            resp = session.get(url, allow_redirects=False)
            if resp.status_code == 200:
                logger.debug('回應 200 OK')
                if resp.headers['content-type'].find('charset=') == -1:
                    content = resp.content.decode('utf-8')
                else:
                    content = resp.text
                soup = BeautifulSoup(content, 'lxml')
                rawlen = len(resp.text.encode('utf-8'))
                with lzma.open(path, 'wt') as (cache_file):
                    logger.debug('寫入快取: %s', path)
                    cache_file.write(content)
            else:
                logger.warning('回應碼: %d', resp.status_code)
        except requests.exceptions.ConnectionError as ex:
            try:
                logger.error('連線失敗: %s', ex)
            finally:
                ex = None
                del ex

    return (
     soup, rawlen)


def soup_from_file(file_path):
    """
    本地檔案轉換成 BeautifulSoup 4 物件
    """
    html = None
    soup = None
    clen = 0
    if file_path.endswith('.xz'):
        with lzma.open(file_path, 'rt') as (cache_file):
            html = cache_file.read()
    else:
        with open(file_path, 'rt') as (cache_file):
            html = cache_file.read()
    if html is not None:
        soup = BeautifulSoup(html, 'lxml')
        clen = len(html.encode('utf-8'))
    return (soup, clen)


def scan_author(article):
    """
    從新聞內文找出記者姓名
    """
    patterns = [
     ('(記者|中心)(\\w{2,5})[/／╱](.+報導|特稿)', 2),
     ('文[/／╱]記者(\\w{2,5})', 1),
     ('[\\(（](\\w{2,5})[/／╱].+報導[\\)）]', 1),
     ('記者(\\w{2,3}).{2}[縣市]?\\d{1,2}日電', 1),
     ('(記者|遊戲角落 )(\\w{2,5})$', 2),
     ('\\s(\\w{2,5})[/／╱].+報導$', 1),
     ('（譯者：(\\w{2,5})/.+）', 1),
     ('【(\\w{2,5})╱.+報導】', 1)]
    exclude_list = [
     '國際中心',
     '地方中心',
     '社會中心',
     '攝影']
    for patt, gidx in patterns:
        pobj = re.compile(patt)
        match = pobj.search(article)
        if match is not None and match.group(1) not in exclude_list:
            return match.group(gidx)


class NewsSoup:
    __doc__ = '\n    新聞分解器\n    '

    def __init__(self, path, refresh=False, proxy_first=False):
        """
        建立新聞分解器
        """
        self.path = path
        self.refresh = refresh
        self.proxy_first = proxy_first
        self.loaded = False
        self.soup = None
        self.rawlen = 0
        self.logger = twnews.common.get_logger()
        self.channel = twnews.common.detect_channel(path)
        self.cache = {'title':None, 
         'date_raw':None, 
         'date':None, 
         'author':None, 
         'contents':None, 
         'tags':None}
        if self.channel == '':
            self.logger.error('不支援的新聞台，請檢查設定檔')
            return
        if self.path.startswith('http'):
            self.path = url_follow_redirection(self.path, self.proxy_first)
            self.path = url_force_https(self.path)
            if self.channel == 'ltn':
                self.path = url_force_ltn_mobile(self.path)
        layout = 'mobile'
        layout_list = twnews.common.get_channel_conf(self.channel, 'layout_list')
        for item in layout_list:
            if self.path.startswith(item['prefix']):
                layout = item['layout']

        self.conf = twnews.common.get_channel_conf(self.channel, layout)

    def __get_soup(self):
        self.loaded = self.loaded or True
        try:
            if self.path.startswith('http'):
                self.logger.debug('從網路載入新聞')
                self.soup, self.rawlen = soup_from_website(self.path, self.channel, self.refresh, self.proxy_first)
            else:
                self.logger.debug('從檔案載入新聞')
                self.soup, self.rawlen = soup_from_file(self.path)
        except requests.ConnectionError as ex:
            try:
                self.logger.error('因連線問題，無法載入新聞: %s', ex)
                self.logger.error(self.path)
            finally:
                ex = None
                del ex

        except FileNotFoundError as ex:
            try:
                self.logger.error('檔案不存在，無法載入新聞: %s', ex)
                self.logger.error(self.path)
            finally:
                ex = None
                del ex

        except TypeError as ex:
            try:
                self.logger.error('頻道不存在，無法載入新聞: %s', ex)
                self.logger.error(self.path)
            finally:
                ex = None
                del ex

        if self.soup is None:
            self.logger.error('無法轉換 BeautifulSoup，可能是網址或檔案路徑錯誤')
        return self.soup

    def title(self):
        """
        取得新聞標題
        """
        soup = self._NewsSoup__get_soup()
        if soup is None:
            return
            if self.cache['title'] is None:
                nsel = self.conf['title_node']
                found = soup.select(nsel)
                if found:
                    node = copy.copy(found[0])
                    for child_node in node.select('*'):
                        child_node.extract()

                    self.cache['title'] = node.text.strip()
                    if len(found) > 1:
                        self.logger.warning('找到多組標題節點 (新聞台: %s)', self.channel)
        else:
            self.logger.error('找不到標題節點 (新聞台: %s)', self.channel)
        return self.cache['title']

    def date_raw(self):
        """
        取得原始時間字串
        """
        soup = self._NewsSoup__get_soup()
        if soup is None:
            return
            if self.cache['date_raw'] is None:
                nsel = self.conf['date_node']
                found = soup.select(nsel)
                if found:
                    node = copy.copy(found[0])
                    if not ('date_with_children' not in self.conf or self.conf['date_with_children']):
                        for child_node in node.select('*'):
                            child_node.extract()

                    self.cache['date_raw'] = node.text.strip()
                    if len(found) > 1:
                        self.logger.warning('發現多組日期節點 (新聞台: %s)', self.channel)
        else:
            self.logger.error('找不到日期時間節點 (新聞台: %s)', self.channel)
        return self.cache['date_raw']

    def date(self):
        """
        取得 datetime.datetime 格式的時間
        """
        soup = self._NewsSoup__get_soup()
        if soup is None:
            return
        if self.cache['date'] is None:
            formats = self.conf['date_format']
            if isinstance(formats, str):
                formats = [
                 formats]
            for dfmt in formats:
                try:
                    self.cache['date'] = datetime.strptime(self.date_raw(), dfmt)
                except TypeError as ex:
                    try:
                        errmsg = '日期格式分析失敗 {} (新聞台: {})'.format(ex, self.channel)
                    finally:
                        ex = None
                        del ex

                except ValueError as ex:
                    try:
                        errmsg = '日期格式分析失敗 {} (新聞台: {})'.format(ex, self.channel)
                    finally:
                        ex = None
                        del ex

            if self.cache['date'] is None:
                self.logger.error(errmsg)
        return self.cache['date']

    def author(self):
        """
        取得新聞記者/社論作者
        """
        soup = self._NewsSoup__get_soup()
        if soup is None:
            return
            if self.cache['author'] is None:
                nsel = self.conf['author_node']
                if nsel != '':
                    if isinstance(nsel, str):
                        selectors = [
                         nsel]
                    else:
                        selectors = nsel
                    for nsel in selectors:
                        found = soup.select(nsel)
                        if found:
                            node = copy.copy(found[0])
                            for child_node in node.select('*'):
                                child_node.extract()

                            author_raw = node.text.strip()
                            if author_raw[0] != '記' and len(author_raw) <= 5:
                                self.cache['author'] = author_raw
                            else:
                                self.cache['author'] = scan_author(author_raw)
                            if len(found) > 1:
                                self.logger.warning('找到多組記者姓名 (新聞台: %s)', self.channel)
                            break
                        else:
                            self.logger.warning('找不到記者節點 (新聞台: %s)', self.channel)

        else:
            contents = self.contents()
            if contents is not None:
                self.cache['author'] = scan_author(contents)
                if self.cache['author'] is None:
                    self.logger.warning('內文中找不到記者姓名 (新聞台: %s)', self.channel)
            else:
                self.logger.error('因為沒有內文所以無法比對記者姓名 (新聞台: %s)', self.channel)
        return self.cache['author']

    def contents(self, limit=0):
        """
        取得新聞內文
        """
        soup = self._NewsSoup__get_soup()
        if soup is None:
            return
            if self.cache['contents'] is None:
                nsel = self.conf['article_node']
                found = soup.select(nsel)
                if found:
                    contents = io.StringIO()
                    for node in found:
                        contents.write(node.text.strip())

                    self.cache['contents'] = contents.getvalue()
                    contents.close()
        else:
            self.logger.error('找不到內文節點 (新聞台: %s)', self.channel)
        if isinstance(self.cache['contents'], str):
            if limit > 0:
                return self.cache['contents'][0:limit]
        return self.cache['contents']

    def effective_text_rate(self):
        """
        計算有效內容率 (有效內容位元組數/全部位元組數)
        """
        soup = self._NewsSoup__get_soup()
        if soup is None or self.rawlen == 0:
            return 0
        data = [
         self.title(),
         self.author(),
         self.date_raw(),
         self.contents()]
        useful_len = 0
        for datum in data:
            if datum is not None:
                useful_len += len(datum.encode('utf-8'))

        return useful_len / self.rawlen