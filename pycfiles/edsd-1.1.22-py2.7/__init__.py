# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/edsd/__init__.py
# Compiled at: 2017-03-07 02:12:08
__author__ = 'Thomas Li <yanliang.lyl@alibaba-inc.com>'
__license__ = 'GNU License'
__version__ = '1.1.22'
DEBUG = False

def default_colored(text, *args, **kwargs):
    """a default colored function used for print raw text without any color.
    """
    return text


try:
    from termcolor import colored
except:
    colored = default_colored