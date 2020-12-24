# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/captcha/browser/captchaview.py
# Compiled at: 2008-12-22 08:21:43
"""Image checker view  for the Zope 3 imageechecker package

$Id: captchaview.py 35230 2007-11-28 11:21:54Z anton $
"""
__author__ = 'Egor Shershenev'
__license__ = 'ZPL'
__version__ = '$Revision: 35230 $'
__date__ = '$Date: 2007-11-28 13:21:54 +0200 (Wed, 28 Nov 2007) $'
from zope.publisher.browser import BrowserView
from zope.component import getUtility
from ks.captcha.interfaces import ICaptcha

class CaptchaView(BrowserView):
    __module__ = __name__

    def banner(self):
        ic = getUtility(ICaptcha, context=self.context)
        self.request.response.setHeader('Content-Type', 'image/jpeg')
        return ic.banner(self.request.get('key'))