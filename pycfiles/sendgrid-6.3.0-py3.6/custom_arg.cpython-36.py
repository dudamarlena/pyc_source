# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/custom_arg.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 2682 bytes


class CustomArg(object):
    __doc__ = 'Values that will be carried along with the email and its activity data.\n\n    Substitutions will not be made on custom arguments, so any string entered\n    into this parameter will be assumed to be the custom argument that you\n    would like to be used. Top-level CustomArgs may be overridden by ones in a\n    Personalization. May not exceed 10,000 bytes.\n    '

    def __init__(self, key=None, value=None, p=None):
        """Create a CustomArg with the given key and value.

            :param key: Key for this CustomArg
            :type key: string, optional
            :param value: Value of this CustomArg
            :type value: string, optional
            :param p: p is the Personalization object or Personalization
                      object index
            :type p: Personalization, integer, optional
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
        """Key for this CustomArg.

        :rtype: string
        """
        return self._key

    @key.setter
    def key(self, value):
        """Key for this CustomArg.

        :param value: Key for this CustomArg.
        :type value: string
        """
        self._key = value

    @property
    def value(self):
        """Value of this CustomArg.

        :rtype: string
        """
        return self._value

    @value.setter
    def value(self, value):
        """Value of this CustomArg.

        :param value: Value of this CustomArg.
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
        Get a JSON-ready representation of this CustomArg.

        :returns: This CustomArg, ready for use in a request body.
        :rtype: dict
        """
        custom_arg = {}
        if self.key is not None:
            if self.value is not None:
                custom_arg[self.key] = self.value
        return custom_arg