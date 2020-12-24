# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/aitjcize/Work/creepy/creepy/crawler.py
# Compiled at: 2016-04-24 02:58:44
from __future__ import print_function
import os, re, sys
from threading import Thread, Lock
if sys.version_info < (3, 0):
    import httplib
    from urllib import quote
else:
    import http.client as httlib
    from urllib.parse import quote

class Document(object):

    def __init__(self, res, url):
        self.url = url
        self.query = '' if '?' not in url else url.split('?')[(-1)]
        self.status = res.status
        self.text = res.read()
        self.headers = dict(res.getheaders())
        if sys.version_info >= (3, 0):
            self.text = self.text.decode()


class Crawler(object):
    F_ANY, F_SAME_DOMAIN, F_SAME_HOST, F_SAME_PATH = list(range(4))

    def __init__(self):
        self.host = None
        self.visited = {}
        self.targets = set()
        self.threads = []
        self.concurrency = 0
        self.max_outstanding = 16
        self.max_depth = 0
        self.include_hashtag = False
        self.follow_mode = self.F_SAME_HOST
        self.content_type_filter = '(text/html)'
        self.url_filters = []
        self.prefix_filter = '^(#|javascript:|mailto:)'
        self.targets_lock = Lock()
        self.concurrency_lock = Lock()
        return

    def set_content_type_filter(self, cf):
        self.content_type_filter = '(%s)' % ('|').join(cf)

    def add_url_filter(self, uf):
        self.url_filters.append(uf)

    def set_follow_mode(self, mode):
        if mode > 5:
            raise RuntimeError('invalid follow mode.')
        self.follow_mode = mode

    def set_concurrency_level(self, level):
        self.max_outstanding = level

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth

    def set_include_hashtag(self, include):
        self.include_hashtag = include

    def process_document(self, doc):
        print('GET', doc.status, doc.url)

    def crawl(self, url, path=None):
        self.root_url = url
        rx = re.match('(https?://)([^/]+)([^\\?]*)(\\?.*)?', url)
        self.proto = rx.group(1)
        self.host = rx.group(2)
        self.path = rx.group(3)
        self.dir_path = os.path.dirname(self.path)
        self.query = rx.group(4)
        if path:
            self.dir_path = path
        self.targets.add(url)
        self._spawn_new_worker()
        while self.threads:
            try:
                for t in self.threads:
                    t.join(1)
                    if not t.isAlive():
                        self.threads.remove(t)

            except KeyboardInterrupt:
                sys.exit(1)

    def _url_domain(self, host):
        parts = host.split('.')
        if len(parts) <= 2:
            return host
        else:
            if re.match('^[0-9]+(?:\\.[0-9]+){3}$', host):
                return host
            return ('.').join(parts[1:])

    def _follow_link(self, url, link):
        if re.search(self.prefix_filter, link):
            return
        else:
            for f in self.url_filters:
                if re.search(f, link):
                    return

            if not self.include_hashtag:
                link = re.sub('(%23|#).*$', '', link)
            rx = re.match('(https?://)([^/:]+)(:[0-9]+)?([^\\?]*)(\\?.*)?', url)
            url_proto = rx.group(1)
            url_host = rx.group(2)
            url_port = rx.group(3) if rx.group(3) else ''
            url_path = rx.group(4) if len(rx.group(4)) > 0 else '/'
            url_dir_path = os.path.dirname(url_path)
            rx = re.match('((https?://)([^/:]+)(:[0-9]+)?)?([^\\?]*)(\\?.*)?', link)
            link_full_url = rx.group(1) is not None
            link_proto = rx.group(2) if rx.group(2) else url_proto
            link_host = rx.group(3) if rx.group(3) else url_host
            link_port = rx.group(4) if rx.group(4) else url_port
            link_path = quote(rx.group(5), '/%') if rx.group(5) else url_path
            link_query = quote(rx.group(6), '?=&%') if rx.group(6) else ''
            link_dir_path = os.path.dirname(link_path)
            if not link_full_url and not link.startswith('/'):
                link_path = os.path.normpath(os.path.join(url_dir_path, link_path))
            link_url = link_proto + link_host + link_port + link_path + link_query
            if self.follow_mode == self.F_ANY:
                return link_url
            if self.follow_mode == self.F_SAME_DOMAIN:
                if self._url_domain(self.host) == self._url_domain(link_host):
                    return link_url
                return
            if self.follow_mode == self.F_SAME_HOST:
                if self.host == link_host:
                    return link_url
                return
            if self.follow_mode == self.F_SAME_PATH:
                if self.host == link_host and link_dir_path.startswith(self.dir_path):
                    return link_url
                else:
                    return

            return

    def _calc_depth(self, url):
        return len(url.replace('https', 'http').replace(self.root_url, '').rstrip('/').split('/')) - 1

    def _add_target(self, target):
        if not target:
            return
        if self.max_depth and self._calc_depth(target) > self.max_depth:
            return
        with self.targets_lock:
            if target in self.visited:
                return
            self.targets.add(target)

    def _spawn_new_worker(self):
        with self.concurrency_lock:
            self.concurrency += 1
            t = Thread(target=self._worker, args=(self.concurrency,))
            t.daemon = True
            self.threads.append(t)
            t.start()

    def _worker(self, sid):
        while self.targets:
            try:
                with self.targets_lock:
                    url = self.targets.pop()
                    self.visited[url] = True
                rx = re.match('(https?)://([^/]+)(.*)', url)
                protocol = rx.group(1)
                host = rx.group(2)
                path = rx.group(3)
                if protocol == 'http':
                    conn = httplib.HTTPConnection(host, timeout=10)
                else:
                    conn = httplib.HTTPSConnection(host, timeout=10)
                conn.request('GET', path)
                res = conn.getresponse()
                if res.status == 404:
                    continue
                if res.status == 301 or res.status == 302:
                    rlink = self._follow_link(url, res.getheader('location'))
                    self._add_target(rlink)
                    continue
                try:
                    if not re.search(self.content_type_filter, res.getheader('Content-Type')):
                        continue
                except TypeError:
                    continue

                doc = Document(res, url)
                self.process_document(doc)
                links = re.findall('href\\s*=\\s*[\'"]\\s*([^\'"]+)[\'"]', doc.text, re.S)
                links = list(set(links))
                for link in links:
                    rlink = self._follow_link(url, link.strip())
                    self._add_target(rlink)

                if self.concurrency < self.max_outstanding:
                    self._spawn_new_worker()
            except KeyError:
                break
            except (httplib.HTTPException, EnvironmentError):
                with self.targets_lock:
                    self.targets.add(url)

        with self.concurrency_lock:
            self.concurrency -= 1