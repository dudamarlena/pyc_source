# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/se/portlet/gallery/galleryportlet.py
# Compiled at: 2009-11-26 03:05:28
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey
from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from random import shuffle
import random
from se.portlet.gallery import GalleryPortletMessageFactory as _
from types import UnicodeType
_default_encoding = 'utf-8'

def _encode(s, encoding=_default_encoding):
    try:
        return s.encode(encoding)
    except (TypeError, UnicodeDecodeError, ValueError):
        return s


def _decode(s, encoding=_default_encoding):
    try:
        return unicode(s, encoding)
    except (TypeError, UnicodeDecodeError, ValueError):
        return s


class IGalleryPortlet(IPortletDataProvider):
    __module__ = __name__
    name = schema.TextLine(title=_('Title'), description=_('The title of the gallery. Leave blank to not display the title.'), default='', required=False)
    width = schema.Int(title=_('Width of the portlet'), description=_('Width in pixels. Enter 0 to allow default portlet width.'), required=True, default=0)
    height = schema.Int(title=_('Height of the portlet'), description=_('Height in pixels.'), required=True, default=128)
    omit_border = schema.Bool(title=_('Omit portlet border'), description=_('Tick this box if you want to render the text above without the standard header, border or footer.'), required=True, default=False)
    display_desc = schema.Bool(title=_('Display image description'), description=_('Tick to let portlet gallery display description of the image.'), required=True, default=True)
    desc_font_size = schema.TextLine(title=_('Description font size'), description=_('Font size of description'), default='7px', required=True)
    desc_font_color = schema.TextLine(title=_('Description font color'), description=_('Font color of description'), default='#CCCCCC', required=True)
    desc_height = schema.TextLine(title=_('Description height'), description=_('Height of description field under images.'), default='15px', required=True)
    count = schema.Int(title=_('Maximum number of pictures to display in gallery'), description=_('How many items to list.'), required=True, default=5)
    shuffle = schema.Bool(title=_('Shuffle'), description=_('Check to shuffle images.'), default=True, required=False)
    image_types = schema.Tuple(title=_('Image Types'), description=_('Image types to be included into search'), default=('Image', ), required=False, value_type=schema.Choice(vocabulary='plone.app.vocabularies.PortalTypes'))
    state = schema.Tuple(title=_('Workflow state'), description=_('Items in which workflow state to show. Leave blank to not include this criterium.'), default=(), required=False, value_type=schema.Choice(vocabulary='plone.app.vocabularies.WorkflowStates'))
    paths = schema.Text(title=_('Paths'), description=_('List of paths to be included in searching images (it will include all sub-folders). The path is relative to the Zope root, so if your Plone side id is Plone and you would like include all folders under it, you should enter /Plone'), default='/', required=True)
    div_id = schema.TextLine(title=_('ID'), description=_('Unique identifier for the gallery.'), default='slideshow' + str(random.randrange(0, 10001)), required=True)
    image_size = schema.TextLine(title=_('Image size'), description=_('Choose image resize function (e.g. large, preview, mini, thumb, title, icon, listing) or leave blank.'), default='thumb', required=False)
    anim_interval = schema.Int(title=_('Animation Interval.'), description=_('Time interval between slides change (in ms).'), required=True, default=5000)
    anim_steps = schema.Int(title=_('Animation duration.'), description=_('Duration of fade in/out animation (in ms).'), required=True, default=500)
    jquery_symbol = schema.TextLine(title=_('JQuery symbol'), description=_('JQuery introduce $ symbol, which in some versions of Plone is replaced by jq to avoid name-conflict. However in some versions it may still be $ or some of products you have installed might also changed it to $ or any different name.'), default='jq', required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IGalleryPortlet)

    def __init__(self, name='', width=0, height=128, omit_border=False, display_desc=True, desc_font_size='7px', desc_font_color='#CCCCCC', desc_height='15px', count=5, shuffle=True, image_types=('Image', ), state=(), paths=('/', ), div_id='slideshow' + str(random.randrange(0, 10001)), image_size='thumb', anim_interval=5000, anim_steps=500, jquery_symbol='jq'):
        self.name = name
        self.width = width
        self.height = height
        self.omit_border = omit_border
        self.display_desc = display_desc
        self.desc_font_size = desc_font_size
        self.desc_font_color = desc_font_color
        self.desc_height = desc_height
        self.count = count
        self.shuffle = shuffle
        self.image_types = image_types
        self.state = state
        self.paths = paths
        self.div_id = div_id
        self.image_size = image_size
        self.anim_interval = anim_interval
        self.anim_steps = anim_steps
        self.jquery_symbol = jquery_symbol

    @property
    def title(self):
        return _('Gallery Portlet')


