# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zptest/virthosts/src/my315ok.portlet.rollitems/my315ok/portlet/rollitems/rollportlet.py
# Compiled at: 2009-07-09 23:10:46
import random, time
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.ATContentTypes.interface import IATTopic
from plone.portlet.collection import PloneMessageFactory as _a
from my315ok.portlet.rollitems import RollPortletMessageFactory as _

class IRollPortlet(IPortletDataProvider):
    """A portlet which renders the results of a collection object.
    """
    __module__ = __name__
    header = schema.TextLine(title=_a('Portlet header'), description=_a('Title of the rendered portlet'), required=True)
    target_collection = schema.Choice(title=_a('Target collection'), description=_a('Find the collection which provides the items to list'), required=True, source=SearchableTextSourceBinder({'object_provides': IATTopic.__identifier__}, default_query='path:'))
    limit = schema.Int(title=_a('Limit'), description=_a('Specify the maximum number of items to show in the portlet. Leave this blank to show all items.'), required=False)
    random = schema.Bool(title=_a('Select random items'), description=_a('If enabled, items will be selected randomly from the collection, rather than based on its sort order.'), required=True, default=False)
    show_more = schema.Bool(title=_a('Show more... link'), description=_a('If enabled, a more... link will appear in the footer of the portlet, linking to the underlying Collection.'), required=True, default=True)
    show_dates = schema.Bool(title=_a('Show dates'), description=_a('If enabled, effective dates will be shown underneath the items listed.'), required=True, default=True)
    roll_images = schema.Bool(title=_('roll images'), description=_('If enabled,  will be shown roll image items,else roll text items.'), required=True, default=False)
    previewmode = schema.Choice(title=_('image size'), description=_('Choose source image size'), required=True, default='thumb', vocabulary='rollitems.ImageSizeVocabulary')
    roll_direc = schema.Choice(title=_('direction'), description=_('Choose the roll direction'), vocabulary='rollitems.RollDirectionVocabulary')
    speed = schema.Int(title=_('speed'), description=_('Specify the speed of the roll items '), required=True)
    roll_width = schema.Int(title=_('roll_width'), description=_('Specify the width of the roll zone .'), required=True)
    roll_height = schema.Int(title=_('roll_height'), description=_('Specify the height of the roll zone .'), required=True)


class Assignment(base.Assignment):
    """
    Portlet assignment.    
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IRollPortlet)
    header = ''
    target_collection = None
    limit = 5
    random = False
    show_more = True
    show_dates = True
    speed = 35
    roll_width = 110
    roll_height = 70
    previewmode = 'thumb'
    roll_direc = 'top'
    roll_images = False

    def __init__(self, header='', target_collection=None, limit=None, random=False, show_more=True, show_dates=False, speed=None, roll_width=None, roll_height=None, previewmode=None, roll_direc=None, roll_images=False):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.random = random
        self.show_more = show_more
        self.show_dates = show_dates
        self.speed = speed
        self.roll_width = roll_width
        self.roll_height = roll_height
        self.previewmode = previewmode
        self.roll_direc = roll_direc
        self.roll_images = roll_images

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.
    
    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    _template = ViewPageTemplateFile('rollportlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    render = _template

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
    def js_settings(self):
        data = self.data
        out = []
        jsOut = ''
        jsOut += '\n var rootdiv = "rootlink";\n'
        jsOut += ' var son1 = "son1link";\n'
        jsOut += ' var son2 = "son2link";\n'
        jsOut += ' var collectScroll;\n'
        jsOut += ' var Ltab;\n'
        jsOut += ' var Ltab1;\n'
        jsOut += ' var Ltab2;\n'
        jsOut += ' var MyL;\n'
        jsOut += '\n var thelinkAutoScroll= new LinkAutoScroll();\n'
        if self.results():
            for obj in self.results():
                img = obj.getObject()
                Durl = img.absolute_url()
                Dtitle = img.Title()
                Dtime = img.Date()[:10]
                if data.roll_images:
                    jsOut += 'thelinkAutoScroll.addItem("%s/image_%s","","move_friendly_link","%s","%s","_blank");\n' % (Durl, data.previewmode, Durl, Dtitle)
                else:
                    jsOut += 'thelinkAutoScroll.addItem("","","move_friendly_link","%s","%s(%s)","_blank");\n' % (Durl, Dtitle, Dtime)

        jsOut += 'thelinkAutoScroll.play();'
        out.append('<!--')
        out.append('var LinkDirection = "%s";' % data.roll_direc)
        out.append('var Isimage = "%s";' % data.roll_images)
        out.append('var Lspeed = %s;' % data.speed)
        out.append('var LAWidth = %s;' % data.roll_width)
        out.append('var LAHeight = %s;' % data.roll_height)
        out.append(jsOut)
        out.append('-->')
        return ('\n').join(out)

    def results(self):
        """ Get the actual result brains from the collection. 
            This is a wrapper so that we can memoize if and only if we aren't
            selecting random items."""
        if self.data.random:
            return self._random_results()
        else:
            return self._standard_results()

    @memoize
    def _standard_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog()
            if self.data.limit and self.data.limit > 0:
                results = results[:self.data.limit]
        return results

    def _random_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog(sort_on=None)
            limit = self.data.limit and min(len(results), self.data.limit) or 1
            try:
                results = [ results._seq[1]._func(i) for i in random.sample(results._seq[1]._seq, limit) ]
            except AttributeError, IndexError:
                results = []

        return results

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
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(collection_path, default=None)


class AddForm(base.AddForm):
    """Portlet add form.
    
    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IRollPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
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
    form_fields = form.Fields(IRollPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    label = _a('Edit Collection Portlet')
    description = _a('This portlet display a listing of items from a Collection.')