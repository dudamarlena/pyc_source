# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/utm_term.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 964 bytes


class UtmTerm(object):
    __doc__ = 'The utm term of an Ganalytics object.'

    def __init__(self, utm_term=None):
        """Create a UtmTerm object

        :param utm_term: Used to identify any paid keywords.

        :type utm_term: string, optional
        """
        self._utm_term = None
        if utm_term is not None:
            self.utm_term = utm_term

    @property
    def utm_term(self):
        """Used to identify any paid keywords.

        :rtype: string
        """
        return self._utm_term

    @utm_term.setter
    def utm_term(self, value):
        """Used to identify any paid keywords.

        :param value: Used to identify any paid keywords.
        :type value: string
        """
        self._utm_term = value

    def get(self):
        """
        Get a JSON-ready representation of this UtmTerm.

        :returns: This UtmTerm, ready for use in a request body.
        :rtype: string
        """
        return self.utm_term