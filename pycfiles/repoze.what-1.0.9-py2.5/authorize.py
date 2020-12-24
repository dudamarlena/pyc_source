# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/what/authorize.py
# Compiled at: 2010-04-06 05:16:33
"""
Utilities to restrict access based on predicates.

.. deprecated:: 1.0.4
    This module won't be available in :mod:`repoze.what` v2. See
    :meth:`repoze.what.predicates.Predicate.check_authorization`.

"""
from warnings import warn
from repoze.what.predicates import *

def check_authorization(predicate, environ):
    """
    Verify if the current user really can access the requested source.
    
    :param predicate: The predicate to be evaluated.
    :param environ: The WSGI environment.
    :raise NotAuthorizedError: If it the predicate is not met.
    
    .. deprecated:: 1.0.4
        Use :meth:`repoze.what.predicates.Predicate.check_authorization`
        instead.
    
    .. versionchanged:: 1.0.4
        :class:`repoze.what.predicates.PredicateError` used to be the exception
        raised.
    
    """
    msg = 'repoze.what.authorize is deprecated for forward compatibility with repoze.what v2; use Predicate.check_authorization(environ) instead'
    warn(msg, DeprecationWarning, stacklevel=2)
    if predicate is not None:
        predicate.check_authorization(environ)
    return