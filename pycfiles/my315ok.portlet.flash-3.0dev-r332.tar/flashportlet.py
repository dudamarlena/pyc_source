# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/adam/workspace/virthosts/src/my315ok.portlet.flash/my315ok/portlet/flash/flashportlet.py
# Compiled at: 2010-08-08 10:54:13
import re
from zope.interface import implements
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.ATContentTypes.interface import IATTopic
from Products.ATFlashMovie.interfaces import IFlashMovie
from my315ok.portlet.flash import FlashPortletMessageFactory as _
from plone.portlet.collection import PloneMessageFactory as _a
color_validator = re.compile('[a-fA-F\\d]{6,6}$').match

class IFlashPortlet(IPortletDataProvider):
    """A portlet
    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    header = schema.TextLine(title=_a('Portlet header'), description=_a('Title of the rendered portlet'), required=True)
    swfsrc = schema.TextLine(title=_('target URI'), description=_('the URI of the flash'), required=False)
    target_collection = schema.Choice(title=_a('Target collection'), description=_a('Find the collection which provides the items to list'), required=False, source=SearchableTextSourceBinder({'object_provides': IATTopic.__identifier__}, default_query='path:'))
    target_flash = schema.Choice(title=_a('Target flash'), description=_a('Find the flash file which provides the flash source'), source=SearchableTextSourceBinder({'object_provides': IFlashMovie.__identifier__}, default_query='path:'))
    limit = schema.Int(title=_a('Limit'), description=_a('Specify the maximum number of items to show in the portlet. Leave this blank to show all items.'), required=False)
    swfLocid = schema.TextLine(title=_("swf's location"), description=_('the flash position will put'), required=True)
    wmode = schema.TextLine(title=_('wmode'), description=_('the flash background model'), required=True)
    swf_width = schema.Int(title=_('swf_width'), description=_('Specify the width of the full flash.'), required=True)
    swf_height = schema.Int(title=_('swf_height'), description=_('Specify the height of the full flash.'), required=True)
    color_bg = schema.TextLine(title=_('Background color'), description=_('Choose a custom background color. Use hex color codes.'), required=True, default='ffffff', constraint=color_validator)


class Assignment(base.Assignment):
    """Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IFlashPortlet)
    header = ''
    swfsrc = ''
    target_collection = None
    target_flash = None
    limit = 1
    swfLocid = ''
    wmode = 'transparent'
    swf_width = None
    swf_height = None
    color_bg = 'ffffff'

    def __init__(self, header='', swfsrc='', target_collection=None, target_flash=None, limit=1, swfLocid='', wmode='transparent', swf_width=None, swf_height=None, color_bg='ffffff'):
        self.header = header
        self.swfsrc = swfsrc
        self.target_collection = target_collection
        self.target_flash = target_flash
        self.limit = limit
        self.swfLocid = swfLocid
        self.wmode = wmode
        self.swf_width = swf_width
        self.swf_height = swf_height
        self.color_bg = color_bg

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('flashportlet.pt')

    @property
    def available(self):
        return len(self.results())

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return
        else:
            return collection.absolute_url()
        return

    @memoize
    def results(self):
        """ Get the actual result brains from the collection. 
            This is a wrapper so that we can memoize if and only if we aren't
            selecting random items."""
        file_path = self.data.target_flash
        swfsrc = self.data.swfsrc
        if swfsrc:
            return swfsrc
        elif not file_path:
            return self._standard_results()
        else:
            return self.flash_path()

    @memoize
    def _standard_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog()
            if self.data.limit and self.data.limit > 0:
                brain = results[0]
                result = brain.getURL() + '/index_html'
        return result

    def portal_state(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
        return portal_state

    @memoize
    def collection(self):
        """ get the collection the portlet is pointing to"""
        collection_path = self.data.target_collection
        if not collection_path:
            return
        if collection_path.startswith('/'):
            collection_path = collection_path[1:]
        if not collection_path:
            return
        portal = self.portal_state().portal()
        return portal.unrestrictedTraverse(collection_path, default=None)

    @memoize
    def flash_path(self):
        """ get the flash file's path"""
        collection_path = self.data.target_flash
        if not collection_path:
            return
        swf_url = self.portal_state().portal_url() + collection_path
        swfrender = swf_url + '/index_html'
        return swfrender

    @memoize
    def swfvars(self):
        data = self.data
        vrs = {}
        vrs['menu'] = 'false'
        vrs['quality'] = 'best'
        vrs['scale'] = 'noscale'
        vrs['allowScriptAccess'] = 'sameDomain'
        vrs['height'] = data.swf_height
        vrs['width'] = data.swf_width
        vrs['wmode'] = data.wmode
        return vrs

    @memoize
    def locid(self):
        if '#' in self.data.swfLocid:
            locid = self.data.swfLocid[1:]
        else:
            locid = self.data.swfLocid
        return locid

    @memoize
    def js_settings(self):
        swf = self.results()
        if swf:
            svars = self.swfvars()
            out = 'genswf("%(swfile)s","%(we)s",%(ht)s,%(wh)s,"#%(swfLocid)s")' % dict(swfile=swf, ht=svars['height'], wh=svars['width'], we=svars['wmode'], swfLocid=self.locid())
            return out
        else:
            return "document.write('<div>you has been not assign a source flash file</div>');"


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IFlashPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['target_flash'].custom_widget = UberSelectionWidget
    label = _a('Add Collection Portlet')
    description = _a('This portlet display a listing of items from a Collection.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(IFlashPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['target_flash'].custom_widget = UberSelectionWidget
    label = _a('Edit Collection Portlet')
    description = _a('This portlet display a listing of items from a Collection.')