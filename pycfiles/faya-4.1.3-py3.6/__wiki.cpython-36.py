# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/faya/lib/__wiki.py
# Compiled at: 2018-07-04 01:37:37
# Size of source mod 2**32: 1952 bytes
from lxml import html
import requests
from pyquery import PyQuery
import re, sys

def get(key):
    try:
        jp_reg = re.compile('[ぁ-んァ-ヶ]')
        en_reg = re.compile('[a-zA-Z]')
        language = 'zh'
        if re.findall(jp_reg, key):
            language = 'ja'
        else:
            if re.findall(en_reg, key):
                language = 'en'
        print('from ' + language + '.wiki')
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 
         'Referer':'https://www.sanseido.biz/', 
         'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
         'Connection':'close', 
         'authority':f"{language}.wikipedia.org"}
        s = requests.session()
        s.keep_alive = False
        page = s.get(f"https://{language}.wikipedia.org/wiki/{key}", headers=headers)
        page.encoding = 'UTF-8'
        tree = html.fromstring(page.text)
        p1 = tree.xpath('//*[@id="mw-content-text"]/div/p[1]')
        if not p1:
            return f"wiki里查不到 {key}"
        p1_text = html.tostring((p1[0]), encoding='UTF-8')
        de = PyQuery(p1_text.decode('UTF-8')).text()
        if 'refer' in de or '可指' in de:
            refer = tree.xpath('//*[@id="mw-content-text"]/div/ul[1]/li')
            for each in refer:
                refer_text = html.tostring(each, encoding='UTF-8')
                refer_link = PyQuery(refer_text.decode('UTF-8')).text()
                de += '\n' + refer_link

        return de.strip()
    except Exception as e:
        return f"似乎有些问题:\n{e}"


if __name__ == '__main__':
    print(get('apple'))