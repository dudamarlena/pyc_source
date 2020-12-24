# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/zcml/smartmenuitem/metadirectives.py
# Compiled at: 2008-12-22 18:19:14
"""Interface of ZCML metadirective "smartmenuitem"

$Id: metadirectives.py 23904 2007-11-27 15:42:17Z anatoly $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 23904 $'
__date__ = '$Date: 2007-11-27 17:42:17 +0200 (Tue, 27 Nov 2007) $'
from copy import copy
from zope.interface import Interface
from zope.schema import TextLine, Field
from zope.configuration.fields import GlobalInterface
from zope.app.publisher.browser.metadirectives import IMenuItemDirective
from zope.configuration.fields import Tokens, GlobalObject

class ISmartMenuItemDirective(IMenuItemDirective):
    __module__ = __name__
    originUtilityInterface = GlobalInterface(title='Origin Utility Interface', description='Interface of registered utility, used for origin', required=False)
    originUtilityName = TextLine(title='Origin Utility Name', description='Name of registered utility, used for origin', default='', required=False)
    originAdapterInterface = GlobalInterface(title='Origin Adapter Interface', description='Context and request will be adapted to Interface, used for origin', required=False)
    originAdapterName = TextLine(title='Origin Adapter Name', description='Context and request will be adapted to Interface, used for origin', default='', required=False)
    selectedCondition = TextLine(title='A condition for displaying the menu item selected', description='\n        The condition is given as a TALES expression. The expression\n        has access to the variables:\n\n        context -- The object the menu is being displayed for\n\n        request -- The browser request\n\n        nothing -- None\n\n        The menu item will not be displayed if there is a filter and\n        the filter evaluates to a false value.', required=False)


ISmartMenuItemDirective.setTaggedValue('keyword_arguments', True)