# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/django-smart-proxy/lib/python3.3/site-packages/smart_proxy/decorators.py
# Compiled at: 2014-11-26 21:04:56
# Size of source mod 2**32: 604 bytes
import re
from django.core.urlresolvers import reverse
REWRITE_REGEX = re.compile('((?:src|action|href)=["\\\'])/')

def rewrite_response(fn):
    """
    Rewrites the response to fix references to resources loaded from HTML
    files (images, etc.).
    """

    def decorate(request, *args, **kwargs):
        response = fn(request, *args, **kwargs)
        proxy_root = reverse('smart_proxy.views.proxy', kwargs={'url': ''})
        response.content = REWRITE_REGEX.sub('\\1%s' % proxy_root, response.content)
        return response

    return decorate