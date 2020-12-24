# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/category.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 992 bytes


class Category(object):
    __doc__ = 'A category name for this message.'

    def __init__(self, name=None):
        """Create a Category.

        :param name: The name of this category
        :type name: string, optional
        """
        self._name = None
        if name is not None:
            self.name = name

    @property
    def name(self):
        """The name of this Category. Must be less than 255 characters.

        :rtype: string
        """
        return self._name

    @name.setter
    def name(self, value):
        """The name of this Category. Must be less than 255 characters.

        :param value: The name of this Category. Must be less than 255
                      characters.
        :type value: string
        """
        self._name = value

    def get(self):
        """
        Get a JSON-ready representation of this Category.

        :returns: This Category, ready for use in a request body.
        :rtype: string
        """
        return self.name