# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.hub.client/unicore/hub/client/utils.py
# Compiled at: 2015-05-26 03:45:58
from urlparse import urlparse
PROTOCOL_TO_PORT = {'http': 80, 
   'https': 443}

def client_from_config(client_cls, configuration, prefix='unicorehub.', **kwargs):
    settings = dict((key[len(prefix):], value) for key, value in configuration.iteritems() if key.startswith(prefix))
    settings.update(kwargs)
    if 'app_password' in settings:
        settings['app_key'] = settings['app_password']
        del settings['app_password']
    return client_cls(**settings)


def same_origin(url1, url2):
    """ Return True if the urls have the same origin, else False.
    Copied from Django:
    https://github.com/django/django/blob/master/django/utils/http.py#L255
    """
    p1, p2 = urlparse(url1), urlparse(url2)
    try:
        o1 = (
         p1.scheme, p1.hostname, p1.port or PROTOCOL_TO_PORT[p1.scheme])
        o2 = (p2.scheme, p2.hostname, p2.port or PROTOCOL_TO_PORT[p2.scheme])
        return o1 == o2
    except (ValueError, KeyError):
        return False