# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/youdao/spider.py
# Compiled at: 2019-02-16 23:51:48
import sys, bs4, urllib, requests
from contextlib import contextmanager

class Spider(object):

    def __init__(self, lang='eng', timeout=3):
        self.__html_url = ('http://dict.youdao.com/w/{}/').format(lang)
        self.__headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36', 
           'Cookie': 'domain=.youdao.com'}
        self.__timeout = timeout

    @contextmanager
    def soup(self, target_word):
        """get bs soup context"""
        url = self.__html_url + urllib.quote(target_word.replace('/', ''))
        try:
            resp = requests.get(url, timeout=self.__timeout, headers=self.__headers)
            if not resp.status_code == 200:
                sys.stderr.write(('链接 `{}` 非法状态码: {}\r\n').format(url, resp.status_code))
            else:
                yield bs4.BeautifulSoup(resp.content, 'html.parser')
        except requests.Timeout:
            sys.stderr.write(('链接 `{}` 请求超时\r\n').format(url))
            yield
        except requests.ConnectionError:
            sys.stderr.write(('链接 `{}` 连接失败\r\n').format(url))
            yield
        except Exception as e:
            sys.stderr.write(('链接 `{}` 连接时发生未知错误\r\n').format(e.message))
            yield

        return

    def deploy(self, word):
        """format spider raw data"""
        with self.soup(word) as (soup):
            if soup is None:
                return (None, None)
            else:
                match = soup.find(class_='keyword')
                if match:
                    wordbook = soup.find(class_='wordbook-js')
                    _pronounce = wordbook.find_all(class_='pronounce')
                    pronounces = []
                    translate = []
                    web_translate = []
                    word_phrase = []
                    if not _pronounce:
                        _pronounce = wordbook.find_all(class_='phonetic')
                    for p in _pronounce:
                        temp = p.get_text().replace(' ', '').replace('\n', '')
                        if not temp:
                            continue
                        pronounces.append(p.get_text().replace(' ', '').replace('\n', ''))

                    _trans = soup.find(class_='trans-container')
                    if _trans and _trans.find('ul'):
                        _normal_trans = _trans.find('ul').find_all('li')
                        if not _normal_trans:
                            _normal_trans = _trans.find('ul').find_all(class_='wordGroup')
                        for _nt in _normal_trans:
                            title = _nt.find(class_='contentTitle')
                            type_ = _nt.find('span')
                            if title and type_ and title != type_:
                                title = title.get_text()
                                type_ = type_.get_text()
                            else:
                                title = _nt.get_text()
                                type_ = ''
                            tmp = (type_ + title).replace('\n', '')
                            if tmp.count(' ') > 4:
                                tmp = tmp.replace('  ', '')
                            translate.append(tmp)

                    _web_trans = soup.find(id='tWebTrans')
                    if _web_trans:
                        for i in _web_trans.find_all('span', class_=None):
                            temp = i.get_text().replace('\n', '').replace(' ', '')
                            if not temp:
                                continue
                            web_translate.append(temp)

                        _word_phrase = _web_trans.find(id='webPhrase')
                        if _word_phrase:
                            for i in _word_phrase.find_all(class_='wordGroup'):
                                title = i.find(class_='contentTitle')
                                if not title:
                                    continue
                                title = title.get_text()
                                word_phrase.append({'phrase': title, 
                                   'explain': i.get_text().replace('\n', '').replace(title, '').replace(' ', '')})

                    return (
                     0,
                     {'pronounces': pronounces, 
                        'translate': translate, 
                        'web_translate': web_translate})
                similar = soup.find(class_='error-typo')
                if similar:
                    possibles = []
                    similar = similar.find_all(class_='typo-rel')
                    for s in similar:
                        title = s.find(class_='title')
                        content = s.get_text()
                        if title:
                            title = title.get_text().replace(' ', '').replace('\n', '')
                            content = content.replace(title, '').replace(' ', '').replace('\n', '')
                        else:
                            continue
                        possibles.append({'possible': title, 
                           'explain': content})

                    return (
                     1,
                     {'possibles': possibles})
                return (None, None)

        return


if __name__ == '__main__':
    print Spider().deploy('chinese')