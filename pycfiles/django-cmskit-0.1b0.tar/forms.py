# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/slideshow/forms.py
# Compiled at: 2012-09-26 05:06:05
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class AdminSlideWidget(AdminFileWidget):

    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, 'url', None):
            image_url = value.url
            file_name = str(value)
            output.append(' <a href="%s" target="_blank"><img src="%s" alt="%s" style="height: 100px;" /></a><br /> %s ' % (
             unicode(image_url), unicode(image_url), unicode(file_name), _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(('').join(output))