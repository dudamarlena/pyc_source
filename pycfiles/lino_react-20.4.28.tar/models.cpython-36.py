# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luc/work/react/lino_react/react/models.py
# Compiled at: 2018-11-22 17:23:05
# Size of source mod 2**32: 951 bytes
"""
Database models for `lino.modlib.bootstrap3`.

.. autosummary::

"""
from django.conf import settings
from lino.core.tables import AbstractTable
from django.utils.translation import ugettext_lazy as _
from lino.api import dd

class ShowAsHtml(dd.Action):
    label = _('HTML')
    help_text = _('Show this table in Bootstrap3 interface')
    icon_name = 'html'
    ui5_icon_name = 'sap-icon://attachment-html'
    sort_index = -15
    select_rows = False
    default_format = 'ajax'
    preprocessor = 'Lino.get_current_grid_config'
    callable_from = 't'

    def is_callable_from(self, caller):
        return isinstance(caller, dd.ShowTable)

    def run_from_ui(self, ar, **kw):
        url = dd.plugins.bootstrap3.renderer.get_request_url(ar)
        ar.success(open_url=url)


if settings.SITE.default_ui != 'lino.modlib.bootstrap3':
    AbstractTable.show_as_html = ShowAsHtml()