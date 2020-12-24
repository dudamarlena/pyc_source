# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/browser/shorturl_view.py
# Compiled at: 2010-08-19 05:10:29
__doc__ = '\nshorturl_view.py\n\nCreated by Manabu Terada on 2010-08-03.\nCopyright (c) 2010 CMScom. All rights reserved.\n'
from Products.Five.browser import BrowserView

class ShortUrlView(BrowserView):

    def __call__(self, *args, **kw):
        context = self.context
        request = self.request
        response = request.response
        response.redirect(context.get_org_url())
        return