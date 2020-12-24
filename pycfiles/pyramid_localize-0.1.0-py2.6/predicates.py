# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/routing/predicates.py
# Compiled at: 2014-05-04 12:45:31
"""Localize route predicate."""

def language(field):
    """Create language predicate for given url match field."""

    def predicate(info, request):
        """Check whether language is one of the defaults."""
        if field in info['match'] and info['match'][field] in request.registry['config'].localize.locales.available:
            return True
        return False

    return predicate


language.__text__ = 'language predicate, to determine allowed languages in route'