# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/patches/publisher.py
# Compiled at: 2018-04-03 08:39:39
import logging, inspect, json
from datetime import datetime
from zope.contenttype import guess_content_type
from zope.publisher.browser import BrowserView
from Products.PageTemplates.PageTemplate import PageTemplate
from edw.logger.util import get_request_data
from edw.logger.config import logger
from edw.logger.config import LOG_PUBLISHER
IGNORED_CTS = ('text/css', 'image/', 'javascript', 'font')
IGNORED_URLS = ('health.check', 'varnish_probe')
KNOWN_METHODS = ('GET', 'POST')

def skip_contenttype(content_type):
    return any(tuple(ct in content_type for ct in IGNORED_CTS))


def skip_url(url):
    return any(tuple(url.endswith(u) for u in IGNORED_URLS))


URL_VALIDATORS = (
 lambda url: skip_contenttype(guess_content_type(url)[0]),
 skip_url)

def traverse_wrapper(meth):
    """Extract some basic info about the object and view. traverse method
    gives us access to the traversed object"""

    def extract(self, *args, **kwargs):
        try:
            obj = meth(self, *args, **kwargs)
            try:
                if self.method not in KNOWN_METHODS:
                    return obj
                else:
                    request_data = get_request_data(self)
                    kv = {'User': request_data['user'], 
                       'IP': request_data['ip'], 
                       'URL': self.URL, 
                       'ACTUAL_URL': self.ACTUAL_URL, 
                       'Partition': request_data['user_type'], 
                       'Type': 'Traverse', 
                       'Date': datetime.now().isoformat(), 
                       'LoggerName': logger.name}
                    if isinstance(obj, PageTemplate):
                        kv['Action'] = obj.getId()
                        kv['Template'] = obj.pt_source_file()
                        parent = obj.getParentNode()
                        kv['Controller'] = parent.meta_type
                        kv['Object'] = parent.absolute_url()
                    else:
                        if isinstance(obj, BrowserView):
                            kv['Action'] = obj.__name__
                            if hasattr(obj.context, 'meta_type'):
                                kv['Controller'] = obj.context.meta_type
                            kv['Object'] = obj.context.absolute_url()
                        elif inspect.ismethod(obj):
                            content_type = getattr(obj.im_self, 'content_type', '')
                            if skip_contenttype(content_type):
                                return obj
                            if hasattr(obj.im_self, 'meta_type'):
                                kv['Controller'] = obj.im_self.meta_type
                        else:
                            kv['Controller'] = obj.aq_parent.meta_type
                        if 'Controller' not in kv:
                            return obj
                    if not any(tuple(v(self.URL) for v in URL_VALIDATORS)):
                        logger.info(json.dumps(kv))
                    return obj

            except:
                return obj

        except:
            raise

    return extract


if LOG_PUBLISHER:
    from ZPublisher.BaseRequest import BaseRequest
    BaseRequest.orig_traverse = BaseRequest.traverse
    BaseRequest.traverse = traverse_wrapper(BaseRequest.orig_traverse)