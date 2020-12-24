# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Crawler.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 5583 bytes
import re, sys, urllib.error
from bs4 import BeautifulSoup
from xsrfprobe.modules import Parser
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import *
from xsrfprobe.files.dcodelist import *
from xsrfprobe.core.request import Get
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.logger import ErrorLogger
from xsrfprobe.files.discovered import INTERNAL_URLS

class Handler:
    __doc__ = '\n    This is a crawler that is used to fetch all the Urls\n        associated to the HTML page, and susequently\n            crawl them and build checks for CSRFs.\n    '

    def __init__(self, start, opener):
        self.visited = []
        self.toVisit = []
        self.uriPatterns = []
        self.currentURI = ''
        self.opener = opener
        self.toVisit.append(start)

    def __next__(self):
        self.currentURI = self.toVisit[0]
        self.toVisit.remove(self.currentURI)
        return self.currentURI

    def getVisited(self):
        return self.visited

    def getToVisit(self):
        return self.toVisit

    def noinit(self):
        if self.toVisit:
            return True
        else:
            return False

    def addToVisit(self, Parser):
        self.toVisit.append(Parser)

    def process(self, root):
        if EXCLUDE_DIRS:
            for link in EXCLUDE_DIRS:
                self.toVisit.remove(link)

        else:
            url = self.currentURI
            try:
                query = Get(url)
                if query != None:
                    if not str(query.status_code).startswith('40'):
                        INTERNAL_URLS.append(url)
                if url in self.toVisit:
                    self.toVisit.remove(url)
            except (urllib.error.HTTPError, urllib.error.URLError) as msg:
                verbout(R, 'HTTP Request Error: ' + msg.__str__())
                ErrorLogger(url, msg.__str__())
                if url in self.toVisit:
                    self.toVisit.remove(url)
                return

            if not query or not re.search('html', query.headers['Content-Type']):
                return
            verbout(GR, 'Making request to new location...')
            if hasattr(query.headers, 'Location'):
                url = query.headers['Location']
        verbout(O, 'Reading response...')
        response = query.content
        try:
            verbout(O, 'Trying to parse response...')
            soup = BeautifulSoup(response)
        except HTMLParser.HTMLParseError:
            verbout(R, 'BeautifulSoup Error: ' + url)
            self.visited.append(url)
            if url in self.toVisit:
                self.toVisit.remove(url)
            return
        else:
            for m in soup.findAll('a', href=True):
                app = ''
                if not re.match('javascript:', m['href']) or re.match('http://', m['href']):
                    app = Parser.buildUrl(url, m['href'])
                if app != '' and re.search(root, app):
                    while re.search(RID_DOUBLE, app):
                        p = re.compile(RID_COMPILE)
                        app = p.sub('/', app)

                    p = re.compile(RID_SINGLE)
                    app = p.sub('', app)
                    uriPattern = removeIDs(app)
                    if self.notExist(uriPattern) and app != url:
                        verbout(G, 'Added :> ' + color.BLUE + app)
                        self.toVisit.append(app)
                        self.uriPatterns.append(uriPattern)

            self.visited.append(url)
            return soup

    def getUriPatterns(self):
        return self.uriPatterns

    def notExist(self, test):
        if test not in self.uriPatterns:
            return 1
        else:
            return 0

    def addUriPatterns(self, Parser):
        self.uriPatterns.append(Parser)

    def addVisited(self, Parser):
        self.visited.append(Parser)


def removeIDs(Parser):
    """
    This function removes the Numbers from the Urls
                    which are built.
    """
    p = re.compile(NUM_SUB)
    Parser = p.sub('=', Parser)
    p = re.compile(NUM_COM)
    Parser = p.sub('\\1', Parser)
    return Parser