# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/imsto_client/django/widgets.py
# Compiled at: 2013-05-27 04:53:33
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None):
        output = []
        print ('value: {} type {}').format(value, type(value))
        if value and getattr(value, 'url', None):
            image_url = value.url
            file_name = str(value)
            output.append(' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a> %s ' % (
             image_url, image_url, file_name, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(('').join(output))