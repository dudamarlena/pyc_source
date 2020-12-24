# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/exc.py
# Compiled at: 2019-08-24 21:09:08
# Size of source mod 2**32: 666 bytes
__doc__ = 'Configuration related exceptions.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

class MissingRequiredOption(ValueError):
    """MissingRequiredOption"""
    pass


class NamespaceNotRegistered(AttributeError):
    """NamespaceNotRegistered"""
    pass


class OptionNotRegistered(AttributeError):
    """OptionNotRegistered"""
    pass


class UnrecognizedFileExtension(ValueError):
    """UnrecognizedFileExtension"""
    pass