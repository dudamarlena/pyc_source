# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/browser/jsslot.py
# Compiled at: 2008-10-10 10:13:59
"""
Javascript slot viewlet
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import os, simplejson
from zope.component import getMultiAdapter
from zope.component import getAdapter
from zope.component import queryAdapter
from Acquisition import aq_inner
from Globals import DTMLFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFPlone.utils import getSiteEncoding
from iw.sitestat.interfaces import ISitestatConfigSchema
from iw.sitestat.interfaces import IFileLinksFinder
from iw.sitestat.interfaces import IContentOptions
from iw.sitestat.utils import getSite, sitestatifyTitle
from iw.sitestat.config import ZOPETESTCASE

class SitestatViewlet(ViewletBase):
    """Base viewlet - must be subclassed"""
    __module__ = __name__

    def update(self):
        """Callback for viewlets manager"""
        super(SitestatViewlet, self).update()
        self.context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        self.global_config = getAdapter(getSite(), ISitestatConfigSchema)
        self.local_config = queryAdapter(self.context, IContentOptions)

    def enabled(self):
        """Check conditions to provide the JS slot"""
        if not ZOPETESTCASE and not self.context_state.is_view_template():
            return False
        if not self.global_config.sitestat_enabled:
            return False
        return True

    def sitestatBaseURL(self):
        """Make sitestat server base URL from config"""
        gc = self.global_config
        private_url = gc.sitestat_private_url
        if private_url:
            private_url = private_url.strip()
            if not private_url.endswith('/'):
                private_url += '/'
            return private_url
        if self.request.URL.startswith('https') and gc.https_enabled:
            protocol = 'https'
        else:
            protocol = 'http'
        template = '%s://%s.sitestat.com/%s/%s/'
        return template % (protocol, gc.country_code, gc.company_code, gc.site_code)

    def getCounters(self):
        """Sitestat formatted counters"""
        if self.local_config.override_counters:
            counters = self.local_config.counters
        else:
            context = aq_inner(self.context)
            encoding = getSiteEncoding(context)
            if self.global_config.counter_name_mode == 'id':
                portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
                root_url = portal_state.navigation_root_url()
                this_url = context.absolute_url()
                path = this_url[len(root_url):].split('/')
                counters = [ x for x in path if x != '' ]
            else:
                breadcrumbs_view = getMultiAdapter((context, self.request), name='breadcrumbs_view')
                breadcrumbs = breadcrumbs_view.breadcrumbs()
                counters = [ sitestatifyTitle(b['Title'].strip(), encoding) for b in breadcrumbs ]
            counters = ('.').join(counters)
        return counters

    def standardCodeURL(self):
        """Standard code URL, for standard measure code."""
        code = '%ss?%s' % (self.sitestatBaseURL(), self.getCounters())
        labels = self.local_config.labels
        if len(self.local_config.labels) > 0:
            code += '&amp;' + ('&amp;').join(labels)
        return code


class JSSlotStartViewlet(SitestatViewlet):
    """To be placed immediately after <head>"""
    __module__ = __name__

    def index(self):
        if self.enabled():
            if self.global_config.dltime_enabled:
                out = '<!-- Begin Sitestat4 Loadingtime1 code -->\n<script language="JavaScript1.1" type="text/javascript">ns_loadingtime1=(new Date()).getTime()</script>\n<!-- End Sitestat4 Loadingtime1 code -->\n'
            else:
                out = ''
            out += '<link rel="SHORTCUT ICON" href="%s&amp;ns_class=bookmark" />\n' % self.standardCodeURL()
            return out
        else:
            return ''


_templatesdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
jsslotend_template = DTMLFile('sitestatinline.js', _templatesdir)

class JSSlotEndViewlet(SitestatViewlet):
    """To be placed immediately before </body>"""
    __module__ = __name__

    def listPdfURLs(self):
        """URLs to be marked as PDF files"""
        context = aq_inner(self.context)
        gc = self.global_config
        if not gc.pdf_marking:
            return []
        file_links_finder = queryAdapter(context, IFileLinksFinder)
        if file_links_finder is not None:
            pdf_file_urls = file_links_finder.pdfFileURLs()
            if gc.files_as_pdf:
                pdf_file_urls.extend(file_links_finder.fileURLs())
        else:
            pdf_file_urls = []
        return pdf_file_urls

    def listClickinURLs(self):
        """We transform paths to URLs"""
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        portal_url = portal_state.portal_url()
        if not portal_url.endswith('/'):
            portal_url += '/'
        return [ portal_url + p for p in self.global_config.clickin_paths ]

    def index(self):
        """Render hook"""
        if not self.enabled():
            return ''
        template = jsslotend_template.__of__(self.context)
        return template(standard_code_url=simplejson.dumps(self.standardCodeURL()), render_dl_time=self.global_config.dltime_enabled, pdf_file_urls=simplejson.dumps(self.listPdfURLs()), clickin_urls=simplejson.dumps(self.listClickinURLs()), clickout_urls=simplejson.dumps(self.global_config.clickout_urls))