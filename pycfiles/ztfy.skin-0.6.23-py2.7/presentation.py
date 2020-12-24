# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/presentation.py
# Compiled at: 2014-05-08 10:52:05
__docformat__ = 'restructuredtext'
import copy
from hurry.query.interfaces import IQuery
from z3c.json.interfaces import IJSONWriter
from z3c.language.switch.interfaces import II18n
from zope.dublincore.interfaces import IZopeDublinCore
from zope.intid.interfaces import IIntIds
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.traversing.interfaces import TraversalError
from ztfy.skin.interfaces import ISkinnable, IPresentationTarget, IPresentationForm, IBaseIndexView
from z3c.form import field
from z3c.formjs import ajax
from z3c.template.template import getLayoutTemplate
from zope.component import queryUtility, queryMultiAdapter, getUtility
from zope.interface import implements
from zope.publisher.skinnable import applySkin
from zope.traversing import namespace
from ztfy.skin.form import DialogEditForm
from ztfy.skin.page import TemplateBasedPage
from ztfy.utils.catalog.index import Text
from ztfy.utils.traversing import getParent

class PresentationNamespaceTraverser(namespace.view):
    """++presentation++ namespace"""

    def getSkin(self):
        skinnable = getParent(self.context, ISkinnable)
        if skinnable is None:
            return
        else:
            skin_name = skinnable.getSkin()
            if skin_name is None:
                return
            return queryUtility(IBrowserSkinType, skin_name)

    def traverse(self, name, ignored):
        skin = self.getSkin()
        if skin is None:
            raise TraversalError('++presentation++')
        fake = copy.copy(self.request)
        applySkin(fake, skin)
        adapter = queryMultiAdapter((self.context, fake), IPresentationTarget)
        if adapter is not None:
            try:
                return adapter.target_interface(self.context)
            except:
                pass

        raise TraversalError('++presentation++')
        return


class BasePresentationEditForm(DialogEditForm):
    """Presentation edit form"""
    implements(IPresentationForm)
    layout = getLayoutTemplate()

    def __init__(self, context, request):
        super(BasePresentationEditForm, self).__init__(context, request)
        skin = self.getSkin()
        if skin is None:
            raise NotFound(self.context, self.name, self.request)
        fake = copy.copy(self.request)
        applySkin(fake, skin)
        adapter = queryMultiAdapter((self.context, fake, self), IPresentationTarget)
        if adapter is None:
            adapter = queryMultiAdapter((self.context, fake), IPresentationTarget)
        if adapter is None:
            raise NotFound(self.context, self.name, self.request)
        self.interface = adapter.target_interface
        return

    def getContent(self):
        return self.interface(self.context)

    @property
    def fields(self):
        return field.Fields(self.interface)

    def getSkin(self):
        skinnable = getParent(self.context, ISkinnable)
        if skinnable is None:
            return
        else:
            skin_name = skinnable.getSkin()
            if skin_name is None:
                return
            return queryUtility(IBrowserSkinType, skin_name)

    @ajax.handler
    def ajaxEdit(self):
        return super(BasePresentationEditForm, self).ajaxEdit(self)

    @ajax.handler
    def ajaxSearch(self):
        writer = getUtility(IJSONWriter)
        title = self.request.form.get('title')
        if not title:
            return writer.write(None)
        else:
            query = getUtility(IQuery)
            intids = getUtility(IIntIds)
            result = []
            for obj in query.searchResults(Text(('Catalog', 'title'), {'query': title + '*', 'ranking': True})):
                i18n = II18n(obj, None)
                result.append({'oid': intids.register(obj), 'title': i18n.queryAttribute('title') if i18n is not None else IZopeDublinCore(obj).title})

            return writer.write(result)


class BaseIndexView(TemplateBasedPage):
    """Base index view"""
    implements(IBaseIndexView)
    presentation = None

    def update(self):
        super(BaseIndexView, self).update()
        adapter = queryMultiAdapter((self.context, self.request, self), IPresentationTarget)
        if adapter is None:
            adapter = queryMultiAdapter((self.context, self.request), IPresentationTarget)
        if adapter is not None:
            interface = adapter.target_interface
            self.presentation = interface(self.context)
        return