# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\browser\utils.py
# Compiled at: 2008-10-12 05:15:37
from Acquisition import aq_inner
import DateTime
from App.Common import rfc1123_date
from OFS.Image import Image as OFSImage
from zope.interface import implements
from Products.Five import BrowserView
from zope.app.component.hooks import getSite
from StringIO import StringIO
from Products.CMFPlone.utils import getToolByName, base_hasattr
from plone.memoize.instance import memoize
from interfaces import IThreeColorsThemedynamicImages
HAS_PIL = True
try:
    from PIL import Image as PILImage
    from PIL import ImagePalette
except:
    HAS_PIL = False

def _hexColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#':
        colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, 'input #%s is not in #RRGGBB format' % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    (r, g, b) = [ int(n, 16) for n in (r, g, b) ]
    return (
     r, g, b)


class ThreeColorsThemedynamicImages(BrowserView):
    """ 3 colors theme Dynamic Images  """
    __module__ = __name__
    implements(IThreeColorsThemedynamicImages)

    def getIconsColor(self):
        """
        Render some colors of a phantasy skin
        used to change icons color
        """
        context = aq_inner(self.context)
        if base_hasattr(context, 'getLeadingColor'):
            leadingColor = context.getLeadingColor()
            lightColor1 = context.getLightColor1()
            lightColor2 = context.getLightColor2()
        else:
            bp = context.base_properties
            if bp.hasProperty('leadingColor'):
                leadingColor = bp.getProperty('leadingColor')
                lightColor1 = bp.getProperty('lightColor1')
                lightColor2 = bp.getProperty('lightColor2')
            else:
                leadingColor = bp.getProperty('linkColor')
                lightColor1 = bp.getProperty('globalBorderColor')
                lightColor2 = bp.getProperty('contentViewBackgroundColor')
        return (leadingColor, lightColor1, lightColor2)

    def getCollapsedIcon(self):
        """
        Icon rendered in phantasyskin context
        """
        color = self.getIconsColor()[1]
        return self._changePaletteImage(imageId='base-collapsed-icon.gif', hexcolor=color)

    def getExpandedIcon(self):
        """
        Icon rendered in phantasyskin context
        """
        color = self.getIconsColor()[0]
        return self._changePaletteImage(imageId='base-expanded-icon.gif', hexcolor=color)

    def _getImageFromSkin(self, imageId):
        """
        Returns the image stored in skin   
        or stored at portal root 
        """
        portal = getSite()
        context = aq_inner(self.context)
        if base_hasattr(context, imageId):
            image = getattr(context, imageId)
            return PILImage.open(StringIO(image.data))
        elif base_hasattr(portal, imageId):
            image = getattr(portal, imageId)
            return PILImage.open(StringIO(image._data))

    def _changePaletteImage(self, imageId='', hexcolor=None, isFirstColor=True):
        """Change an image colour
           very simple (no anti alias)
           palette with 2 colors
           TODO (but not by me :-)) : change all colours from a monochrome image 
        """
        context = aq_inner(self.context)
        request = self.request
        response = request.RESPONSE
        if not imageId:
            return ''
        if not hexcolor:
            return response.redirect('%s/%s' % (context.portal_url(), imageId))
        if not HAS_PIL:
            return response.redirect('%s/%s' % (context.portal_url(), imageId))
        image = self._getImageFromSkin(imageId)
        pal = []
        if not isFirstColor:
            pal += [255, 255, 255]
            iTr = 0
        pal += _hexColorToRGB(hexcolor)
        if isFirstColor:
            pal += [255, 255, 255]
            iTr = 1
        image.putpalette(pal)
        sup_file = StringIO()
        image.save(sup_file, 'GIF', version='GIF89a', transparency=iTr)
        thumb = OFSImage('thumb', 'thumb', sup_file, content_type='image/gif')
        sup_file.seek(0)
        duration = 20
        seconds = float(duration) * 24.0 * 3600.0
        response.setHeader('Expires', rfc1123_date((DateTime.DateTime() + duration).timeTime()))
        response.setHeader('Cache-Control', 'max-age=%d' % int(seconds))
        return thumb.index_html(request, response)