# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ubuntu/workspace/src/collective/awstats_hitcounter/browser/utils.py
# Compiled at: 2015-10-13 16:05:08
import requests
from os import getenv
from AccessControl import Unauthorized
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse
from plone import api
blacklist = [
 '/acl_users/',
 '/search_rss',
 '/login_form',
 '/login',
 '/request_login_pre',
 '/search.html',
 '/request_login',
 '/search.json',
 '/RSS',
 '/search',
 '/@@flexijson_view',
 '/@@usergroup-userprefs',
 '/awstats_hitcounter_view',
 '/portal_kss/',
 '/login_failed',
 '/search_form',
 '/contact-info',
 '/@@user',
 '/@@user-information']
type_whitelist = [
 'News Item', 'Page', 'Link', 'File']

def counter(path, pattern, hits=False):
    """ usage
    counter(path, pattern)
    # returns the number of views for a given path
    counter(path, pattern, hits=True)
    # returns the number of hits for a given path
    """
    url = pattern.format(path)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    scrape_pattern_b = soup.find('b', text=path)
    trs = scrape_pattern_b.findAllNext('tr')
    hit_count = 0
    for tr in trs:
        tds = tr.findAll('td')
        attrs_ = getattr(tds[0].a, 'attrs', None)
        if attrs_:
            attrs = dict(attrs_)
            href = attrs['href']
            url = urlparse(href)
            if url.path == path and hits == False:
                return int(tds[1].text)
            if hits == True:
                hit_count = hit_count + int(tds[1].text)

    if hits == True:
        return hit_count
    else:
        return 0


def get_urls(url, blacklist=blacklist, limit=10):
    r = requests.get(url)
    _links = []
    for link in BeautifulSoup(r.text, parseOnlyThese=SoupStrainer('a')):
        if link.get('target') in ('url', ):
            _links.append(link['href'])

    for blacklistitem in blacklist:
        _links = [ linkitem for linkitem in _links if blacklistitem not in linkitem
                 ]

    if limit:
        return _links[:limit]


def filter_urls(urls, type_white_list=type_whitelist, items_to_show=None, prevent_direct_downloads=True, read_from_the_global_registry=True):
    if read_from_the_global_registry:
        prevent_direct_downloads = api.portal.get_registry_record('awstats_hitcounter.prevent_direct_downloads')
        black_list = api.portal.get_registry_record('awstats_hitcounter.black_list')
        type_white_list = api.portal.get_registry_record('awstats_hitcounter.type_white_list')
    if prevent_direct_downloads:
        popular_urls_no_downloads = []
        for p_url in urls:
            if p_url.endswith('/at_download/file'):
                p_url = p_url.replace('at_download/file', '')
                popular_urls_no_downloads.append(p_url)
            else:
                popular_urls_no_downloads.append(p_url)

        urls = popular_urls_no_downloads
    popular_urls_remove_imagethumbs = []
    for p_url in urls:
        if p_url.endswith('/image_thumb'):
            p_url = p_url.replace('image_thumb', '')
            popular_urls_remove_imagethumbs.append(p_url)
        else:
            popular_urls_remove_imagethumbs.append(p_url)

    urls = popular_urls_remove_imagethumbs
    if getenv('DUMP_RAW_AWSTATS_URLS', None):
        return [ {'title': url, 'url': url} for url in urls ]
    else:
        popular_urls_ = [ (get_content_by_path(urlparse(p_url).path), p_url) for p_url in urls if get_content_by_path(urlparse(p_url).path) ]
        popular_urls = []
        for p_url in popular_urls_:
            if p_url[0]:
                try:
                    if p_url[0].Type() in type_white_list:
                        popular_urls.append({'title': p_url[0].Title(), 'url': p_url[1]})
                except AttributeError:
                    print 'bad url: %s' % p_url[1]

        if items_to_show:
            if len(popular_urls) > items_to_show:
                return popular_urls[:items_to_show]
        return popular_urls


def get_content_by_path(path):
    output = None
    print 'path:', path
    try:
        output = api.content.get(path)
    except Unauthorized:
        pass

    return output


if __name__ == '__main__':
    pattern = 'http://example.net/awstats/awstats.pl?urlfilter={0}&urlfilterex=&output=urldetail&config=www.example.net'
    path = '/news-events/news-usaid-rmp/farming-gender-neutral-q-a-ann-tutwiler'
    path = '/'
    print 'views:', counter(path, pattern)
    print 'hits:', counter(path, pattern, hits=True)
    url = 'http://example.net/awstats/awstats.pl?urlfilterex=&config=www.example.net&framename=mainright&output=urldetail'
    print get_urls(url)