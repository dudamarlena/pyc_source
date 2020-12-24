# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/editor/management/commands/brokenlinks.py
# Compiled at: 2012-02-14 23:34:00
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os.path, urllib2
from booki.editor import models
from lxml import etree, html
from django.test import Client
cacheLinks = {}

class HeadRequest(urllib2.Request):

    def get_method(self):
        return 'HEAD'


def checkLink(options, chapter, urlLink):
    global cacheLinks
    if urlLink.startswith('http://'):
        if options['no_remote']:
            return
        for hostUrl in options['ignore_url']:
            if urlLink.startswith(hostUrl):
                return

        print '   >>> ', urlLink,
        if cacheLinks.get(urlLink):
            returnCode = cacheLinks.get(urlLink)
        else:
            try:
                response = urllib2.urlopen(HeadRequest(urlLink))
            except IOError as e:
                if hasattr(e, 'reason'):
                    returnCode = e.reason
                elif hasattr(e, 'code'):
                    returnCode = e.code

            returnCode = response.code
        if not options['no_cache']:
            cacheLinks[urlLink] = returnCode
        print '  [%s]' % returnCode
    else:
        if options['no_local']:
            return
        c = Client()
        newUrl = os.path.normpath('/%s/_v/%s/%s/%s' % (chapter.version.book.url_title, chapter.version.getVersion(), chapter.url_title, urlLink))
        print '    >> ', newUrl,
        response = c.get(newUrl)
        print '   [%s]' % response.status_code


class Command(BaseCommand):
    args = '<book name> [, <book name>, ...]'
    help = 'Check links in books.'
    option_list = BaseCommand.option_list + (
     make_option('--no-remote', action='store_true', dest='no_remote', default=False, help='Do we check for remote links?'),
     make_option('--no-local', action='store_true', dest='no_local', default=False, help='Do we check for local links?'),
     make_option('--no-cache', action='store_true', dest='no_cache', default=False, help='Do not cache network links.'),
     make_option('--ignore-url', action='append', dest='ignore_url', default=[], help='What hosts to ignore, e.g. http://www.wikipedia.org/'))

    def handle(self, *args, **options):
        if len(args) > 0:
            booksList = models.Book.objects.filter(url_title__in=args).order_by('url_title')
        else:
            booksList = models.Book.objects.all().order_by('url_title')
        for book in booksList:
            print '[%s]' % book.url_title
            try:
                for chapter in models.Chapter.objects.filter(version__book=book):
                    print '  [%s]' % chapter.url_title,
                    try:
                        tree = html.document_fromstring(chapter.content)
                        print ''
                    except:
                        print '   [ERROR PARSING HTML]'
                        continue

                    for elem in tree.iter():
                        src = elem.get('src')
                        if src:
                            checkLink(options, chapter, src)
                        href = elem.get('href')
                        if href:
                            checkLink(options, chapter, href)

            except:
                pass