class Renderer(base.Renderer):
    __module__ = __name__
    _template = ViewPageTemplateFile('galleryportlet.pt')
    imageFirstId = 0

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()
        self.portal = portal_state.portal()
        self.navigation_root_path = portal_state.navigation_root_path()

    render = _template

    @property
    def available(self):
        return len(self._data())

    def resize_function(self):
        if self.data.image_size:
            return '/image_' + self.data.image_size
        else:
            return ''

    def images(self):
        return self._data()

    def title(self):
        return self.data.name

    def width(self):
        return self.data.width

    def height(self):
        return self.data.height

    def gallery_css(self):
        if self.width() > 0:
            widthTag = 'width: %dpx  !important;' % self.width()
        else:
            widthTag = ''
        id = self.data.div_id
        images = self.images()
        if len(images) > 0:
            if self.data.shuffle:
                self.imageFirstId = random.randrange(0, len(images) - 1)
            firstImgTag = "background-image:url('%s');" % (images[self.imageFirstId].getURL() + self.resize_function())
        else:
            firstImgTag = ''
        return ('\n<style type="text/css">\n#slideshow {\n   %s\n   background-repeat: no-repeat;\n   background-attachment: related;\n   background-position: center center;\n   %s\n   height:%spx;\n}\n#slideshow-desc {\n   font-size: %s;\n   color: %s;\n   text-align:center;\n   height:%s;\n}\n</style> ' % (firstImgTag, widthTag, self.height(), self.data.desc_font_size, self.data.desc_font_color, self.data.desc_height)).replace('slideshow', id)

    def div_id(self):
        return self.data.div_id

    def gallery_js(self):
        id = self.data.div_id
        images = self.images()
        if len(images) > 0:
            imagesList = 'var images' + id + ' = ['
            imagesDescList = 'var imagesDesc' + id + ' = ['
            for img in images:
                imagesList = imagesList + "'" + img.getURL() + self.resize_function() + "', "
                imagesDescList = imagesDescList + "'" + _decode(_encode(img.Description)).replace("'", "\\'").replace('\n', '<br/>').replace('\r', '') + "', "

            imagesList = imagesList + ']'
            imagesDescList = imagesDescList + ']'
            firstImgDesc = _decode(_encode(images[self.imageFirstId].Description)).replace("'", "\\'").replace('\n', '<br/>').replace('\r', '')
        else:
            imagesList = '[]'
            imagesDescList = '[]'
            firstImgDesc = '&nbsp;'
        jsInitCounter = 'var galleryCounter = %d;\n' % self.imageFirstId
        if self.data.shuffle:
            jsChooseNext = '\n       \t    \tgalleryCounterOld = galleryCounter;\n       \t    \twhile(galleryCounterOld == galleryCounter){\n     \t    \t\tgalleryCounter = Math.floor(Math.random() * images.length );\n       \t    \t}\n     \t    '
        else:
            jsChooseNext = '\n     \t    \tgalleryCounter++;\n  \t\t\t\tgalleryCounter %= images.length;\n     \t    '
        return '\n<script type="text/javascript">\n%s;\n%s;\n' % (imagesList, imagesDescList) + (' \n%s\n\nfunction slideSwitch() {\n    var $slideshow = $(\'#slideshow\');\n    var $slideshow_desc = $(\'#slideshow-desc\');\n\n    %s\n    \n    $slideshow.animate({opacity : 0.0}, %d, function() {\n    \t$slideshow_desc.html(\'&nbsp;\');\n        $slideshow.css(\'background-image\' , \'url(\'+images[galleryCounter]+\')\');\n          $slideshow.animate({opacity : 1.0}, %d);\n          $slideshow_desc.html(\'&nbsp;\'+descs[galleryCounter]);\n        });\n}\n\n$(\'#slideshow-desc\').html(\'&nbsp;\'+\'%s\');\nsetInterval( "slideSwitch()", %d );\n</script> ' % (jsInitCounter, jsChooseNext, self.data.anim_steps, self.data.anim_steps, firstImgDesc, self.data.anim_interval)).replace('$', self.data.jquery_symbol).replace('slideshow', id).replace('slideSwitch', id).replace('galleryCounter', 'counter' + id).replace('images', 'images' + id).replace('descs', 'imagesDesc' + id)

    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = self.data.count
        state = self.data.state
        query = {'portal_type': self.data.image_types}
        if len(state) > 0:
            query['review_state'] = state
        query['path'] = self.data.paths.split('\n')
        query['sort_on'] = 'Date'
        query['sort_order'] = 'reverse'
        if limit:
            result = catalog(query)[:limit]
        else:
            result = catalog(query)
        return result


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IGalleryPortlet)
    label = _('Add Gallery Portlet')
    description = _('This portlet presents dynamic gallery based on query.')

    def create(self, data):
        return Assignment(name=data.get('name', ''), width=data.get('width', 0), height=data.get('height', 128), omit_border=data.get('omit_border', False), display_desc=data.get('display_desc', True), desc_font_size=data.get('desc_font_size', '7px'), desc_font_color=data.get('desc_font_color', '#CCCCCC'), desc_height=data.get('desc_height', '15px'), count=data.get('count', 5), shuffle=data.get('shuffle', True), image_types=data.get('image_types', ('Image', )), state=data.get('state', ()), paths=data.get('paths', '/'), div_id='slideshow' + str(random.randrange(0, 10001)), image_size=data.get('image_size', 'thumb'), anim_interval=data.get('anim_interval', 5000), anim_steps=data.get('anim_steps', 500), jquery_symbol=data.get('jquery_symbol', 'jq'))


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(IGalleryPortlet)
    label = _('Edit Gallery Portlet')
    description = _('This portlet presents dynamic gallery.')