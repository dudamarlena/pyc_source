# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/formalworkflow/browser/info.py
# Compiled at: 2013-06-23 13:03:58
from plone.app.iterate.browser.info import BaselineInfoViewlet
from AccessControl import getSecurityManager

class BaselineInfoViewlet(BaselineInfoViewlet):
    """ Added to alter security declaration to allow editors
        to see info viewlet """

    def render(self):
        if self.working_copy() is not None and getSecurityManager().checkPermission('Copy or Move', self.context):
            return self.index()
        else:
            return ''
            return