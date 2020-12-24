# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/content/external.py
# Compiled at: 2018-10-18 17:35:13
from plone.dexterity.content import Item
from zope.interface import implementer
from zope.interface import Interface

def has_image(blog_entry):
    image = blog_entry.image
    return image and image.getSize()


class IExternalContent(Interface):
    """ Um conteudo externo a este site
    """


@implementer(IExternalContent)
class ExternalContent(Item):

    def image_thumb(self):
        """ Return a thumbnail """
        if not has_image(self):
            return None
        else:
            view = self.unrestrictedTraverse('@@images')
            return view.scale(fieldname='image', scale='thumb').index_html()

    def tag(self, scale='thumb', css_class='tileImage', **kw):
        """ Return a tag to the image """
        if not has_image(self):
            return ''
        view = self.unrestrictedTraverse('@@images')
        return view.tag(fieldname='image', scale=scale, css_class=css_class, **kw)