# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/browser/manage.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope.formlib import form
from zope.event import notify
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.app.file.interfaces import IImage
from zope.cachedescriptors.property import Lazy
from zope.lifecycleevent import ObjectModifiedEvent
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.dublincore.interfaces import IZopeDublinCore
from zope.contentprovider.interfaces import IContentProvider
from zope.component import getUtilitiesFor, queryUtility, getUtility
from ice.adverlet.interfaces import IFileStorage, IImageWrapper
from ice.adverlet.interfaces import IAdverlet, ISourceStorage
from ice.adverlet.image import ImageWrapper
from interfaces import IManageUITemplate
from widget import RichTextWidget
from ice.adverlet.i18n import _

class ManageForm(form.FormBase):
    __module__ = __name__
    implements(IContentProvider)
    primary_actions = form.Actions()
    secondary_actions = form.Actions()
    preview = None
    info = None
    no_changes = False

    def __init__(self, context, request, view):
        self.__parent__ = view
        self.request = request
        self.context = self.getContext()
        self.default_css = self._sources.defaultCSS
        self.template = getMultiAdapter((self, self.request), IManageUITemplate, name='ice.adverlet.ManageTemplate')
        if IAdverlet(self.context, None):
            self.title = _('Edit HTML')
            self.form_fields = form.Fields(IAdverlet)
            if IAdverlet(self.context).wysiwyg:
                self.form_fields['source'].custom_widget = RichTextWidget
                self.form_fields = self.form_fields.omit('newlines')
                IAdverlet(self.context).newlines = False
            self.form_fields = self.form_fields.omit('__name__', 'description', 'default')
        elif ISourceStorage(self.context, None):
            self.title = _('Edit settings')
            self.form_fields = form.Fields(ISourceStorage)
            self.form_fields = self.form_fields.omit('defaultCSS')
        elif IImageWrapper(self.context, None):
            self.title = _('Upload File')
            self.form_fields = form.Fields(IImageWrapper)
        if self.context:
            super(ManageForm, self).__init__(self.context, request)
        return

    @Lazy
    def _sources(self):
        return getUtility(ISourceStorage)

    @Lazy
    def _files(self):
        return getUtility(IFileStorage)

    def getContext(self):
        request = self.request
        custom = request.get('custom')
        settings = request.get('settings')
        upload = request.get('images')
        if custom:
            return queryUtility(IAdverlet, custom)
        elif settings:
            return self._sources
        elif upload:
            return ImageWrapper()
        else:
            return
        return

    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        if self.context:
            self.widgets = form.setUpEditWidgets(self.form_fields, self.prefix, self.context, self.request, adapters=self.adapters, ignore_request=ignore_request)
        else:
            self.widgets = ()

    def update(self):
        request = self.request
        self.adverlets = [ i[1] for i in getUtilitiesFor(IAdverlet) ]
        preview_name = request.get('preview')
        if preview_name:
            adv = queryUtility(IAdverlet, preview_name)
            self.adverlet_name = adv.__name__
            self.preview = adv and adv.source
        file_key = request.get('delete')
        if file_key:
            del self._files[file_key]
            self.redirect('?images=yes')
        self.setUpWidgets()
        self.form_reset = False
        data = {}
        if form.handleSubmit(self.secondary_actions, data)[1]:
            self.redirect()
        (errors, action) = form.handleSubmit(self.primary_actions, data, self.validate)
        if errors:
            self.status = 'There were errors'
            result = action.failure(data, errors)
        elif errors is not None:
            self.form_reset = True
            result = action.success(data)
        else:
            result = None
        self.form_result = result
        if action and not errors and not self.no_changes:
            custom = request.get('custom')
            self.redirect(request.get('images') and '?images=yes' or request.get('settings') and '?settings=yes' or custom and '?custom=%s' % custom or '')
        return

    @Lazy
    def actions(self):
        return list(self.primary_actions) + list(self.secondary_actions)

    @form.action(_('Apply'), primary_actions)
    def handle_apply_action(self, action, data):
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            self.status = _('Updated')
        else:
            self.status = _('No changes')
            self.no_changes = True

    @form.action(_('Close'), secondary_actions)
    def handle_close_action(self, *argv):
        pass

    def redirect(self, query=''):
        self.request.response.redirect(str(self.request.URL) + query)

    @property
    def info(self):
        """ Some information """
        sources_size = sum([ len(source) for source in self._sources.sources.values() if source ])
        images_size = sum([ f.getSize() for f in self._files.values() if IImage(f, None) ])
        return {'sources_size': sources_size, 'images_size': images_size}

    def getFiles(self):
        """ Listing of images """
        for (id, ob) in self._files.items():
            if IImage(ob, None):
                yield {'id': id, 'ob': ob, 'dc': IZopeDublinCore(ob)}

        return

    def render(self):
        if self.form_result is None:
            if self.form_reset:
                self.resetForm()
                self.form_reset = False
            self.form_result = self.template(self)
        return self.form_result