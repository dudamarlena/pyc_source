# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/pluggabletemplates/interfaces.py
# Compiled at: 2006-11-01 08:19:33
__docformat__ = 'reStructuredText'
from zope.contentprovider.interfaces import IContentProvider

class ITemplatedContentProvider(IContentProvider):
    """Content providers implementing this interface use templates to generate
    their content.
    """
    __module__ = __name__