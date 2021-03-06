# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/LinguaFaceTool.py
# Compiled at: 2010-11-30 09:59:25
import re, os
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from DateTime import DateTime
from ZODB.POSException import ConflictError
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from OFS.CopySupport import _cb_decode, cookie_path, _cb_encode
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.utils import UniqueObject
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import transaction_note, getToolByName
import Products.Archetypes.Field
from Products.LinguaFace import config, LOG
from interface import ILinguaFaceTool
from plone.locking.interfaces import ILockable
from Products.LinguaPlone.interfaces import ITranslatable

class LinguaFaceTool(PropertyManager, UniqueObject, SimpleItem):
    """
        This tool holds the Google Analytics Id inserted on each page.
    """
    __module__ = __name__
    implements(ILinguaFaceTool)
    id = config.TOOL_ID
    meta_type = 'LinguaFaceTool'
    plone_tool = 1
    title = 'LinguaFace Tool'
    synchronise_translations_workflow = False
    _properties = ({'id': 'synchronise_translations_workflow', 'type': 'boolean', 'mode': 'w'},)
    overviewPath = os.path.join(os.path.dirname(__file__), 'zmi', 'overview')
    manage_options = ({'label': 'Overview', 'action': 'overview'},) + PropertyManager.manage_options + SimpleItem.manage_options
    security = ClassSecurityInfo()
    overview = PageTemplateFile(overviewPath)
    security.declareProtected(CMFCorePermissions.ManagePortal, 'overview')
    security.declarePrivate('manage_afterAdd')

    def manage_afterAdd(self, item, container):
        SimpleItem.manage_afterAdd(self, item, container)

    security.declarePrivate('getShortContentSubClass')

    def getShortContentSubClass(self, field, instance):
        """
            Override this function if you want to add your own Field handlers.
        """
        return False

    security.declarePublic('getShortContent')

    def getShortContent(self, field, instance):
        """
            Return a short string value for each type of field
            field is the field instance that have to be "short-displayed"
            instance is the content instance
        """
        result = self.getShortContentSubClass(field, instance)
        if result:
            return result
        if isinstance(field, Products.Archetypes.Field.StringField) or isinstance(field, Products.Archetypes.Field.IntegerField) or isinstance(field, Products.Archetypes.Field.BooleanField):
            result = str(field.getAccessor(instance)())
        elif isinstance(field, Products.Archetypes.Field.TextField):
            result = str(field.getAccessor(instance)())
            result = re.sub('<.*>', '', result)[:100]
        elif isinstance(field, (Products.Archetypes.Field.ImageField, Products.Archetypes.Field.FileField)):
            result = field.getFilename(instance)
        elif isinstance(field, Products.Archetypes.Field.ReferenceField):
            result = '<em>References</em>'
        else:
            result = '<em>No short content found (%s).</em>' % field.__class__.__name__
        if len(result) == 0:
            return '<em>Field is empty.</em>'
        else:
            return result

    security.declarePublic('isTranslatable')

    def isTranslatable(self, object):
        """ return true if object is translatable """
        return base_hasattr(object, 'getCanonicalPath')

    security.declarePublic('assembleCopies')

    def assembleCopies(self, cp_list, op):
        """
        Put together the data from several copies
        """
        context = self
        request = self.REQUEST
        oblist = []
        for cp in cp_list:
            oblist.extend(_cb_decode(cp)[1])

        cp = (
         op, oblist)
        cp = _cb_encode(cp)
        resp = request.RESPONSE
        resp.setCookie('__cp', cp, path='%s' % cookie_path(request))
        request['__cp'] = cp
        return cp

    security.declarePrivate('_editContent')

    def _editContent(self, obj, effective, expiry):
        """
        edit expires and actives dates on workflow transitions
        """
        kwargs = {}
        if effective and (isinstance(effective, DateTime) or len(effective) > 5):
            kwargs['effective_date'] = effective
        if expiry and (isinstance(expiry, DateTime) or len(expiry) > 5):
            kwargs['expiration_date'] = expiry
        plone_utils = getToolByName(self, 'plone_utils')
        plone_utils.contentEdit(obj, **kwargs)

    security.declareProtected(CMFCorePermissions.View, 'doWorkflowAction')

    def doWorkflowAction(self, context, workflow_action, comment, effective_date, expiration_date):
        """
          do workflow actions on context
        """
        plone_utils = getToolByName(self, 'plone_utils')
        contentEditSuccess = 0
        plone_log = self.plone_log
        new_context = self.portal_factory.doCreate(context)
        portal_workflow = new_context.portal_workflow
        transitions = portal_workflow.getTransitionsFor(new_context)
        transition_ids = [ t['id'] for t in transitions ]
        if workflow_action in transition_ids and not effective_date and context.EffectiveDate() == 'None':
            effective_date = DateTime()
        try:
            self._editContent(new_context, effective_date, expiration_date)
            contentEditSuccess = 1
        except (Unauthorized, 'Unauthorized'):
            pass

        wfcontext = context
        note = 'Changed status of %s at %s' % (wfcontext.title_or_id(), wfcontext.absolute_url())
        if workflow_action in transition_ids:
            wfcontext = new_context.portal_workflow.doActionFor(context, workflow_action, comment=comment)
        if not wfcontext:
            wfcontext = new_context
        if not contentEditSuccess:
            try:
                self._editContent(wfcontext, effective_date, expiration_date)
            except (Unauthorized, 'Unauthorized'):
                pass

        transaction_note(note)
        if plone_utils.isDefaultPage(new_context):
            parent = new_context.aq_inner.aq_parent
            try:
                self.doWorkflowAction(parent, workflow_action, comment, effective_date=effective_date, expiration_date=expiration_date)
            except ConflictError:
                raise
            except Exception:
                pass

    def _moveTranslatedContents(self, folder):
        """
        move Translated contents in good folder
        do not change modification date

        only for a site with two languages (can be easily changed for x languages)
        """
        otherlangs = []
        if folder.isPrincipiaFolderish and ITranslatable.providedBy(folder):
            translations = folder.getOtherTranslations()
            tDict = {}
            idsDict = {}
            for t in translations:
                lang = t.getLanguage()
                otherlangs.append(lang)
                tDict[lang] = t
                idsDict[lang] = []

            for obj in folder.objectValues():
                if ITranslatable.providedBy(obj):
                    lang = obj.getLanguage()
                    if not lang:
                        lang = 'neutral'
                    if lang in otherlangs:
                        lockable = ILockable(obj, None)
                        if lockable is not None and lockable.can_safely_unlock():
                            lockable.unlock()
                        idsDict[lang].append(obj.getId())

            for lang in otherlangs:
                moveids = idsDict[lang]
                if moveids:
                    trans = tDict[lang]
                    trans._v__dont_move_translations__ = True
                    trans.manage_pasteObjects(folder.manage_cutObjects(moveids))
                    LOG.info('%s', 'move this ids inside folder : %s' % str(moveids))
                    for oid in moveids:
                        newobj = getattr(trans, oid)
                        newobj.reindexObject(idxs=['path', 'getCanonicalPath'])

        return

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'fixTranslationsPath')

    def fixTranslationsPath(self, folder):
        """
            Move translated content inside good translated folders
            after clone/move objects
        """
        for f in folder.myGetTranslations():
            self._moveTranslatedContents(f)


InitializeClass(LinguaFaceTool)