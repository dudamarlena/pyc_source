# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maxxn/__init__.py
# Compiled at: 2014-08-13 08:45:51
import sys, requests
from bs4 import BeautifulSoup

def main():
    url = sys.argv[1]
    locate = sys.argv[2]
    content = _get_page_content(url)
    print _get_sizzle_res(content, locate)


def _get_page_content(url):
    page = requests.get(url)
    return page.content


def _get_sizzle_res(content, locate):
    html = BeautifulSoup(content)
    return html.select(locate)


if __name__ == '__main__':
    main()