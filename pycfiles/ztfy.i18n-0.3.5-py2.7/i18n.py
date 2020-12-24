# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/i18n.py
# Compiled at: 2012-06-20 11:46:34
__docformat__ = 'restructuredtext'
from z3c.language.session.interfaces import ILanguageSession
from zope.publisher.browser import BrowserView
from zope.traversing.browser import absoluteURL

class I18nLanguageView(BrowserView):

    def setLanguage(self):
        lang = self.request.form.get('language')
        if lang:
            ILanguageSession(self.request).setLanguage(lang)
        self.request.response.redirect(absoluteURL(self.context, self.request))