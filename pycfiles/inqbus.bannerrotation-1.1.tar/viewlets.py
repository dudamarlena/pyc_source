# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/development/checkouts/inqbus.bannerrotation/inqbus/bannerrotation/browser/viewlets.py
# Compiled at: 2011-04-29 09:06:21
from zope.site.hooks import getSite
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.viewlets.common import ViewletBase
from AccessControl.unauthorized import Unauthorized
import random

class BannerViewlet(ViewletBase):
    """This simple viewlet should be shown next to
    the logo and contains a banner-picture
    """
    render = ViewPageTemplateFile('banner.pt')

    def update(self):
        """
        """
        self.firstimage = None
        self.get_properties()
        self.active_banners_folder = self.get_active_banners_folder()
        self.bannerimages = []
        (self.bannerimages, self.firstimage) = self.get_banner_images()
        return

    def get_properties(self):
        """ Extract the propertievalues out of the bannerrotation_properties.
        
        self.effect is a string, containing the pic-changing-effect. Possible
        effects are blindX, blindY, blindZ, cover, curtainX, curtainY, fade,
        fadeZoom, growX growY, none, scrollUp, scrollDown, scrollLeft
        scrollRight, scrollHorz, scrollVert, shuffle, slideX, slideY, toss
        turnUp, turnDown, turnLeft, turnRight, uncover, wipe and zoom.
        Default is fade
        
        self.timeout is an int, representing the time between the picturechanges 
        in milliseconds(default is 6000).
        
        self.speed is an int, which stays for the duration of the effect in 
        milliseconds(default is 1000).
        
        self.random is a boolean. True for random, false for sequence.
        
        self.banner_source_id is a string. Its the id of the folder, which holds the
        pictures for the banner. Default is banners.
        """
        portal = getSite()
        ptool = portal.portal_properties
        self.effect = ptool.bannerrotation_properties.effect
        self.timeout = ptool.bannerrotation_properties.timeout
        self.speed = ptool.bannerrotation_properties.speed
        self.enabled = ptool.bannerrotation_properties.enabled
        if ptool.bannerrotation_properties.random:
            self.random = 1
        else:
            self.random = 0
        self.banner_source_id = ptool.bannerrotation_properties.banner_source_id

    def get_active_banners_folder(self):
        """
        """
        try:
            banners_folder = self.context.restrictedTraverse(self.banner_source_id)
        except AttributeError:
            return
        except KeyError:
            return
        except Unauthorized:
            return

        return banners_folder

    def get_banner_images(self):
        """
        """
        bannerimages = []
        firstimage = None
        if self.active_banners_folder:
            images = self.active_banners_folder.objectValues()
            bannerimages = [ image.absolute_url() for image in images if image.portal_type == 'Image' ]
            if not bannerimages and ISiteRoot.providedBy(self.active_banners_folder.aq_inner.aq_parent):
                return self.get_default_banner_images()
        else:
            return self.get_default_banner_images()
        if self.random:
            firstimage = bannerimages.pop(random.randint(0, len(bannerimages) - 1))
        elif bannerimages:
            firstimage = bannerimages.pop(0)
        return (
         bannerimages, firstimage)

    def get_default_banner_images(self):
        """
        """
        url = self.context.absolute_url()
        firstimage = url + '/++resource++inqbus.bannerrotation.images/' + 'inqbus.bannerrotations.dummy01.png'
        bannerimages = [
         url + '/++resource++inqbus.bannerrotation.images/' + 'inqbus.bannerrotations.dummy02.png',
         url + '/++resource++inqbus.bannerrotation.images/' + 'inqbus.bannerrotations.dummy03.png',
         url + '/++resource++inqbus.bannerrotation.images/' + 'inqbus.bannerrotations.dummy04.png']
        return (bannerimages, firstimage)

    def get_cycle_script(self):
        """
        """
        javascript = '<script type="text/javascript">\n  jq(document).ready(\n    function() {\n      for (url in bannerimages) {\n        jq(\'.bannerrotation\').append(\'<img src="\'+bannerimages[url]+\'" />\');\n      }\n      jq(\'.bannerrotation\').cycle({\n        fx: \'%(fx)s\',\n        timeout: %(timeout)s,\n        speed: %(speed)s,\n        random: %(random)s\n      })\n    }\n  );\n</script>        \n'
        returnvalue = javascript % {'fx': self.effect, 
           'timeout': self.timeout, 
           'speed': self.speed, 
           'random': self.random}
        return returnvalue

    def get_banner_array(self):
        """
        """
        javascript = '<script type="text/javascript">\n  bannerimages = new Array(%s);\n</script>\n'
        url_script_strings = ''
        for imageurl in self.bannerimages:
            url_script_strings = url_script_strings + '"' + imageurl + '"'
            if not imageurl == self.bannerimages[(-1)]:
                url_script_strings = url_script_strings + ', '

        return javascript % url_script_strings

    def load_jq_cycle(self):
        """
        """
        return self.context.absolute_url() + '/++resource++inqbus.bannerrotation.scripts/jq_cycle.js'