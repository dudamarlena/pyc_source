# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/batch_id.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1316 bytes


class BatchId(object):
    __doc__ = 'This ID represents a batch of emails to be sent at the same time.\n       Including a batch_id in your request allows you include this email\n       in that batch, and also enables you to cancel or pause the delivery\n       of that batch. For more information, see\n       https://sendgrid.com/docs/API_Reference/Web_API_v3/cancel_schedule_send.\n    '

    def __init__(self, batch_id=None):
        """Create a batch ID.

        :param batch_id: Batch Id
        :type batch_id: string
        """
        self._batch_id = None
        if batch_id is not None:
            self.batch_id = batch_id

    @property
    def batch_id(self):
        """A unix timestamp.

        :rtype: string
        """
        return self._batch_id

    @batch_id.setter
    def batch_id(self, value):
        """A unix timestamp.

        :param value: Batch Id
        :type value: string
        """
        self._batch_id = value

    def __str__(self):
        """Get a JSON representation of this object.

        :rtype: string
        """
        return str(self.get())

    def get(self):
        """
        Get a JSON-ready representation of this SendAt object.

        :returns: The BatchId, ready for use in a request body.
        :rtype: string
        """
        return self.batch_id