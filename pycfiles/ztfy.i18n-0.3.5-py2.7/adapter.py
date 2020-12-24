# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/adapter.py
# Compiled at: 2012-06-20 11:46:34
from ztfy.i18n.interfaces import II18nManagerInfo
from z3c.form import form, field, button
from zope.traversing.browser import absoluteURL
from ztfy.i18n import _

class I18nManagerEditForm(form.EditForm):
    """Edit form for I18nManagerInfo properties"""
    form.extends(form.EditForm)
    fields = field.Fields(II18nManagerInfo)

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        self.request.response.redirect('%s/@@manageLanguages.html' % absoluteURL(self.context, self.request))