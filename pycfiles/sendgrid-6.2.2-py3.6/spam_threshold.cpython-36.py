# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/spam_threshold.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1879 bytes


class SpamThreshold(object):
    __doc__ = 'The threshold used to determine if your content qualifies as spam\n       on a scale from 1 to 10, with 10 being most strict, or most likely\n       to be considered as spam.'

    def __init__(self, spam_threshold=None):
        """Create a SpamThreshold object

        :param spam_threshold: The threshold used to determine if your content
                               qualifies as spam on a scale from 1 to 10, with
                               10 being most strict, or most likely to be
                               considered as spam.
        :type spam_threshold: integer, optional
        """
        self._spam_threshold = None
        if spam_threshold is not None:
            self.spam_threshold = spam_threshold

    @property
    def spam_threshold(self):
        """The threshold used to determine if your content
           qualifies as spam on a scale from 1 to 10, with
           10 being most strict, or most likely to be
           considered as spam.

        :rtype: integer
        """
        return self._spam_threshold

    @spam_threshold.setter
    def spam_threshold(self, value):
        """The threshold used to determine if your content
           qualifies as spam on a scale from 1 to 10, with
           10 being most strict, or most likely to be
           considered as spam.

        :param value: The threshold used to determine if your content
        qualifies as spam on a scale from 1 to 10, with
        10 being most strict, or most likely to be
        considered as spam.
        :type value: integer
        """
        self._spam_threshold = value

    def get(self):
        """
        Get a JSON-ready representation of this SpamThreshold.

        :returns: This SpamThreshold, ready for use in a request body.
        :rtype: integer
        """
        return self.spam_threshold