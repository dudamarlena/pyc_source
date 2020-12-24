# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/gacontext/interfaces.py
# Compiled at: 2008-05-20 05:21:26
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 60982 $'
__version__ = '$Revision: 60982 $'[11:-2]
from zope.schema import SourceText
from zope.interface import Interface
from collective.gacontext import gacontextMessageFactory as _

class IGAContextMarker(Interface):
    """ a Marker interface
    """
    __module__ = __name__


class IGACode(Interface):
    """ The GA Form
    """
    __module__ = __name__
    ga_code = SourceText(title=_('JavaScript for web statistics support'), description=_('For enabling web statistics support from external providers (for e.g. Google Analytics). Paste the code snippets provided. It will be included in the rendered HTML as entered near the end of the page.'), default='', required=False)


class IGAFinder(Interface):
    """ Finds the responsible GA Code for the context
    """
    __module__ = __name__

    def __call__(self, context):
        """ Returns the ga_code or none
        """
        pass