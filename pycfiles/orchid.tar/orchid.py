# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pesachzon/workspace/crawler/orchid/orchid.py
# Compiled at: 2005-12-13 08:18:07
"""
This package is a multi-threaded generic web crawler. 
For more detail about the package please see the attached paper.
"""
import os, urlparse, urllib2, robotparser
from threading import *
import re
from BeautifulSoup import BeautifulSoup
import logging, socket
from time import sleep
from random import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename='ugrah.log', filemode='w')

class NaiveAnalyzer(Thread):
    """
    This is an interface for the analyzers. To use the Ugrah crawler
    subclass this class with you logic of analyzing the gathered
    data and choosing which links to crawl.
    """
    __module__ = __name__

    def __init__(self, linksToFetchAndCond, siteQueueAndCond, db):
        """
        Creates a new analyzer. There can be as many analyzers as you like,
        depending on the type of processing of data you wish to do.
        @param linksToFetchAndCond: A tuple of the form (map, Condition) where the map
        is the map of domains to links to be fetched (which is updated by the analyzer)
        and the condition is a L{threading.Condition} object which is used to synchronize
        access to the list.
        @param siteQueueAndCond: A tuple (siteQueue, siteCond). The siteQueue is a queue
        unto which new sites (with their links) are inserted. The siteCond is a Condition
        object used to lock the queue and signal the analyzer to wake up.
        @param db: a tuple of the form (siteDb, siteDbLock) where the linkDb
        is the global link database, siteDb is the global site database and the lock
        is used to synchronize access to both of these databases.
        """
        Thread.__init__(self)
        self.linksToFetch = linksToFetchAndCond
        self.db = db
        self.siteQueueAndCond = siteQueueAndCond
        self.__stopCondition = False
        self.__scl = Lock()
        if not self.db[0].has_key('crawled'):
            self.db[0]['crawled'] = {}
        if not self.db[0].has_key('sites'):
            self.db[0]['sites'] = {}
        self.__sitesProcessed = 0

    def setStopCondition(self, val):
        """
        Sets the stop condition to the specified value. Should be True to stop
        the analyzer thread.
        """
        self.__scl.acquire()
        self.__stopCondition = val
        self.__scl.release()

    def getNumSitesProcessed(self):
        """
        Returns the number of sites this analyzer has processed
        """
        return self.__sitesProcessed

    def run(self):
        """
        Performs the main function of the analyzer. In this case,
        just adds all the hyperlinks to the toFetch queue.
        """
        (lfs, lfsCond) = self.linksToFetch
        (siteDb, dbLock) = self.db
        (siteQueue, siteQueueCond) = self.siteQueueAndCond
        self.__scl.acquire()
        siteQueueCond.acquire()
        while not self.__stopCondition or len(siteQueue) != 0:
            while len(siteQueue) == 0 and not self.__stopCondition:
                self.__scl.release()
                siteQueueCond.wait()
                self.__scl.acquire()

            if self.__stopCondition and len(siteQueue) == 0:
                break
            self.__scl.release()
            siteToProcess = siteQueue.pop()
            self.__sitesProcessed += 1
            siteQueueCond.release()
            dbLock.acquire()
            self.analyzeSite(siteDb, siteToProcess)
            dbLock.release()
            lfsCond.acquire()
            self.addSiteToFetchQueue(lfs)
            lfsCond.notify()
            lfsCond.release()
            self.__scl.acquire()
            siteQueueCond.acquire()

        self.__scl.release()
        siteQueueCond.release()

    def analyzeSite(self, db, site):
        """
        Processes the site and adds it to the db.
        Any real analyzer should override this method with it's
        own logic.
        """
        db['crawled'][site.stringUrl] = True
        self.__newLinksToCrawl = [ link for link in site.links['regular'] if not db['crawled'].has_key(link) ]
        tempList = []
        for l in self.__newLinksToCrawl:
            db['crawled'][l] = True
            if l not in tempList:
                tempList += [l]

        self.__newLinksToCrawl = tempList

    def addSiteToFetchQueue(self, lfs):
        """
        Adds links to the fetch queue. A real analyzer should override
        this method.
        """
        logging.debug('Adding to lfs')
        domMap = self.reorganizeByDomain(self.__newLinksToCrawl)
        for dom in domMap:
            if lfs.has_key(dom):
                lfs[dom] += domMap[dom]
            else:
                lfs[dom] = domMap[dom]

    def reorganizeByDomain(self, listOfLinks):
        """
        Returns a map which maps domain names to links inside the domain.
        """
        pLinks = [ urlparse.urlparse(l) for l in listOfLinks ]
        domMap = {}
        for l in pLinks:
            if domMap.has_key(l[1]):
                domMap[l[1]] += [urlparse.urlunparse(l)]
            else:
                domMap[l[1]] = [
                 urlparse.urlunparse(l)]

        return domMap

    def selectNextUrl(self):
        """
        Chooses the next url to crawl to. This implementation
        will select a random domain and then crawl to the first link 
        in that domain's queue.
        """
        toFetchQueue = self.linksToFetch[0]
        dom = toFetchQueue.keys()
        selectedDom = dom[randint(0, len(dom) - 1)]
        curUrl = toFetchQueue[selectedDom].pop()
        if len(toFetchQueue[selectedDom]) == 0:
            toFetchQueue.pop(selectedDom)
        return curUrl

    def report(self):
        """
        A real analyzer should override this method. Outputs the results
        of the analysis so far.
        """
        None
        return


