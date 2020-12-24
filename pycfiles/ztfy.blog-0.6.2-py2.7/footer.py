# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/defaultskin/viewlets/footer/footer.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from datetime import datetime
from ztfy.blog.browser.viewlets import BaseViewlet

class FooterViewlet(BaseViewlet):
    """Footer viewlet"""

    @property
    def year(self):
        return datetime.now().year