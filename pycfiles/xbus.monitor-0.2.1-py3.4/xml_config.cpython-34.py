# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/xml_config.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 331 bytes
from pyramid.view import view_config
from xbus.monitor.i18n import req_l10n
from .util import get_view_params

@view_config(route_name='xml_config_ui', renderer='xbus.monitor:templates/xml_config.pt')
def xml_config_view(request):
    _ = req_l10n(request)
    return get_view_params(request, _('XML configuration'))