class OrchidController(Thread):
    """
    This class is responsible for controlling the fetchers and distributing
    the work load.
    """
    __module__ = __name__

    def __init__(self, linksToFetch, siteQueueAndCond, analyzer, numFetchers=1, maxFetches=100, socketTimeOut=20, delay=5):
        """
        Creates a new controller. Typically you will need only one.
        @param linksToFetch: A tuple of the form (Dict, Condition) where the dict
        is the map of domains to links to be fetched (which is updated by the analyzer)
        and the condition is a L{threading.Condition} object which is used to synchronize
        access to the list.
        @param siteQueueAndCond: a tuple of the form (list, cond) where list is the site queue
        into which fetchers insert new sites that have been fetched. cond is a Condition
        object which is used to lock the queue.
        @param analyzer: The analyzer which we are using for analyzing crawled data.
        @param numFetchers: The number of active threads used for crawling.
        @param maxFetches: Maximum number of pages to crawl.
        @param socketTimeOut: The timeout to use for opening urls. 
        WARNING: the timeout is set using socket.setdefaulttimeout(..)
        which affects ALL the sockets in the multiverse.
        @param delay: The delay in seconds between assignments of urls to fetchers.
        """
        Thread.__init__(self)
        self.__linksToFetch = linksToFetch
        self.__db = siteQueueAndCond
        self.__maxFetches = maxFetches
        socket.setdefaulttimeout(socketTimeOut)
        self.__numFetches = 0
        self.__fetchers = []
        (siteQueue, siteQueueCond) = siteQueueAndCond
        for i in range(numFetchers):
            c = Condition()
            scl = Lock()
            f = OrchidFetcher(siteQueue, siteQueueCond, c, scl)
            self.__fetchers += [(f, c, scl)]

        self.__verificationMap = {}
        self.__delay = delay
        self.__analyzer = analyzer

    def getFetcherThreadUtilization(self):
        """
        Returns a list of number of urls each fetcher thread handler.
        """
        return [ ftuple[0].getUrlsCounter() for ftuple in self.__fetchers ]

    def getNumFetchersUsed(self):
        """
        Returns the number of fetchers that handled at least one url.
        """
        u = [ ftuple[0].getUrlsCounter() for ftuple in self.__fetchers ]
        counter = 0
        for x in u:
            if x > 0:
                counter += 1

        return counter

    def run(self):
        """
        Runs this controller thread. The controller will use it's
        fetchers to fill the links and sites databases.
        """
        logging.info('Starting the controller thread')
        for ftuple in self.__fetchers:
            ftuple[0].start()

        (toFetchQueue, toFetchCond) = self.__linksToFetch
        while self.__numFetches < self.__maxFetches:
            sleep(self.__delay)
            logging.debug('getting cond')
            toFetchCond.acquire()
            logging.debug('got cond')
            while len(toFetchQueue) == 0:
                logging.debug('waiting')
                toFetchCond.wait()

            logging.debug('done waiting')
            curUrl = self.__analyzer.selectNextUrl()
            if self.__verificationMap.has_key(curUrl):
                raise Exception, 'Duplicate URL [%s]' % curUrl
            else:
                self.__verificationMap[curUrl] = True
            logging.debug('Controller acquired URL: [%s]' % curUrl)
            toFetchCond.release()
            self.__numFetches += 1
            logging.info('Processed %d out of %d pages' % (self.__numFetches, self.__maxFetches))
            foundFreeFetcher = False
            while not foundFreeFetcher:
                for ftuple in self.__fetchers:
                    if ftuple[1].acquire(False):
                        if ftuple[0].isFree():
                            logging.debug('Controller found free fetcher')
                            ftuple[0].setUrl(curUrl)
                            ftuple[1].notify()
                            ftuple[1].release()
                            foundFreeFetcher = True
                            break
                        else:
                            ftuple[1].notify()
                            ftuple[1].release()

        self.__stopFetchers()
        logging.debug('Stopping controller, %d fetcher threads were useful.' % self.getNumFetchersUsed())

    def __stopFetchers(self):
        """
        Stops all the fetchers
        """
        logging.debug('Stopping fetchers')
        for ftuple in self.__fetchers:
            ftuple[2].acquire()
            ftuple[0].setStopCondition(True)
            ftuple[2].release()
            ftuple[1].acquire()
            ftuple[1].notify()
            ftuple[1].release()
            ftuple[0].join()


