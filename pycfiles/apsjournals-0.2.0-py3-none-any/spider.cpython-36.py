# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\apsitemap\spider.py
# Compiled at: 2017-10-12 21:55:38
# Size of source mod 2**32: 2640 bytes
from concurrent import futures
from .utility import standardize_url, sitemap_log
from .urlset import UrlSet
import requests, pyquery

def _visit_url(url):
    """visit url and get response or origin url"""
    try:
        return requests.get(url)
    except requests.exceptions.RequestException:
        return url


def _concurrent_download_with_futures(urls):
    """concurrent visit urls with futures"""
    with futures.ThreadPoolExecutor(max_workers=(min(20, len(urls)))) as (executor):
        return executor.map(_visit_url, urls)


class Spider(object):

    def __init__(self, entry: str, urlset: UrlSet):
        self._Spider__entry = standardize_url(entry)
        self._Spider__urlset = urlset
        self._Spider__dead_links = []
        sitemap_log.debug('Initialize spider....')

    def start(self):
        urls = [
         self._Spider__entry]
        sitemap_log.debug('Start spider...')
        while 1:
            responses = _concurrent_download_with_futures(urls)
            crawled_urls = []
            new_add = 0
            for resp in responses:
                if isinstance(resp, requests.Response):
                    if resp.status_code == 200:
                        new_add += 1
                        self._Spider__urlset.add([resp.request.url])
                        try:
                            text = resp.text.encode('ISO-8859-1').decode('utf-8')
                        except (UnicodeEncodeError, UnicodeDecodeError):
                            text = resp.text

                        pq = pyquery.PyQuery(text)
                        links = pq.find('a')
                        for index in range(links.length):
                            link = links.eq(index)
                            crawled_urls.append(link.attr('href'))

                    else:
                        self._Spider__dead_links.append(resp.request.url)
                else:
                    self._Spider__dead_links.append(resp)

            urls = self._Spider__urlset.fix_urls(list(set(crawled_urls)))
            urls = list(filter(lambda url: url not in self._Spider__dead_links and url not in self._Spider__urlset, urls))
            sitemap_log.info('correct urls: %s, new add: %s', new_add, len(urls))
            if len(urls) == 0:
                break

        sitemap_log.info('Spider have crawled %s urls', len(self._Spider__urlset))


if __name__ == '__main__':
    urlset = UrlSet(entry='http://blog.fudenglong.site/')
    spider = Spider(entry='http://blog.fudenglong.site/', urlset=urlset)
    spider.start()
    urlset.save_xml()