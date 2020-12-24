# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/utils/web.py
# Compiled at: 2016-10-03 09:39:22
import gtk, re, logging
logger = logging.getLogger(__name__)
import bauble.utils.desktop as desktop
from bauble.i18n import _

def _open_link(func, data=None):
    desktop.open(data)


gtk.link_button_set_uri_hook(_open_link)

class BaubleLinkButton(gtk.LinkButton):
    _base_uri = '%s'
    _space = '_'
    title = _('Search')
    tooltip = None
    pt = re.compile('%\\(([a-z_\\.]*)\\)s')

    def __init__(self, title=_('Search'), tooltip=None):
        super(BaubleLinkButton, self).__init__('', self.title)
        self.set_tooltip_text(self.tooltip or self.title)
        self.__class__.fields = self.pt.findall(self._base_uri)

    def set_string(self, row):
        if self.fields == []:
            s = str(row)
            self.set_uri(self._base_uri % s.replace(' ', self._space))
        else:
            values = {}
            for key in self.fields:
                value = row
                for step in key.split('.'):
                    value = getattr(value, step, '-')

                values[key] = value == str(value) and value or ''

            self.set_uri(self._base_uri % values)