# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/mapscookiegettercli/mapscookiegettercli/mapscookiegettercliexceptions.py
# Compiled at: 2019-06-16 09:01:32
# Size of source mod 2**32: 1920 bytes
"""
Custom exception code for mapscookiegettercli

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '04-03-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'

class UnsupportedOS(Exception):
    __doc__ = 'The os identified is not a supported one.'


class UnsupportedDefaultBrowser(Exception):
    __doc__ = 'The browser could not be identified or is not supported.'