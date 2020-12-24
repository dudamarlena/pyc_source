# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/utm_content.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1102 bytes


class UtmContent(object):
    __doc__ = 'The utm content of an Ganalytics object.'

    def __init__(self, utm_content=None):
        """Create a UtmContent object

        :param utm_content: Used to differentiate your campaign from advertisements.

        :type utm_content: string, optional
        """
        self._utm_content = None
        if utm_content is not None:
            self.utm_content = utm_content

    @property
    def utm_content(self):
        """Used to differentiate your campaign from advertisements.

        :rtype: string
        """
        return self._utm_content

    @utm_content.setter
    def utm_content(self, value):
        """Used to differentiate your campaign from advertisements.

        :param value: Used to differentiate your campaign from advertisements.
        :type value: string
        """
        self._utm_content = value

    def get(self):
        """
        Get a JSON-ready representation of this UtmContent.

        :returns: This UtmContent, ready for use in a request body.
        :rtype: string
        """
        return self.utm_content