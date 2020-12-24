# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivan/pycharm-workplace/test_ftp/pureftpd_admin/localdir/widgets.py
# Compiled at: 2013-08-23 05:29:04
__author__ = 'ivan'
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms
import os, re
popup_init_script = '\n<br>\n<a href="#" onclick="popupWin = window.open(django.jQuery(\'#%(target_id)s\').attr(\'popup_url\')+\'?pop=1&id=%(target_id)s\', \'Localdir popup\', \'location,width=400,height=800,top=100,left=500\'); popupWin.focus();">\n    %(select_text)s\n</a>\n'

class LocalDirAdminWidget(forms.Textarea):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        try:
            popup_url = str(self.attrs['popup_url'])
        except KeyError:
            raise TypeError("You need set widget's attr 'popup_url' for LocalDirAdminWidget")

        document_root = self.attrs.pop('document_root', '')
        if value.startswith(document_root):
            popup_url = os.path.normpath(('/').join([popup_url, re.sub(document_root + '/?', '', value, count=1)])) + '/'
            print popup_url
            self.attrs['popup_url'] = popup_url
        content = super(LocalDirAdminWidget, self).render(name, value, attrs)
        content += mark_safe(popup_init_script % {'target_id': attrs['id'], 
           'select_text': unicode(_('Chose from local dir')), 
           'popup_url': popup_url})
        return content