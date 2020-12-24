# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/interfaces/extension.py
# Compiled at: 2012-06-04 04:50:16
from zope.interface import Interface, Attribute
from zope.schema import TextLine, URI
from ztfy.thesaurus import _

class IThesaurusTermExtension(Interface):
    """Thesaurus term extension interface
    
    An extension is a marker interface implemented by
    a term, which provides additional attributes to the term.
    
    Each available extension is defined as a named utility.
    """
    label = TextLine(title=_('Extension name'), description=_('User name given to the extension'), required=True)
    target_interface = Attribute(_('Extension marker interface'))
    target_view = URI(title=_('Extension target view'), required=True)
    icon = URI(title=_('Extension icon URI'), required=True)