class OrchidFetcher(Thread):
    """
    This class is responsible for fetching url contents, processing them
    with UgrahExtractor and updating the site and link database.
    """
    __module__ = __name__

    def __init__(self, siteQueue, siteQueueCond, fetcherCondition, stopConditionLock):
        """
        Creates a new fetcher thread (not started) with the following
        @param siteQueue: the site queue from which the analyzer takes sites
        to analyze.
        @param siteQueueCond: A Condition object used to lock the siteQueue.
        @param fetcherCondition: a threading.Condition object which is used for
        communication between the fetcher and the controller: whenever
        a fetcher finishes working on it's assignment it calls 
        fetcherCondition.wait() and waits until the controller assigns
        a new url for it to fetch.
        @param stopConditionLock: a threading.Lock object which is used to lock
        the internal stop condition variable. A thread that wishes
        to change this variable should lock it first.
        """
        Thread.__init__(self)
        self.siteQueue = siteQueue
        self.condition = fetcherCondition
        self.siteQueueCond = siteQueueCond
        self.stopConditionLock = stopConditionLock
        self.stopCondition = False
        self.currentStringUrl = None
        self.urlHandler = UrlHandler()
        self.extractor = OrchidExtractor()
        self.handledUrlsCounter = 0
        return

    def setStopCondition(self, val):
        """ 
        Can receive either True or False. Set to Ture when the fetcher
        should stop working. WARNING: It's *necessary* to acquire the lock
        which was passed to the constructor as stopConditionLock before
        calling this method.
        """
        self.stopCondition = val

    def setUrl(self, stringUrl):
        """
        Sets the url that the fetcher should work on. It's *necessary*
        to acquire the condition instance which was passed to the constructor
        as fetcherCondition before calling this method and call notify afterwards
        """
        self.currentStringUrl = stringUrl

    def getUrlsCounter(self):
        """
        Returns the number of URLs this fetcher has handled.
        Should be called only AFTER the thread is dead.
        """
        return self.handledUrlsCounter

    def isFree(self):
        """
        Returns True if the fetcher hasn't been assigned a URL yet.
        """
        return self.currentStringUrl == None

    def run(self):
        """
        Performs the main function of the fetcher which is to fetch
        the contents of the url specified by setCurrentStringUrl.
        This method loops until the stop condition is set.
        """
        self.condition.acquire()
        self.stopConditionLock.acquire()
        while not self.stopCondition or self.currentStringUrl:
            while not self.currentStringUrl and not self.stopCondition:
                self.stopConditionLock.release()
                self.condition.wait()
                self.stopConditionLock.acquire()

            if self.stopCondition and not self.currentStringUrl:
                break
            else:
                self.stopConditionLock.release()
            self.handledUrlsCounter += 1
            try:
                self.__processSite()
                links = self.extractor.getLinks()
                parsedContent = self.extractor.getParsedContent()
                rawContent = self.extractor.getRawContent()
                s = Site(self.currentStringUrl, links, parsedContent, rawContent)
                self.__fileData(s, links)
                logging.info('URL processing succeeded: [%s]' % self.currentStringUrl)
            except Exception, e:
                logging.info('URL processing failed: [%s], error: %s' % (self.currentStringUrl, e))

            self.currentStringUrl = None
            self.stopConditionLock.acquire()

        self.condition.release()
        self.stopConditionLock.release()
        return

    def __fileData(self, s, links):
        """
        Stores the given site and links in the databases
        """
        self.siteQueueCond.acquire()
        self.siteQueue.insert(0, s)
        self.siteQueueCond.notify()
        self.siteQueueCond.release()

    def __processSite(self):
        """
        Fetches the url contents and creates a parsed structure
        """
        self.urlHandler.processUrl(self.currentStringUrl)
        content = self.urlHandler.getSite()
        self.extractor.setSite(self.currentStringUrl, content)
        self.extractor.extract()


