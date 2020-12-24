# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/header.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 2640 bytes


class Header(object):
    __doc__ = 'A header to specify specific handling instructions for your email.\n\n    If the name or value contain Unicode characters, they must be properly\n    encoded. You may not overwrite the following reserved headers:\n    x-sg-id, x-sg-eid, received, dkim-signature, Content-Type,\n    Content-Transfer-Encoding, To, From, Subject, Reply-To, CC, BCC\n    '

    def __init__(self, key=None, value=None, p=None):
        """Create a Header.

        :param key: The name of the header (e.g. "Date")
        :type key: string, optional
        :param value: The header's value (e.g. "2013-02-27 1:23:45 PM PDT")
        :type value: string, optional
        :param name: p is the Personalization object or Personalization object
                     index
        :type name: Personalization, integer, optional
        """
        self._key = None
        self._value = None
        self._personalization = None
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value
        if p is not None:
            self.personalization = p

    @property
    def key(self):
        """The name of the header.

        :rtype: string
        """
        return self._key

    @key.setter
    def key(self, value):
        """The name of the header.

        :param value: The name of the header.
        :type value: string
        """
        self._key = value

    @property
    def value(self):
        """The value of the header.

        :rtype: string
        """
        return self._value

    @value.setter
    def value(self, value):
        """The value of the header.

        :param value: The value of the header.
        :type value: string
        """
        self._value = value

    @property
    def personalization(self):
        """The Personalization object or Personalization object index

        :rtype: Personalization, integer
        """
        return self._personalization

    @personalization.setter
    def personalization(self, value):
        """The Personalization object or Personalization object index

        :param value: The Personalization object or Personalization object
                      index
        :type value: Personalization, integer
        """
        self._personalization = value

    def get(self):
        """
        Get a JSON-ready representation of this Header.

        :returns: This Header, ready for use in a request body.
        :rtype: dict
        """
        header = {}
        if self.key is not None:
            if self.value is not None:
                header[self.key] = self.value
        return header