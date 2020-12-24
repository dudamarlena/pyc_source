# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyOpenBSD/_mirrors.py
# Compiled at: 2016-11-20 08:29:35
from enum import Enum
from urlparse import urlparse
import _ftp_html
_non_pingable = [
 'mirrors.unb.br',
 'ftp.openbsd.org',
 'openbsd.delfic.org',
 'mirrors.ucr.ac.cr',
 'ftp.aso.ee',
 'ftp.cc.uoc.gr',
 'www.ftp.ne.jp',
 'mirror.jmu.edu',
 'ftp.kddilabs.jp']
Protocol = Enum('any', 'http', 'ftp', 'rsync')

class Mirror(object):

    def __init__(self, url):
        self.url = url
        self.protocol = self._get_protocol(url)
        self.hostname = self._get_hostname(url)
        self.is_pingable = self._is_pingable(self.hostname)

    def _get_protocol(self, url):
        protocol = url.split(':')[0]
        return Protocol.__dict__[protocol]

    def _get_hostname(self, url):
        uri = urlparse(url)
        return uri.hostname

    def _is_pingable(self, hostname):
        return hostname not in _non_pingable

    def __str__(self):
        return self.url

    def pkg_repo(self, osversion, arch):
        sep = '' if self.url.endswith('/') else '/'
        format_url = '%(base_url)s%(sep)s%(osversion)s/packages/%(arch)s'
        repo = format_url % {'base_url': self.url, 'sep': sep, 
           'osversion': osversion, 
           'arch': arch}
        return repo


def _load_mirrors():
    result = {Protocol.any: [], Protocol.http: [], Protocol.ftp: [], Protocol.rsync: []}
    mirror_list = _ftp_html.raw.strip().split('\n')
    for url in mirror_list:
        mirror = Mirror(url.strip())
        result[Protocol.any].append(mirror)
        result[mirror.protocol].append(mirror)

    return {k:tuple(v) for k, v in result.iteritems()}


mirrors = _load_mirrors()