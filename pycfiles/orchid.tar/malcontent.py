# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pesachzon/workspace/crawler/orchid/malcontent.py
# Compiled at: 2005-12-13 08:20:11
"""
This package is an implementation of an exploit detection analyzer
for the Orchid system and several rules for detecting specific
types of exploits.
"""
from orchid import *
import re, logging

class Malcontent(NaiveAnalyzer):
    """
    This is a concrete analyzer which used together with the Orchid crawler
    to detect malicious web pages based on a given set of rules.
    """
    __module__ = __name__

    def __init__(self, linksToFetchAndCond, siteQueueAndCond, db, rules):
        """
        Creates a new malicious content analyzer.
        @param rules: a list of Rule objects to be applied against crawled sites.
        """
        NaiveAnalyzer.__init__(self, linksToFetchAndCond, siteQueueAndCond, db)
        self.__newLinksToCrawl = []
        self.__evilServers = {}
        self.__rules = rules
        self.__evilnessCounter = {Rule.GOOD: 0, Rule.MAY_BE_EVIL: 0, Rule.EVIL: 0}
        self.__exploitCounter = {}

    def analyzeSite(self, db, site):
        """
        Applies all the available rules to the given site and extracts the
        links that we intend to crawl. Currently we follow regular ('<a...'), frame,
        iframe and script links.
        """
        if not db.has_key('evilSites'):
            db['evilSites'] = {}
        if self.__checkSiteEvilness(site) > Rule.GOOD:
            del site.content
            del site.rawContent
            db['evilSites'][site.stringUrl] = site
            logging.warning('Evil site found: url [%s], evilness [%d]' % (site.stringUrl, site.evilness))
        db['crawled'][site.stringUrl] = True
        self.__newLinksToCrawl = [ link for link in site.links['regular'] if not db['crawled'].has_key(link) ]
        self.__newLinksToCrawl += [ link for link in site.links['frame'] if not db['crawled'].has_key(link) ]
        self.__newLinksToCrawl += [ link for link in site.links['iframe'] if not db['crawled'].has_key(link) ]
        self.__newLinksToCrawl += [ link for link in site.links['script'] if not db['crawled'].has_key(link) ]
        tempList = []
        for l in self.__newLinksToCrawl:
            db['crawled'][l] = True
            if l not in tempList:
                tempList += [l]

        tempList = [ l for l in tempList if l not in site.evilLinks ]
        self.__newLinksToCrawl = tempList

    def addSiteToFetchQueue(self, lfs):
        """
        Add the sites we extracted in analyzeSite to the "to fetch" queue.
        """
        logging.debug('Adding to lfs')
        domMap = self.reorganizeByDomain(self.__newLinksToCrawl)
        for dom in domMap:
            if lfs.has_key(dom):
                lfs[dom] += domMap[dom]
            else:
                lfs[dom] = domMap[dom]

    def selectNextUrl(self):
        """
        Select the next url to crawl to. This is done by selecting
        a random domain and then taking one page from it's queue.
        """
        toFetchQueue = self.linksToFetch[0]
        dom = toFetchQueue.keys()
        selectedDom = dom[randint(0, len(dom) - 1)]
        curUrl = toFetchQueue[selectedDom].pop()
        if len(toFetchQueue[selectedDom]) == 0:
            toFetchQueue.pop(selectedDom)
        return curUrl

    def __checkSiteEvilness(self, site):
        """
        Applies all the rules to the given site and records
        the results.
        """
        ruleEvilness = self.__checkSiteEvilnessWithRules(site)
        evilness = ruleEvilness
        self.__evilnessCounter[evilness] += 1
        if evilness > Rule.GOOD:
            serverName = extractServerName(site.stringUrl)
            if not self.__evilServers.has_key(serverName):
                self.__evilServers[serverName] = evilness
            else:
                self.__evilServers[serverName] = max(evilness, self.__evilServers[serverName])
        site.evilness = evilness
        return evilness

    def __checkSiteEvilnessWithRules(self, site):
        """
        Applies all the rules to the given site. 
        Helper method.
        """
        finalEvilness = Rule.GOOD
        for rule in self.__rules:
            (evilness, exploits) = rule(site)
            if evilness > finalEvilness:
                finalEvilness = evilness
            if evilness > Rule.GOOD:
                for exploit in exploits:
                    if not self.__exploitCounter.has_key(exploit):
                        self.__exploitCounter[exploit] = exploits[exploit]
                    else:
                        self.__exploitCounter[exploit] += exploits[exploit]

        return finalEvilness

    def report(self):
        """
        Logs the results of the crawl.
        """
        logging.info('Report:')
        logging.info('============')
        logging.info('Malicious sites detected: %d' % sum(self.__evilnessCounter))
        logging.info('    Breakdown: Good [%d], maybe evil [%d], evil [%d]' % (self.__evilnessCounter[Rule.GOOD], self.__evilnessCounter[Rule.MAY_BE_EVIL], self.__evilnessCounter[Rule.EVIL]))
        logging.info('Exploits:')
        for e in self.__exploitCounter:
            logging.info('    [%s] : %d' % (e, self.__exploitCounter[e]))

        logging.info('Evil servers:')
        for s in self.__evilServers:
            logging.info('    [%s] : %d' % (s, self.__evilServers[s]))

        logging.info('Exploit Info:')
        for s in self.db[0]['evilSites']:
            logging.info('    [%s]' % s)
            for l in self.db[0]['evilSites'][s].matches:
                logging.info('        [%s] [%s]' % (l[0], l[1]))


