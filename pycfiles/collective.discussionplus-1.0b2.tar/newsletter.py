# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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