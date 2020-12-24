# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/uniconnect/redirect.py
# Compiled at: 2019-08-27 00:56:48
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
from six import with_metaclass
import ipaddress, socket
from typing import Any, Text
from six.moves.urllib_parse import urlparse

class RedirectHandler(with_metaclass(abc.ABCMeta)):

    @abc.abstractmethod
    def handle(self, url):
        pass


def _normalize_url_with_hostname(url):
    parsed = urlparse(url.encode('utf-8'))
    hostname = parsed.hostname.decode('utf-8')
    try:
        ipaddress.ip_address(hostname)
        hostname = socket.gethostbyaddr(hostname)[0].encode('utf-8')
    except ValueError:
        return url

    return parsed._replace(netloc='%s:%d' % (hostname, parsed.port)).geturl()


class GatewayRedirectHandler(RedirectHandler):

    def handle(self, url):
        if url is None:
            return
        else:
            return _normalize_url_with_hostname(url)