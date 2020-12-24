# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_html_comments/sanitize.py
# Compiled at: 2016-09-11 20:15:06
from BeautifulSoup import BeautifulSoup
import re

def sanitize(html):
    whitelist = [
     'em', 'i', 'strong', 'u', 'a', 'b', 'p', 'br', 'code', 'pre']
    attr_whitelist = {'a': ['href', 'title', 'hreflang']}
    blacklist = [
     'script', 'style']
    attributes_with_urls = [
     'href', 'src']
    soup = BeautifulSoup(html)
    for tag in soup.findAll():
        if tag.name.lower() in blacklist:
            tag.extract()
        elif tag.name.lower() in whitelist:
            for attr in tag.attrs:
                if tag.name.lower() in attr_whitelist and attr[0].lower() in attr_whitelist[tag.name.lower()]:
                    if attr[0].lower() in attributes_with_urls:
                        if not re.match('(https?|ftp)://', attr[1].lower()):
                            tag.attrs.remove(attr)
                else:
                    tag.attrs.remove(attr)

        else:
            tag.name = 'span'
            tag.attrs = []

    safe_html = unicode(soup)
    safe_html = re.sub('<!--[.\\n]*?-->', '', safe_html)
    return safe_html