class Rule:
    """
    An abstract class representing rules for detecting malicious content.
    """
    __module__ = __name__
    GOOD = 0
    MAY_BE_EVIL = 1
    EVIL = 2

    def __call__(self, site):
        """
        Applies the rule to the given site. Should be overriden by real
        rules.
        """
        raise Exception, 'This is an abstract class'


class LinkRule(Rule):
    """
    This rule applies regular expressions to certain link 
    types.
    """
    __module__ = __name__

    def __init__(self, reMap, reFlags=re.I | re.X):
        """
        Creates a new LinkRule
        @param reMap: a map which maps regular expression strings to tuples
        of the form (exploitName, linkTypes, level) where exploitName is the
        name of the exploit, linkTypes is a list of link types on which to match
        the regular expression (see orchid.OrchidExtractor for more detail), and level
        is the level of maliciousness for example: Rule.EVIL
        """
        self.__reMap = {}
        for pattern in reMap:
            self.__reMap[re.compile(pattern, reFlags)] = reMap[pattern]

    def __call__(self, site):
        """
        Applies the rule to the given site.
        """
        links = site.links
        curLevel = Rule.GOOD
        exploits = {}
        for pattern in self.__reMap:
            (exploitName, linkTypes, level) = self.__reMap[pattern]
            for linkType in linkTypes:
                if links.has_key(linkType) and len(links[linkType]) != 0:
                    for link in links[linkType]:
                        m = pattern.search(link)
                        if m:
                            site.evilLinks += [link]
                            site.matches += [(m.group(), exploitName)]
                            if curLevel < level:
                                curLevel = level
                            if exploits.has_key(exploitName):
                                exploits[exploitName] += 1
                            else:
                                exploits[exploitName] = 1

        return (
         curLevel, exploits)


class ContentRule(Rule):
    """
    This rule type matches regular expressions against the 
    raw content of the pages.
    """
    __module__ = __name__

    def __init__(self, reMap, reFlags=re.I | re.X):
        """
        Creates a new ContentRule.
        @param reMap: a map from regular expression strings to tuples
        of the form (exploitName, level) where exploit name is the exploit
        name and level is the badness level like Rule.EVIL
        """
        self.__reMap = {}
        for pattern in reMap:
            self.__reMap[re.compile(pattern, reFlags)] = reMap[pattern]

    def __call__(self, site):
        """
        Applies the rule to the given site
        """
        links = site.links
        curLevel = Rule.GOOD
        exploits = {}
        content = (' ').join(site.rawContent.split())
        for pattern in self.__reMap:
            (exploitName, level) = self.__reMap[pattern]
            m = pattern.search(content)
            if m:
                site.matches += [(m.group(), exploitName)]
                if curLevel < level:
                    curLevel = level
                if exploits.has_key(exploitName):
                    exploits[exploitName] += 1
                else:
                    exploits[exploitName] = 1

        return (
         curLevel, exploits)


class ExternalIframeRule(Rule):
    """
    This rule type identifies IFRAME elements which load
    content from external servers.
    """
    __module__ = __name__

    def __init__(self):
        """Creates a new ExternalIframeRule"""
        None
        return

    def __call__(self, site):
        """Applies this rule to the given site"""
        links = site.links
        curLevel = Rule.GOOD
        siteServerName = extractServerName(site.stringUrl)
        exploits = {'external iframe': 0}
        for l in links['iframe']:
            sName = extractServerName(l)
            if sName != siteServerName:
                curLevel = Rule.MAY_BE_EVIL
                exploits['external iframe'] += 1
                site.matches += [(l, 'external iframe')]

        return (
         curLevel, exploits)