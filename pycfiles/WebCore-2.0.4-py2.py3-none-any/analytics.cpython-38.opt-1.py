# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/analytics.py
# Compiled at: 2020-05-11 19:05:21
# Size of source mod 2**32: 1898 bytes
"""Record basic performance statistics."""
from __future__ import unicode_literals
import time
from web.core.compat import unicode
log = __import__('logging').getLogger(__name__)

class AnalyticsExtension(object):
    __doc__ = 'Record performance statistics about each request, and potentially a lot more.\n\t\n\tBy default this extension adds a `X-Generation-Time` header to all responses and logs the generation time at the\n\t`debug` level.  You can disable either by passing `header=None` or `level=None`, or specify an alternate logging\n\tlevel by passing in the name of the level.\n\t'
    __slots__ = ('header', 'log')
    first = True
    provides = ['analytics']

    def __init__(self, header='X-Generation-Time', level='debug'):
        """Executed to configure the extension."""
        super(AnalyticsExtension, self).__init__()
        self.header = header
        self.log = getattr(log, level) if level else None

    def prepare(self, context):
        """Executed during request set-up."""
        context._start_time = None

    def before(self, context):
        """Executed after all extension prepare methods have been called, prior to dispatch."""
        context._start_time = time.time()

    def after(self, context, exc=None):
        """Executed after dispatch has returned and the response populated, prior to anything being sent to the client."""
        duration = time.time() - context._start_time
        delta = unicode(round(duration, 5))
        if self.header:
            context.response.headers[self.header] = delta
        if self.log:
            self.log(('Response generated in ' + delta + ' seconds.'), extra=dict(duration=duration,
              request=(id(context))))