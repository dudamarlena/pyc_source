# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/rss-miner/package/src/rss_miner/content.py
# Compiled at: 2017-05-14 13:29:46
# Size of source mod 2**32: 1482 bytes
from bs4 import BeautifulSoup
import requests

def fetch_article_content(entry, content_tag=None, header=None):
    """Return a list of all paragraph tags in the entry """
    response = requests.get((entry.link), headers=header)
    if not response.ok:
        raise IOError('Could not fetch article content, encountered: {} from {}'.format(response.status_code, response.url))
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        if content_tag:
            parent_tag = soup.select(content_tag)
            if parent_tag:
                p_tags = parent_tag[0].find_all(name='p')
            else:
                p_tags = []
        else:
            p_tags = find_content_p_tags(soup)
    paragraphs = []
    for p in p_tags:
        text = p.get_text()
        if text is not None:
            text = text.strip()
            paragraphs.append(text)

    return paragraphs


def find_content_p_tags(soup):
    title_string = soup.find_all(string="Gordon Brown accuses Tories of 'waging war against poor'")[0]
    enclosing_tag = title_string.find_parent().find_parent()
    p_tags = enclosing_tag.find_all(name='p')
    p_tags = [p for p in p_tags if len(p.text.split()) > 3]
    return p_tags