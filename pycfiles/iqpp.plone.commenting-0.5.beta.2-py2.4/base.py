# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/viewlets/base.py
# Compiled at: 2007-10-06 06:19:54
from iqpp.plone.commenting.interfaces import ICommentingOptions

class CommentingViewletsBase(object):
    """
    """
    __module__ = __name__

    @property
    def available(self):
        """
        """
        co = ICommentingOptions(self.context)
        if co.getEffectiveOption('is_enabled') == False:
            return False
        return True