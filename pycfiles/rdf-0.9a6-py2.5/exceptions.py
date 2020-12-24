# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdf/exceptions.py
# Compiled at: 2008-03-16 19:10:10
"""
Various exceptions used in rdf.

"""

class Error(Exception):
    """Base class for rdf exceptions."""

    def __init__(self, msg=None):
        Exception.__init__(self, msg)
        self.msg = msg


class ParserError(Error):
    """RDF Parser error."""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class UniquenessError(Error):
    """A uniqueness assumption was made in the context, and that is not true"""

    def __init__(self, values):
        Error.__init__(self, 'Uniqueness assumption is not fulfilled. Multiple values are: %s' % values)