# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/themecustomizer/src/collective/themecustomizer/browser/viewlets.py
# Compiled at: 2014-01-16 18:43:07
from plone import api
from plone.app.layout.viewlets.common import LogoViewlet as BaseViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class LogoViewlet(BaseViewlet):
    """ Custom plone.logo viewlet to show/hide logo image and
    site title and description
    """
    index = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()
        portal = api.portal.get()
        self.navigation_root_title = self.portal_state.navigation_root_title()
        logoTitle = self.portal_state.portal_title()
        if portal.get('logo.png'):
            self.logo_tag = portal.get('logo.png').tag(title=logoTitle, alt=logoTitle)
        else:
            bprops = portal.restrictedTraverse('base_properties', None)
            if bprops is not None:
                logoName = bprops.logoName
            else:
                logoName = 'logo.jpg'
            self.logo_tag = portal.restrictedTraverse(logoName).tag(title=logoTitle, alt=logoTitle)
        return

    def show_logo(self):
        """Return the value of the 'show_header_logo' site property.
        """
        portal_properties = api.portal.get_tool('portal_properties')
        site_properties = portal_properties.site_properties
        return getattr(site_properties, 'show_header_logo', True)

    def show_portal_title(self):
        """Return the value of the 'show_header_text' site property.
        """
        portal_properties = api.portal.get_tool('portal_properties')
        site_properties = portal_properties.site_properties
        return getattr(site_properties, 'show_header_text', False)

    def get_portal_title(self):
        """Return portal title.
        """
        return api.portal.get().title

    def get_portal_description(self):
        """Return portal description.
        """
        return api.portal.get().description


class HeaderViewlet(BaseViewlet):
    """ Custom plone.header viewlet to show/hide background image
    """

    def logo_background_style(self):
        portal = api.portal.get()
        if portal.get('background.png'):
            return 'background-image: url(' + portal.absolute_url() + '/background.png)'
        return ''