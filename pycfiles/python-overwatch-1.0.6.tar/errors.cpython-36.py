# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alexbotello/Code/python-overwatch/overwatch/errors.py
# Compiled at: 2018-02-25 19:48:26
# Size of source mod 2**32: 592 bytes


class InvalidFilter(Exception):
    __doc__ = "\n    Raise when 'filter' key word argument is not recognized\n    "


class InvalidHero(Exception):
    __doc__ = "\n    Raise when 'hero' key word argument is not recognized\n    "


class InvalidCombination(Exception):
    __doc__ = "\n    Raise when 'filter' and 'hero' key word arguments\n    are an invalid combination.\n    "


class InvalidBattletag(Exception):
    __doc__ = "\n    Raise when 'battletag' key word argument is none \n    "


class NotFound(Exception):
    __doc__ = '\n    Raise when stats could not be found\n    '