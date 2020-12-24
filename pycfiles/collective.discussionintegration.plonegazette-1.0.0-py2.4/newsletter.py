# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/discussionintegration/plonegazette/newsletter.py
# Compiled at: 2010-01-27 11:14:10


class NewsletterConversation(object):
    """
    """
    __module__ = __name__

    def __init__(self, context):
        self.context = context
        self.total_comments = 0

    def enabled(self):
        return False