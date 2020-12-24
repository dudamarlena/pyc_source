# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yhoorneman/Git/opsgenielib/opsgenielib/opsgenielibexceptions.py
# Compiled at: 2019-11-22 14:25:58
# Size of source mod 2**32: 1803 bytes
"""
Custom exception code for opsgenielib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Yorick Hoorneman <yhoorneman@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '12-04-2019'
__copyright__ = 'Copyright 2019, Yorick Hoorneman'
__credits__ = ['Yorick Hoorneman']
__license__ = 'MIT'
__maintainer__ = 'Yorick Hoorneman'
__email__ = '<yhoorneman@schubergphilis.com>'
__status__ = 'Development'

class InvalidApiKey(Exception):
    __doc__ = 'The api key provided is not valid.'