class Site:
    """
    A class for representing the information that is collected for
    a specific site.
    """
    __module__ = __name__

    def __init__(self, stringUrl, links, parsedContent, rawContent):
        """
        Creates a new site. 
        @param stringUrl: the url of the site
        @param links: a map from link types to links which appear on this page
        @param parsedContent: BeautifulSoup instance which contains the parsed content
        of the page.
        @param rawContent: The raw content of the page as a string.
        """
        self.stringUrl = stringUrl
        self.links = links
        self.content = parsedContent
        self.rawContent = rawContent
        self.evilLinks = []
        self.evilness = 0
        self.matches = []


class OrchidExtractor:
    """
    A class responsible for parsing and analyzing html content and extracting
    various forms of links from it. The goal is to provide the user with a datastructure
    representing the parsed HTML and a set of links that appear on the given page.
    Supported links type are:
        1. simple <a href="...">link</a> type links (done)
        2. relative links
        3. BASE tag (done)
        4. LINK tag (done)
        5. FRAMESET links (done)
        6. IMG links (done)
        7. client side image maps (done)
        8. server side image maps (unsupported)
        9. Object links
        10. JavaScript links
        11. Meta refresh tags
        12. iframes
        13. form links
    """
    __module__ = __name__
    LINK_PATTERNS = [
     (
      'regular', re.compile('^[aA]$'), {'href': re.compile('.+')}, 'href'), ('base', re.compile('^(BASE)|(base)$'), {'href': re.compile('.+')}, 'href'), ('link', re.compile('^(LINK)|(link)$'), {'href': re.compile('.+')}, 'href'), ('frame', re.compile('^(FRAME)|(frame)$'), {'src': re.compile('.+')}, 'src'), ('area', re.compile('^(AREA)|(area)$'), {'href': re.compile('.+')}, 'href'), ('iframe', re.compile('^(IFRAME)|(iframe)$'), {'src': re.compile('.+')}, 'src'), ('script', re.compile('^(SCRIPT)|(script)$'), {'src': re.compile('.+')}, 'src'), ('image', re.compile('^(IMG)|(img)$'), {'src': re.compile('.+')}, 'src')]

    def __init__(self):
        """
        Creates a new link extractor. Should be followed by a call to setSite
        """
        self.stringUrl = None
        self.domain = None
        self.parsedContent = None
        self.rawContent = None
        self.links = {}
        return

    def setSite(self, stringUrl, content):
        """
        Sets the current site url and content for the extractor.
        @param stringUrl: The url of the site being analyzed.
        @param content: The html content of the site.
        """
        self.stringUrl = stringUrl
        preDomain = urlparse.urlparse(self.stringUrl)
        self.domain = urlparse.urlunparse((preDomain[0], preDomain[1], '', '', '', ''))
        self.links = {}
        fullContent = content.read()
        self.parsedContent = BeautifulSoup(fullContent)
        self.rawContent = fullContent

    def getParsedContent(self):
        """
        Returns the BeautifulSoup datastructure of the HTML of the
        site that was set using setSite .
        """
        return self.parsedContent

    def getRawContent(self):
        return self.rawContent

    def getLinks(self):
        """
        Returns a map from link type to a list of links of that type that appeared 
        in the page.
        """
        return self.links

    def extract(self):
        """
        Extracts all the links in the page according to the patterns
        specified in LINK_PATTERNS. The links are stored in 
        a map (link type -> url list) called links (accessible 
        by 'extractor.links' where extractor is an instance of HtmlLinkExtractor)
        """
        for p in self.LINK_PATTERNS:
            self.__extractLinks(*p)

    def __processRelativeLink(self, link):
        """
        Go over the links and see if any of them are relative (like '/about.html').
        When a relative link is found it is replaced by a full link 
        ('http://www.site.com/about.html').
        """
        relativePathRe = re.compile('/.*')
        if relativePathRe.match(link):
            link = self.domain + link
        elif urlparse.urlparse(link)[0] == '':
            link = self.domain + self.path + '/' + link
        return link

    def __extractLinks(self, type, tagPattern, attrPatternMap, urlAttr):
        """
        Extracts links with the specified configuration from the content
        and stores them in the appropriate list of links, according to their
        type.
        @param type: The type of the links to extract. This is also the key name
        under which the links will be added. 
        For example: 'regular', 'iframe'.
        @param tagPattern: a string or compiler regular expression which matches the names
        of the TAGS which contain the links. 
        For example: 'a', 'img', 'link'.
        @param attrPatternMap: A map of attribute names to strings or compiled regular 
        expressions. Only tags that have attribute that match the conditions
        in the map will be scanned for links.
        For example: {'href' : re.compile('.+')}
        @param urlAttr: The attribute from which the url of link should be extracted.
        For example: 'href', 'src'.
        """
        links = self.parsedContent.fetch(tagPattern, attrPatternMap)
        if not self.links.has_key(type):
            self.links[type] = []
        for l in links:
            try:
                self.links[type] += [urlparse.urljoin(self.stringUrl, l[urlAttr].strip())]
            except:
                None

        return


