# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/search.py
# Compiled at: 2019-08-13 04:50:26
# Size of source mod 2**32: 13812 bytes
"""
新聞搜尋模組
"""
import re, time, os.path, urllib.parse
from string import Template
from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Tag
import twnews.common
from twnews.soup import NewsSoup

def visit_dict(dict_node, path):
    """
    用 CSS Selector 的形式拜訪 dict
    """
    keys = []
    if path != '':
        keys = path.split(' > ')
    visited = dict_node
    for key in keys:
        visited = visited[key]

    return visited


def filter_duplicated(results):
    """
    以連結為鍵值去重複化
    """
    filtered = []
    logger = twnews.common.get_logger()
    for cidx, result in enumerate(results):
        duplicated = False
        pidx = -1
        for pidx in range(cidx):
            previous = results[pidx]
            if result['link'] == previous['link']:
                duplicated = True
                break

        if not duplicated:
            filtered.append(result)
        else:
            logger.warning('查詢結果的 %d, %d 筆重複，新聞網址 %s', cidx, pidx, result['link'])

    return filtered


class NewsSearchException(Exception):
    __doc__ = '\n    新聞搜尋例外\n    '


class NewsSearch:
    __doc__ = '\n    新聞搜尋器\n    '

    def __init__(self, channel, limit=25, beg_date=None, end_date=None, proxy_first=False):
        """
        配置新聞搜尋器
        """
        if channel == 'chinatimes':
            msg = '頻道 {} 不支援搜尋功能'.format(channel)
            raise NewsSearchException(msg)
        else:
            if beg_date is None or end_date is None:
                if end_date is not None:
                    msg = '遺漏了開始日期'
                    raise NewsSearchException(msg)
                if beg_date is not None:
                    msg = '遺漏了結束日期'
                    raise NewsSearchException(msg)
            self.params = {'beg_date':None, 
             'end_date':None, 
             'channel':channel, 
             'limit':limit, 
             'proxy_first':proxy_first}
            try:
                if beg_date is not None:
                    self.params['beg_date'] = datetime.strptime(beg_date, '%Y-%m-%d')
                if end_date is not None:
                    self.params['end_date'] = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                msg = '日期必須是 ISO 格式 (yyyy-mm-dd)'
                raise NewsSearchException(msg)

            if self.params['beg_date'] is not None:
                delta = self.params['end_date'] - self.params['beg_date']
                if delta.days < 0:
                    msg = '開始日期必須小於或等於結束日期'
                    raise NewsSearchException(msg)
                if delta.days > 90:
                    if channel == 'ltn':
                        msg = '頻道 {} 的日期條件必須在 90 天內'.format(channel)
                        raise NewsSearchException(msg)
        self.conf = twnews.common.get_channel_conf(channel, 'search')
        self.context = None
        self.result = {'pages':0, 
         'elapsed':0, 
         'items':[]}
        self.url_prefix = {'host':'', 
         'base':''}

    def by_keyword(self, keyword, title_only=False):
        """
        關鍵字搜尋
        """
        logger = twnews.common.get_logger()
        page = 1
        results = []
        no_more = False
        begin_time = time.time()
        if self.params['beg_date'] is not None:
            if self.params['channel'] in ('ettoday', 'udn'):
                page = self._NewsSearch__flip_to_end_date(keyword)
        while not no_more:
            if len(results) < self.params['limit']:
                self._NewsSearch__load_page(keyword, page)
                result_nodes = self._NewsSearch__result_nodes()
                result_count = len(result_nodes)
                logger.info('第 %d 頁: 有 %d 筆搜尋結果', page, result_count)
                if result_count > 0:
                    for node in result_nodes:
                        date_inst = self._NewsSearch__parse_date_node(node)
                        if self.params['beg_date'] is not None:
                            if self.params['channel'] not in ('appledaily', 'ltn'):
                                if date_inst > self.params['end_date']:
                                    continue
                                if date_inst < self.params['beg_date']:
                                    no_more = True
                                    break
                        title = self._NewsSearch__parse_title_node(node)
                        link = self._NewsSearch__parse_link_node(node)
                        if not title_only or keyword in title:
                            results.append({'title':title, 
                             'link':link, 
                             'date':date_inst})
                            if len(results) == self.params['limit']:
                                break

                else:
                    no_more = True
                page += 1

        self.result = {'pages':page - 1,  'elapsed':time.time() - begin_time, 
         'items':filter_duplicated(results)}
        return self

    def to_dict_list(self):
        """
        回傳新聞查詢結果
        """
        return self.result['items']

    def to_soup_list(self):
        """
        回傳新聞查詢結果的分解器
        """
        soup_list = []
        for result in self.result['items']:
            nsoup = NewsSoup((result['link']), proxy_first=(self.params['proxy_first']))
            soup_list.append(nsoup)

        return soup_list

    def elapsed(self):
        """
        耗費時間
        """
        return self.result['elapsed']

    def pages(self):
        """
        頁數
        """
        return self.result['pages']

    def __flip_to_end_date(self, keyword):
        """
        回傳篩選時間範圍的開始頁數
        """
        page_range = {'lower':1, 
         'upper':1000}
        date_range = {'lower':datetime.fromtimestamp(0), 
         'upper':datetime.today()}
        self._NewsSearch__load_page(keyword, 1)
        node = self.context.select(self.conf['last_page'])[0]
        if 'page_pattern' in self.conf:
            match = re.search(self.conf['page_pattern'], node.text)
            if match:
                page_range['upper'] = int(match.group(1))
            else:
                page_range['upper'] = -1
        else:
            try:
                page_range['upper'] = int(node.text)
            except ValueError:
                page_range['upper'] = -1

        if page_range['upper'] == -1:
            return 1
        date_range['upper'] = self._NewsSearch__parse_date_node(self._NewsSearch__result_nodes()[0])
        if date_range['upper'] < self.params['end_date']:
            return 1
        self._NewsSearch__load_page(keyword, page_range['upper'])
        date_range['lower'] = self._NewsSearch__parse_date_node(self._NewsSearch__result_nodes()[(-1)])
        if date_range['lower'] > self.params['end_date']:
            return -1
        page_dist = page_range['upper'] - page_range['lower']
        prev_dist = page_range['upper'] - page_range['lower'] + 1
        logger = twnews.common.get_logger()
        logger.info('page: %d ~ %d, date: %s ~ %s', page_range['lower'], page_range['upper'], date_range['upper'], date_range['lower'])
        while page_dist < prev_dist:
            mid_page = (page_range['lower'] + page_range['upper']) // 2
            self._NewsSearch__load_page(keyword, mid_page)
            middle_udt = self._NewsSearch__parse_date_node(self._NewsSearch__result_nodes()[0])
            middle_ldt = self._NewsSearch__parse_date_node(self._NewsSearch__result_nodes()[(-1)])
            if middle_udt > self.params['end_date']:
                page_range['lower'] = mid_page
                date_range['upper'] = middle_udt
            if middle_ldt < self.params['end_date']:
                page_range['upper'] = mid_page
                date_range['lower'] = middle_ldt
            prev_dist = page_dist
            page_dist = page_range['upper'] - page_range['lower']
            logger.info('page: %d ~ %d, date: %s ~ %s, mid=%d', page_range['lower'], page_range['upper'], date_range['upper'], date_range['lower'], mid_page)

        return page_range['lower']

    def __load_page(self, keyword, page):
        replacement = {'PAGE':page, 
         'KEYWORD':urllib.parse.quote_plus(keyword)}
        url = Template(self.conf['url']).substitute(replacement)
        if self.params['beg_date'] is not None:
            if self.params['channel'] in ('appledaily', 'ltn'):
                url += self.params['beg_date'].strftime(self.conf['begin_date_format'])
                url += self.params['end_date'].strftime(self.conf['end_date_format'])
        else:
            session = twnews.common.get_session(proxy_first=(self.params['proxy_first']))
            logger = twnews.common.get_logger()
            logger.info('新聞搜尋 %s', url)
            resp = session.get(url, allow_redirects=False)
            if resp.status_code == 200:
                logger.debug('回應 200 OK')
                ctype = resp.headers['Content-Type']
                if 'text/html' in ctype:
                    self.context = BeautifulSoup(resp.text, 'lxml')
                if 'application/json' in ctype:
                    self.context = resp.json()
            else:
                if resp.status_code == 404:
                    logger.debug('回應 404 Not Found，視為沒有更多查詢結果')
                    self.context = None
                else:
                    logger.warning('回應碼: %s', resp.status_code)
                    self.context = None

    def __result_nodes(self):
        """
        取查詢結果的 soup 或 dict
        """
        if self.context is not None:
            if isinstance(self.context, BeautifulSoup):
                return self.context.select(self.conf['result_node'])
            return visit_dict(self.context, self.conf['result_node'])
        return []

    def __parse_title_node(self, result_node):
        """
        單筆查詢結果範圍內取標題文字
        """
        if isinstance(result_node, Tag):
            title_node = result_node.select(self.conf['title_node'])[0]
            title = title_node.text.strip()
        else:
            title = visit_dict(result_node, self.conf['title_node'])
        return title

    def __parse_date_node(self, result_node):
        """
        單筆查詢結果範圍內取報導日期
        """
        if isinstance(result_node, Tag):
            date_node = result_node.select(self.conf['date_node'])[0]
            if 'date_pattern' in self.conf:
                match = re.search(self.conf['date_pattern'], date_node.text)
                date_text = match.group(0)
            else:
                date_text = date_node.text.strip()
        else:
            date_text = visit_dict(result_node, self.conf['date_node'])
        date_inst = datetime.strptime(date_text, self.conf['date_format'])
        return date_inst

    def __parse_link_node(self, result_node):
        """
        單筆查詢結果範圍內取新聞連結
        """
        if isinstance(result_node, Tag):
            link_node = result_node.select(self.conf['link_node'])[0]
            href = link_node['href']
        else:
            href = visit_dict(result_node, self.conf['link_node'])
        if href.startswith('https://'):
            return href
            if href.startswith('/'):
                if self.url_prefix['host'] == '':
                    match = re.match('^https://([^/]+)/', self.conf['url'])
                    self.url_prefix['host'] = match.group(1)
                return 'https://{}{}'.format(self.url_prefix['host'], href)
            if self.url_prefix['base'] == '':
                nodes = self.context.select('head > base')
                if len(nodes) == 1:
                    self.url_prefix['base'] = nodes[0]['href']
        else:
            base_end = self.conf['url'].rfind('/')
            self.url_prefix['base'] = self.conf['url'][0:base_end + 1]
        full_url = self.url_prefix['base'] + href
        spos = full_url.find('/', 10)
        reduced_url = full_url[0:spos] + os.path.realpath(full_url[spos:])
        return reduced_url