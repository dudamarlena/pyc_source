# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/what/plugins/pylonshq/utils.py
# Compiled at: 2009-03-16 13:28:54
"""
Miscellaneous utilities for :mod:`repoze.what` when used in a Pylons
application.

"""
from pylons import request
from repoze.what.predicates import Predicate
__all__ = [
 'is_met', 'not_met', 'booleanize_predicates',
 'debooleanize_predicates']

def is_met(predicate):
    """
    Evaluate the :mod:`repoze.what` ``predicate`` checker and return ``True``
    if it's met.
    
    :param predicate: The :mod:`repoze.what` predicate checker to be evaluated.
    :return: ``True`` if it's met; ``False`` otherwise.
    :rtype: bool
    
    """
    return predicate.is_met(request.environ)


def not_met(predicate):
    """
    Evaluate the :mod:`repoze.what` ``predicate`` checker and return ``False``
    if it's met.
    
    :param predicate: The :mod:`repoze.what` predicate checker to be evaluated.
    :return: ``False`` if it's met; ``True`` otherwise.
    :rtype: bool
    
    """
    return not predicate.is_met(request.environ)


def booleanize_predicates():
    """
    Make :mod:`repoze.what` predicates evaluable without passing the 
    ``environ`` explicitly.
    
    .. warning::
    
        The use of this function is **strongly discouraged**. Use
        :func:`is_met` or :func:`not_met` instead.
    
    """
    Predicate.__nonzero__ = lambda self: self.is_met(request.environ)


def debooleanize_predicates():
    """
    Stop :mod:`repoze.what` predicates from being evaluable without passing the 
    ``environ`` explicitly.
    
    This function reverts :func:`booleanize_predicates`.
    
    """
    del Predicate.__nonzero__