# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/terraformtestinglib/terraformtestinglib/utils/utils.py
# Compiled at: 2018-10-12 06:20:41
"""
Main code for utils

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-24'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'

class RecursiveDictionary(dict):
    """Implements recursively updating dictionary

    RecursiveDictionary provides the methods update and iter_rec_update
    that can be used to update member dictionaries rather than overwriting
    them.
    """

    def update(self, other, **third):
        """Implements the recursion

        Recursively update the dictionary with the contents of other and
        third like dict.update() does - but don't overwrite sub-dictionaries.
        """
        try:
            iterator = other.iteritems()
        except AttributeError:
            iterator = other

        self.iter_rec_update(iterator)
        self.iter_rec_update(third.iteritems())

    def iter_rec_update(self, iterator):
        """Updates recursively"""
        for key, value in iterator:
            if key in self and isinstance(self[key], dict) and isinstance(value, dict):
                self[key] = RecursiveDictionary(self[key])
                self[key].update(value)
            else:
                self[key] = value