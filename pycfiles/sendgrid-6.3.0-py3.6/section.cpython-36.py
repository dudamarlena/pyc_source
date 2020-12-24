# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/section.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1506 bytes


class Section(object):
    __doc__ = 'A block section of code to be used as a substitution.'

    def __init__(self, key=None, value=None):
        """Create a section with the given key and value.

        :param key: section of code key
        :type key: string
        :param value: section of code value
        :type value: string
        """
        self._key = None
        self._value = None
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value

    @property
    def key(self):
        """A section of code's key.

        :rtype key: string
        """
        return self._key

    @key.setter
    def key(self, value):
        """A section of code's key.

        :param key: section of code key
        :type key: string
        """
        self._key = value

    @property
    def value(self):
        """A section of code's value.

        :rtype: string
        """
        return self._value

    @value.setter
    def value(self, value):
        """A section of code's value.

        :param value: A section of code's value.
        :type value: string
        """
        self._value = value

    def get(self):
        """
        Get a JSON-ready representation of this Section.

        :returns: This Section, ready for use in a request body.
        :rtype: dict
        """
        section = {}
        if self.key is not None:
            if self.value is not None:
                section[self.key] = self.value
        return section