class UrlHandler:
    """
    A class responsible for parsing a url and retrieving it's contents.
    """
    __module__ = __name__

    def __init__(self):
        """
        A constructor for the url handler. Should be followed 
        by calls to setCurrentUrl and getSite.
        """
        self.robotParser = robotparser.RobotFileParser()
        self.currentSite = None
        return

    def processUrl(self, stringUrl):
        """
        Sets the url that the parser is working on.
        Raises an exception if we can't open it.
        """
        self.robotParser = robotparser.RobotFileParser()
        if not self.__canVisitSite(stringUrl):
            logging.info('access to [%s] was denied by robots.txt' % stringUrl)
            raise Exception, "robots.txt doesn't allow access to %s" % stringUrl
        req = self.__createRequest(stringUrl)
        site = urllib2.urlopen(req)
        if not site.headers.type == 'text/html' and not site.headers.type == 'application/x-javascript':
            logging.info('Url contained mime type which is not text/html: [%s]' % stringUrl)
            raise Exception, 'Not text/html mime type'
        logging.info('successfully opened %s' % stringUrl)
        self.currentSite = site

    def getSite(self):
        """
        Returns the url object which was opened by setCurrentUrl.
        The returned object acts just like a file object.
        """
        return self.currentSite

    def __createRequest(self, stringUrl):
        req = urllib2.Request(stringUrl)
        req.add_header('User-agent', 'Ugrah/0.1')
        return req

    def __canVisitSite(self, stringUrl):
        """
        Checks whether we are allowed by robots.txt to visit some page.
        Returns true if we can, false otherwise.
        """
        parsedUrl = urlparse.urlparse(stringUrl)
        robotsUrl = urlparse.urlunparse((parsedUrl[0], parsedUrl[1], 'robots.txt', parsedUrl[3], parsedUrl[4], parsedUrl[5]))
        self.robotParser.set_url(robotsUrl)
        self.robotParser.read()
        return self.robotParser.can_fetch('Ugrah/0.1', stringUrl)


class Orchid:
    """
    The main class of the crawler. Use this to start the crawling process.
    """
    __module__ = __name__

    def __init__(self, seed, fetcherThreads, maxUrlsToCrawl, timeOut, delay, analyzer=NaiveAnalyzer, args=[]):
        """
        Creates a new crawler.
        @param seed: A map of domain names to urls in that domain from
        which to start crawling.
        @param fetcherThreads: The number of fetcher threads to use.
        @param maxUrlsToCrawl: How many pages to crawl.
        @param timeOut: The socket timeout for loading a page.
        @param delay: The delay between crawls.
        @param analyzer: The class of the analyzer to use.
        """
        authHandler = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener(authHandler)
        urllib2.install_opener(opener)
        self.__linksToFetchAndCond = (dict(seed), Condition())
        self.__siteQueueAndCond = ([], Condition())
        self.__dbAndLock = ({}, Lock())
        self.__maxUrlsToCrawl = maxUrlsToCrawl
        self.__analyzer = analyzer(self.__linksToFetchAndCond, self.__siteQueueAndCond, self.__dbAndLock, *args)
        self.__controller = OrchidController(self.__linksToFetchAndCond, self.__siteQueueAndCond, self.__analyzer, fetcherThreads, maxUrlsToCrawl, timeOut, delay)

    def crawl(self):
        """
        Performs the crawling operation.
        """
        self.__analyzer.start()
        self.__controller.start()
        self.__controller.join()
        self.__analyzer.setStopCondition(True)
        self.__siteQueueAndCond[1].acquire()
        self.__siteQueueAndCond[1].notifyAll()
        self.__siteQueueAndCond[1].release()
        self.__analyzer.join()
        print '%d fetchers were useful' % self.__controller.getNumFetchersUsed()
        print '%d out of %d sites were succesfully crawles' % (len(self.__dbAndLock[0]['sites']), self.__maxUrlsToCrawl)
        print 'The sites that were succesfully crawled:'
        for s in self.__dbAndLock[0]['sites']:
            print self.__dbAndLock[0]['sites'][s].stringUrl

        self.__analyzer.report()


def extractServerName(stringUrl):
    """
    Extracts the domain name from a string URL and returns it.
    """
    u = urlparse.urlparse(stringUrl)
    return u[1]