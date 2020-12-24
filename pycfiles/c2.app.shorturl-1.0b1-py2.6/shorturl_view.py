# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/browser/shorturl_view.py
# Compiled at: 2010-08-19 05:10:29
"""
shorturl_view.py

Created by Manabu Terada on 2010-08-03.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from Products.Five.browser import BrowserView

class ShortUrlView(BrowserView):

    def __call__(self, *args, **kw):
        context = self.context
        request = self.request
        response = request.response
        response.redirect(context.get_org_url())
        return