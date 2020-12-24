# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/weargoggles/django-coreapi/django_coreapi/client.py
# Compiled at: 2017-05-15 07:49:40
# Size of source mod 2**32: 2209 bytes
from coreapi import Client
from coreapi.client import _lookup_link
from coreapi.compat import string_types
from coreapi.document import Link
from coreapi.utils import determine_transport
from django_coreapi.transports import DjangoTestHTTPTransport

def _make_absolute(url):
    if not url.startswith('http'):
        url = 'http://testserver/' + url.lstrip('/')
    return url


class DjangoCoreAPIClient(Client):

    def __init__(self, decoders=None, transports=None):
        if not transports:
            transports = [
             DjangoTestHTTPTransport()]
        super(DjangoCoreAPIClient, self).__init__(decoders, transports)

    def get(self, url):
        url = _make_absolute(url)
        link = Link(url, action='get')
        transport = determine_transport(self.transports, link.url)
        return transport.transition(link, decoders=self.decoders)

    def reload(self, document):
        url = _make_absolute(document.url)
        link = Link(url, action='get')
        transport = determine_transport(self.transports, link.url)
        return transport.transition(link, decoders=self.decoders)

    def action(self, document, keys, params=None, action=None, encoding=None, transform=None):
        if isinstance(keys, string_types):
            keys = [
             keys]
        link, link_ancestors = _lookup_link(document, keys)
        url = _make_absolute(link.url)
        if action is not None or encoding is not None or transform is not None:
            action = link.action if action is None else action
            encoding = link.encoding if encoding is None else encoding
            transform = link.transform if transform is None else transform
            link = Link(url, action=action, encoding=encoding, transform=transform, fields=link.fields)
        transport = determine_transport(self.transports, url)
        return transport.transition(link, params, decoders=self.decoders, link_ancestors=link_ancestors)