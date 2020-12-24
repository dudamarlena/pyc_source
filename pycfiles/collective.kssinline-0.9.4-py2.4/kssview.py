# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/browser/kssview.py
# Compiled at: 2008-10-05 06:40:06
from zope.interface import implements
from Acquisition import aq_inner, aq_parent
from Acquisition import Implicit
from Products.CMFCore.utils import getToolByName
from Products.CMFFormController.ControllerState import ControllerState
from plone.app.kss.interfaces import IPloneKSSView
from plone.app.kss.plonekssview import PloneKSSView
from archetypes.kss.validation import validate, SKIP_KSSVALIDATION_FIELDTYPES
from Products.CMFPlone import PloneMessageFactory as _
from cgi import parse_qs
from urlparse import urlsplit
from kss.core import kssaction, KSSExplicitError
from kss.core.BeautifulSoup import BeautifulSoup
from plone.app.kss.content_replacer import acquirerFactory
from plone.app.layout.globals.interfaces import IViewView
from plone.locking.interfaces import ILockable
from zope.interface import alsoProvides
from zope.interface import implements
from zope.component import getMultiAdapter
from ZPublisher.HTTPRequest import HTTPRequest
from zope.component.exceptions import ComponentLookupError
import base64

class KssView(Implicit, PloneKSSView):
    __module__ = __name__
    implements(IPloneKSSView)

    def prepareAndShowPopup(self, dom_node_id, item_uid=None, container_uid=None, type_name=None, context=None):
        if context is None:
            context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        rc = getToolByName(context, 'reference_catalog')
        container = context
        if container_uid:
            container = rc.lookupObject(container_uid)
        item = None
        if item_uid:
            item = rc.lookupObject(item_uid)
        if item is None:
            assert type_name is not None
            pf = getToolByName(context, 'portal_factory')
            if pf.getFactoryTypes().get(type_name, False):
                newid = pf.generateUniqueId(type_name)
                pf_url = '%s/portal_factory/%s/%s' % (('/').join(context.getPhysicalPath()), type_name, newid)
                item = pf.restrictedTraverse(pf_url)
            else:
                newid = container.generateUniqueId(type_name)
                container.invokeFactory(type_name, newid)
                item = container._getOb(newid)
        html = container.evalMacro('archetype', template='kssinline_macros', here=item, context=item, container=container, controller_state=ControllerState(id='dummy', context=item, errors={}))
        selector = ksscore.getHtmlIdSelector('kssinline-popup-content')
        ksscore.replaceInnerHTML(selector, html)
        commands = self.getCommands()
        selector = ksscore.getHtmlIdSelector('kssinline-popup')
        commands.addCommand('kssinline-popupShow', selector=selector, dom_node_id=dom_node_id)
        return self.render()

    def actionMenuClickHandler(self, dom_node_id, href):
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        (proto, host, path, query, anchor) = urlsplit(href)
        if not query:
            raise KSSExplicitError, 'Nothing to do'
        di = parse_qs(query)
        type_name = di.get('type_name', None)
        if type(type_name) == type([]):
            type_name = type_name[(-1)]
        if not type_name:
            raise KSSExplicitError, 'No type_name specified'
        tool = getToolByName(context, 'portal_kssinline', None)
        if tool is None or type_name not in tool.getEditableTypes():
            raise KSSExplicitError, 'Inline editing not allowed'
        physical_path = list(self.request.physicalPathFromURL('%s://%s/%s' % (proto, host, path)))
        physical_path = physical_path[:-1]
        new_context = self.context.restrictedTraverse(('/').join(physical_path))
        return self.prepareAndShowPopup(dom_node_id=dom_node_id, type_name=type_name, context=new_context)

    def saveItem(self, action, url, item_uid=None, item_path=None):
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        item = context
        if item_path is not None and item_path.find('portal_factory') != -1:
            pf = getToolByName(context, 'portal_factory')
            item = pf.restrictedTraverse(item_path)
        elif item_uid:
            rc = getToolByName(context, 'reference_catalog')
            item = rc.lookupObject(item_uid)
        if action != 'form_submit':
            try:
                lock = getMultiAdapter((item, self.request), name='plone_lock_operations')
            except ComponentLookupError:
                pass
            else:
                lock.safe_unlock()

            commands = self.getCommands()
            selector = ksscore.getHtmlIdSelector('kssinline-popup')
            commands.addCommand('kssinline-popupHide', selector=selector)
            return self.render()
        instance = item
        schema = instance.Schema()
        errors = validate(schema, instance, self.request, errors={}, data=1, metadata=0, predicates=(
         lambda field: field.type not in SKIP_KSSVALIDATION_FIELDTYPES,))
        if errors:
            tool = getToolByName(context, 'plone_utils')
            tool.addPortalMessage(_('Please correct the indicated errors'), type='error')
            html = context.evalMacro('portal_message', template='global_statusmessage')
            selector = ksscore.getHtmlIdSelector('kssinline-popup-messages')
            ksscore.replaceInnerHTML(selector, html)
            ksscore.clearChildNodes(ksscore.getCssSelector('div.field div.fieldErrorBox'))
            for (fieldname, error) in errors.iteritems():
                if isinstance(error, str):
                    error = error.decode('utf', 'replace')
                self.context = instance
                self.getCommandSet('atvalidation').issueFieldError(fieldname, error)

        else:
            pf = getToolByName(context, 'portal_factory')
            instance = pf.doCreate(instance)
            instance.processForm(REQUEST=context.REQUEST)
            try:
                lock = getMultiAdapter((instance, self.request), name='plone_lock_operations')
            except ComponentLookupError:
                pass
            else:
                lock.safe_unlock()

            commands = self.getCommands()
            selector = ksscore.getHtmlIdSelector('kssinline-popup')
            commands.addCommand('kssinline-popupHide', selector=selector)
            self.request.form = {}
            if url:
                (proto, host, path, query, anchor) = urlsplit(url)
                if query:
                    env = {'SERVER_NAME': 'testingharnas', 'SERVER_PORT': '80'}
                    env['QUERY_STRING'] = query
                    req = HTTPRequest(None, env, None)
                    req.processInputs()
                    for (k, v) in req.form.items():
                        self.request.form[k] = v

                html = self.replaceContentRegion('%s://%s/%s' % (proto, host, path), tabid='contentview-folderContents')
            else:
                html = self.replaceContentRegion(context.absolute_url(), tabid='contentview-folderContents')
            if html:
                ksscore.replaceHTML(ksscore.getHtmlIdSelector('region-content'), html)
            self.getCommandSet('plone').issuePortalMessage(_('Changes saved.'))
        return self.render()

    def replaceContentRegion(self, url, tabid=''):
        """
        Shamelessly stolen from plone.app.kss
        """
        context = aq_inner(self.context)
        if not tabid or tabid == 'content':
            raise KSSExplicitError, 'No tabid on the tab'
        if not tabid.startswith('contentview-'):
            raise RuntimeError, 'Not a valid contentview id "%s"' % tabid
        (proto, host, path, query, anchor) = urlsplit(url)
        if query or anchor or proto not in ('http', 'https'):
            raise KSSExplicitError, 'Unhandled protocol on the tab'
        wrapping = acquirerFactory(context)
        path = list(self.request.physicalPathFromURL(url))
        obj_path = list(context.getPhysicalPath())
        if path == obj_path:
            utils = getToolByName(context, 'plone_utils')
            if utils.getDefaultPage(context) is not None:
                raise KSSExplicitError, 'no default page on the tab'
            (viewobj, viewpath) = utils.browserDefault(context)
            if len(viewpath) == 1:
                viewpath = viewpath[0]
            template = viewobj.restrictedTraverse(viewpath)
        else:
            if path[:-1] != obj_path:
                raise KSSExplicitError, 'cannot reload since the tab visits a different context'
            method = path[(-1)]
            try:
                method = context.getTypeInfo().queryMethodID(method, default=method)
            except AttributeError:
                pass

            template = wrapping.restrictedTraverse(method)
        content = template()
        soup = BeautifulSoup(content)
        replace_id = 'region-content'
        tag = soup.find('div', id=replace_id)
        if tag is None:
            raise RuntimeError, 'Result content did not contain <div id="%s">' % replace_id
        result = unicode(tag)
        return result


