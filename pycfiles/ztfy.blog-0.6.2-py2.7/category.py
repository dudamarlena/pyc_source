# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/interfaces/category.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from zope.container.interfaces import IContainer, IContained
from ztfy.i18n.interfaces import II18nAttributesAware
from zope.container.constraints import containers, contains
from zope.interface import Interface
from zope.schema import List, Object, Int
from ztfy.i18n.schema import I18nText, I18nTextLine
from ztfy.blog import _

class ICategoryInfo(II18nAttributesAware):
    """Marker interface used to handle circular references"""
    title = I18nTextLine(title=_('Title'), description=_('Title of the category'), required=True)
    shortname = I18nTextLine(title=_('Short name'), description=_('Short name of the category'), required=True)
    heading = I18nText(title=_('Heading'), description=_('Short description of the category'), required=False)

    def getCategoryIds():
        """Get IDs of category and sub-categories"""
        pass

    def getVisibleTopics():
        """Get list of visible topics matching this category"""
        pass


class ICategoryWriter(Interface):
    """Category writer interface"""
    pass


class ICategory(ICategoryInfo, ICategoryWriter, IContainer, IContained):
    """Category full interface"""
    contains('ztfy.blog.interfaces.category.ICategory')
    containers('ztfy.blog.interfaces.category.ICategory', 'ztfy.blog.interfaces.category.ICategoryManager')


class ICategoryManager(ICategory):
    """Categories management interface"""
    pass


class ICategoryManagerTarget(Interface):
    """Marker interface for categories management"""
    pass


class ICategorizedContent(Interface):
    """Content catagory target interface"""
    categories = List(title=_('Categories'), description=_('List of categories associated with this content'), required=False, default=[], value_type=Object(schema=ICategory))
    categories_ids = List(title=_('Categories IDs'), description=_("Internal IDs of content's categories, used for indexing"), required=False, readonly=True, value_type=Int())


class ICategoriesTarget(Interface):
    """Marker interface for contents handling categories"""
    pass