# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/errors.py
# Compiled at: 2018-04-24 04:48:32
__doc__ = '\nCreated on Dec 9, 2013\n\n@author: nyga\n'

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