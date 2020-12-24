# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/routing/predicates.py
# Compiled at: 2014-05-04 12:45:31
__doc__ = 'Localize route predicate.'

def language(field):
    """Create language predicate for given url match field."""

    def predicate(info, request):
        """Check whether language is one of the defaults."""
        if field in info['match'] and info['match'][field] in request.registry['config'].localize.locales.available:
            return True
        return False

    return predicate


language.__text__ = 'language predicate, to determine allowed languages in route'