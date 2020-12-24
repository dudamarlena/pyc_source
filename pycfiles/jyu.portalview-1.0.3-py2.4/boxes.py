# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/jyu/portalview/browser/boxes/boxes.py
# Compiled at: 2009-11-16 03:44:25
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
try:
    from vice.outbound.interfaces import IFeedConfigs, IFeedSettings
    from vice.outbound.feedformats.interfaces import IFeedFormats
    from zope.component import getUtility
    vice_exists = True
except:
    vice_exists = False

import urlparse, string, re
SRC_REGEXP = re.compile('src="([^"]*)"')
HREF_REGEXP = re.compile('href="([^"]*)"')
SWF_REGEXP = re.compile("SWFObject\\('([^']*)'")
RESOLVEUID_REGEXP = re.compile('[^"]*(?P<uid>resolveuid/[^/"#? ]*)')
UID_REGEXP = re.compile('[^"]*resolveuid/(?P<uid>[^/"#? ]*)')

class ATCTBoxView(BrowserView):
    __module__ = __name__
    __call__ = ViewPageTemplateFile('atct_boxview.pt')

    @staticmethod
    def relativeURL(source, target):
        """ Creates a relative URL given to absolute URLs
        (c) May 2002 Thomas Guettler http://www.thomas-guettler.de
        This code is in the public domain
        http://guettli.sourceforge.net/gthumpy/src/relative_url.py
        """
        su = urlparse.urlparse(source)
        tu = urlparse.urlparse(target)
        junk = tu[3:]
        if su[0] != tu[0] or su[1] != tu[1]:
            return target
        su = re.split('/', su[2])
        tu = re.split('/', tu[2])
        su.reverse()
        tu.reverse()
        while len(su) > 0 and len(tu) > 0 and su[(-1)] == tu[(-1)]:
            su.pop()
            last_pop = tu.pop()

        if len(su) == 0 and len(tu) == 0:
            tu.append(last_pop)
        if len(su) == 1 and su[0] == '' and len(tu) == 0:
            su.append(last_pop)
            tu.append(last_pop)
        tu.reverse()
        relative_url = []
        for i in range(len(su) - 1):
            relative_url.append('..')

        rel_url = string.join(relative_url + tu, '/')
        rel_url = urlparse.urlunparse(['', '', rel_url, junk[0], junk[1], junk[2]])
        return rel_url

    @staticmethod
    def fixRelativeURLs(html, request_url, context_url):
        base = ATCTBoxView.relativeURL(request_url, context_url)
        for path in SRC_REGEXP.findall(html):
            html = html.replace('src="%(path)s"' % vars(), 'src="%s"' % urlparse.urljoin(base, path))

        for path in HREF_REGEXP.findall(html):
            html = html.replace('href="%(path)s"' % vars(), 'href="%s"' % urlparse.urljoin(base, path))

        for path in SWF_REGEXP.findall(html):
            html = html.replace("SWFObject('%(path)s'" % vars(), "SWFObject('%s'" % urlparse.urljoin(base, path))

        return html

    @property
    def language(self):
        tool = getToolByName(self.context, 'portal_languages')
        return tool.getPreferredLanguage()

    def resolveUIDs(self, html):
        rc = getToolByName(self.context, 'reference_catalog')
        for resolveuid in RESOLVEUID_REGEXP.findall(html):
            uid = UID_REGEXP.findall(resolveuid)[0]
            obj = rc.lookupObject(uid)
            relative_url = ATCTBoxView.relativeURL(self.context.absolute_url(), obj.absolute_url())
            html = html.replace(resolveuid, relative_url)

        return html

    def toLocalizedTime(self, time, long_format=None, time_only=None):
        """Convert time to localized time
        """
        context = aq_inner(self.context)
        util = getToolByName(context, 'translation_service')
        if self.language == 'fi':
            s = util.ulocalized_time(time, long_format, time_only, context=context, domain='jyu.portalview.plonelocales', request=self.request)
            return s and s.strip() or None
        else:
            s = util.ulocalized_time(time, long_format, time_only, context=context, domain='plonelocales', request=self.request)
            return s and s.strip() or None
        return


class ATCTDocumentBoxView(ATCTBoxView):
    __module__ = __name__
    __call__ = ViewPageTemplateFile('atct_document_boxview.pt')

    def __init__(self, context, request):
        """ Sets up a few convenience object attributes """
        self.context = context
        self.request = request

    def getText(self, text=None):
        """ Returns document text with fixed urls. """
        text = text or self.context.getText()
        text = self.resolveUIDs(text)
        return ATCTBoxView.fixRelativeURLs(text, self.request.getURL(), self.context.absolute_url())

    def getRawText(self):
        """ Returns document text with fixed urls. """
        return self.getText(text=self.context.getRawText())


class ATCTTopicBoxView(ATCTBoxView):
    __module__ = __name__
    __call__ = ViewPageTemplateFile('atct_topic_boxview.pt')

    @property
    def moreUrl(self):
        hrefs = HREF_REGEXP.findall(self.resolveUIDs(self.context.getText()))
        if hrefs:
            base = ATCTBoxView.relativeURL(self.request.getURL(), self.context.absolute_url())
            return urlparse.urljoin(base, hrefs[0])
        else:
            return
        return

    def queryCatalog(self):
        try:
            subtopics = self.context.getFolderContents()
        except:
            subtopics = []

        if subtopics:
            brains = [ brain for brain in self.context.queryCatalog() ]
            for topic in subtopics:
                try:
                    brains.extend(topic.getObject().queryCatalog())
                except:
                    continue

            UIDs = []
            uniq = []
            for brain in brains:
                if not UIDs.count(brain.UID):
                    UIDs.append(brain.UID)
                    uniq.append(brain)

            if self.context.getLimitNumber():
                return uniq[:self.context.getItemCount()]
            return uniq
        else:
            return self.context.queryCatalog()

    def toRelativeUrl(self, path):
        absolute = ('/').join(self.context.getPhysicalPath())
        relative = ATCTBoxView.relativeURL(self.request.getURL(), self.context.absolute_url())
        base = absolute[:absolute.find(relative)]
        return ATCTBoxView.relativeURL(base, path)

    def getFeeds(self):
        if not vice_exists:
            return []
        global_settings = getUtility(IFeedSettings)
        if not global_settings.enabled:
            return []
        base = ATCTBoxView.relativeURL(self.request.getURL(), self.context.absolute_url())
        base = base + '/'
        local_settings = IFeedConfigs(self.context)
        if not local_settings.enabled:
            return [{'url': '%(base)sRSS' % vars()}]
        configs = local_settings.configs
        feeds = [ {'name': c.name, 'format_view': c.format, 'id': c.id(), 'published_url': c.published_url} for c in configs if c.enabled ]
        for f in feeds:
            if f['published_url']:
                if settings.published_url_enabled:
                    f['url'] = f['published_url']
                else:
                    f['url'] = '%s/%s' % (f['format_view'], f['id'])
            else:
                f['url'] = '%s/%s' % (f['format_view'], f['id'])
            f['url'] = urlparse.urljoin(base, f['url'])
            del f['published_url']
            del f['format_view']
            del f['id']

        return feeds

    @property
    def feedlink(self):
        feeds = self.getFeeds()
        if feeds:
            return feeds[0]['url']
        else:
            return
        return