# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/subscribers/i18n.py
# Compiled at: 2014-05-04 12:45:31
"""i18n subscribers."""
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid_localize.tools import set_localizer

@subscriber(BeforeRender)
def global_renderer(event):
    """BeforeRender subscriber, adds localizer, and translation methods to context."""
    request = event['request']
    set_localizer(request)
    event['_'] = request._
    event['localizer'] = request.localizer


@subscriber(NewRequest)
def add_localizer(event):
    """NewRequest subscriber, adds localizer and translation methods to request."""
    set_localizer(event.request)