class ArchetypesKssWrapperView(Implicit, PloneKSSView):
    """
    Traversal only cares about the context it is aware of, which means
    ZCML permission settings operate on that context. Those permissions
    may not allow traversal, so we have to change the context and then 
    do the traversal.
    """
    __module__ = __name__
    implements(IPloneKSSView)

    def kssValidateField(self, fieldname, value, uid=None, item_path=None):
        """
        Our popup does have an item_path available, but it never gets 
        passed to this method since Archetypes' at.kss does not provide
        it.

        Instead we abuse kssattr-uid to store the item path if the object
        is temporary. This is done in override.py.
        """
        context = aq_inner(self.context)
        if item_path is not None and item_path.find('portal_factory') != -1:
            pf = getToolByName(context, 'portal_factory')
            new_context = pf.restrictedTraverse(item_path)
        elif uid is not None:
            possibly_decoded_uid = base64.b64decode(uid)
            if possibly_decoded_uid.find('portal_factory') != -1:
                pf = getToolByName(context, 'portal_factory')
                new_context = pf.restrictedTraverse(possibly_decoded_uid)
            else:
                rc = getToolByName(context, 'reference_catalog')
                new_context = rc.lookupObject(uid)
        if new_context is not None:
            context = new_context
        return context.restrictedTraverse('originalKssValidateField')(fieldname, value, uid=None)