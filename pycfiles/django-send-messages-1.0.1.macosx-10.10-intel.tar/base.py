# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/esperyong/develop/pyprojects/hwbuluo_src/hwbuluo-site/venv/lib/python2.7/site-packages/sms/backends/base.py
# Compiled at: 2015-05-10 23:04:16
"""Base sms backend class."""

class BaseSMSBackend(object):
    """
    Base class for sms backend implementations.

    Subclasses must at least overwrite send_messages().
    """

    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently

    def open(self):
        """Open a network connection.

        This method can be overwritten by backend implementations to
        open a network connection.

        It's up to the backend implementation to track the status of
        a network connection if it's needed by the backend.

        This method can be called by applications to force a single
        network connection to be used when sending mails. See the
        send_messages() method of the SMTP backend for a reference
        implementation.

        The default implementation does nothing.
        """
        pass

    def close(self):
        """Close a network connection."""
        pass

    def send_messages(self, sms_messages):
        """
        Sends one or more SMSMessage objects and returns the number of sms
        messages sent.
        """
        raise NotImplementedError