# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/util.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 554 bytes
from pyramid import security
from pyramid.renderers import get_renderer
from xbus.monitor.i18n import req_l10n

def get_view_params(request, title):
    """Fill parameters used by every view."""
    _ = req_l10n(request)
    login = security.authenticated_userid(request)
    return {'context_url': request.path_qs, 
     'login': login, 
     'macros': get_renderer('xbus.monitor:templates/base.pt').implementation().macros, 
     'project': _('Xbus Monitor'), 
     'view_title': title}