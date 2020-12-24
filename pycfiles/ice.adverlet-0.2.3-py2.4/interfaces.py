# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/interfaces.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
__docformat__ = 'restructuredtext'
from zope.interface import Interface, Attribute
from zope.tales.interfaces import ITALESExpression
from zope.schema import Text, TextLine, List, Choice, Bool
from zope.location.interfaces import ILocation
from zope.app.file.interfaces import IImage
from i18n import _

class IAdverlet(ILocation):
    """ Adverlet """
    __module__ = __name__
    description = Text(title=_('Description'), required=False)
    default = TextLine(title=_('Default view name'), required=False)
    source = Text(title=_('HTML Source'), required=False)
    wysiwyg = Bool(title=_('Rich-text editor'), default=True)
    newlines = Bool(title=_('Render newlines'), default=False)


class ISourceStorage(Interface):
    """ Storage for HTML sources """
    __module__ = __name__
    sources = Attribute('HTML sources')
    mceplugins = List(title=_('TinyMCE Plugins'), default=[], value_type=Choice(vocabulary='ice.adverlet.mceplugins'))
    defaultCSS = Bool(title=_('Include default css-styles for management UI'), default=True)


class IFileStorage(Interface):
    """ Files storage """
    __module__ = __name__


class IImageWrapper(IImage):
    """ Image wrapper """
    __module__ = __name__
    description = TextLine(title=_('Description'))


class ISourceModifiedEvent(Interface):
    """ Event """
    __module__ = __name__


class ITALESAdverletExpression(ITALESExpression):
    """ Returns a HTML content of the adverlet.
    To call a adverlet in a view use the follow syntax
    in a page template::

      <tal:block content="structure adverlet:adverlet_name" />

    Thus, adverlet is looked up only by the name.
    """
    __module__ = __name__