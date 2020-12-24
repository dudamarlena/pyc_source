# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/utm_source.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 1213 bytes


class UtmSource(object):
    __doc__ = 'The utm source of an Ganalytics object.'

    def __init__(self, utm_source=None):
        """Create a UtmSource object

        :param utm_source: Name of the referrer source.
            (e.g. Google, SomeDomain.com, or Marketing Email)
        :type utm_source: string, optional
        """
        self._utm_source = None
        if utm_source is not None:
            self.utm_source = utm_source

    @property
    def utm_source(self):
        """Name of the referrer source. (e.g. Google, SomeDomain.com, or
           Marketing Email)

        :rtype: string
        """
        return self._utm_source

    @utm_source.setter
    def utm_source(self, value):
        """Name of the referrer source. (e.g. Google, SomeDomain.com, or
           Marketing Email)

        :param value: Name of the referrer source.
        (e.g. Google, SomeDomain.com, or Marketing Email)
        :type value: string
        """
        self._utm_source = value

    def get(self):
        """
        Get a JSON-ready representation of this UtmSource.

        :returns: This UtmSource, ready for use in a request body.
        :rtype: string
        """
        return self.utm_source