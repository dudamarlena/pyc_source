# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/code/pracmln/python3/pracmln/mln/errors.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 341 bytes
"""
Created on Dec 9, 2013

@author: nyga
"""

class MLNParsingError(Exception):
    pass


class NoSuchPredicateError(Exception):
    pass


class NoSuchDomainError(Exception):
    pass


class MRFValueException(Exception):
    pass


class SatisfiabilityException(Exception):
    pass


class OutOfMemoryError(Exception):
    pass


class NoConstraintsError(Exception):
    pass