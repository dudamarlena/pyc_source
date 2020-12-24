# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ModelRssItem.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 7703 bytes
__doc__ = '\nCreated on Nov 11, 2010\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import os
from arelle import XmlUtil
from arelle.ModelObject import ModelObject
edgr = 'http://www.sec.gov/Archives/edgar'
edgrDescription = '{http://www.sec.gov/Archives/edgar}description'
edgrFile = '{http://www.sec.gov/Archives/edgar}file'
edgrInlineXBRL = '{http://www.sec.gov/Archives/edgar}inlineXBRL'
edgrSequence = '{http://www.sec.gov/Archives/edgar}sequence'
edgrType = '{http://www.sec.gov/Archives/edgar}type'
edgrUrl = '{http://www.sec.gov/Archives/edgar}url'
newRssWatchOptions = {'feedSource': '', 
 'feedSourceUri': None, 
 'matchTextExpr': '', 
 'formulaFileUri': '', 
 'logFileUri': '', 
 'emailAddress': '', 
 'validateXbrlRules': False, 
 'validateDisclosureSystemRules': False, 
 'validateCalcLinkbase': False, 
 'validateFormulaAssertions': False, 
 'alertMatchedFactText': False, 
 'alertAssertionUnsuccessful': False, 
 'alertValiditionError': False, 
 'latestPubDate': None}

class ModelRssItem(ModelObject):

    def init(self, modelDocument):
        super(ModelRssItem, self).init(modelDocument)
        try:
            if self.modelXbrl.modelManager.rssWatchOptions.latestPubDate and self.pubDate <= self.modelXbrl.modelManager.rssWatchOptions.latestPubDate:
                self.status = _('tested')
            else:
                self.status = _('not tested')
        except AttributeError:
            self.status = _('not tested')

        self.results = None
        self.assertions = None

    @property
    def cikNumber(self):
        return XmlUtil.text(XmlUtil.descendant(self, edgr, 'cikNumber'))

    @property
    def accessionNumber(self):
        return XmlUtil.text(XmlUtil.descendant(self, edgr, 'accessionNumber'))

    @property
    def fileNumber(self):
        return XmlUtil.text(XmlUtil.descendant(self, edgr, 'fileNumber'))

    @property
    def companyName(self):
        return XmlUtil.text(XmlUtil.descendant(self, edgr, 'companyName'))

    @property
    def formType(self):
        return XmlUtil.text(XmlUtil.descendant(self, edgr, 'formType'))

    @property
    def pubDate(self):
        try:
            return self._pubDate
        except AttributeError:
            from arelle.UrlUtil import parseRfcDatetime
            self._pubDate = parseRfcDatetime(XmlUtil.text(XmlUtil.descendant(self, None, 'pubDate')))
            return self._pubDate

    @property
    def filingDate(self):
        try:
            return self._filingDate
        except AttributeError:
            import datetime
            self._filingDate = None
            date = XmlUtil.text(XmlUtil.descendant(self, edgr, 'filingDate'))
            d = date.split('/')
            if d and len(d) == 3:
                self._filingDate = datetime.date(_INT(d[2]), _INT(d[0]), _INT(d[1]))
            return self._filingDate

    @property
    def period(self):
        per = XmlUtil.text(XmlUtil.descendant(self, edgr, 'period'))
        if per and len(per) == 8:
            return '{0}-{1}-{2}'.format(per[0:4], per[4:6], per[6:8])

    @property
    def assignedSic(self):
        return XmlUtil.text(XmlUtil.descendant(self, edgr, 'assignedSic'))

    @property
    def acceptanceDatetime(self):
        try:
            return self._acceptanceDatetime
        except AttributeError:
            import datetime
            self._acceptanceDatetime = None
            date = XmlUtil.text(XmlUtil.descendant(self, edgr, 'acceptanceDatetime'))
            if date and len(date) == 14:
                self._acceptanceDatetime = datetime.datetime(_INT(date[0:4]), _INT(date[4:6]), _INT(date[6:8]), _INT(date[8:10]), _INT(date[10:12]), _INT(date[12:14]))
            return self._acceptanceDatetime

    @property
    def fiscalYearEnd(self):
        yrEnd = XmlUtil.text(XmlUtil.descendant(self, edgr, 'fiscalYearEnd'))
        if yrEnd and len(yrEnd) == 4:
            return '{0}-{1}'.format(yrEnd[0:2], yrEnd[2:4])

    @property
    def htmlUrl(self):
        htmlDocElt = XmlUtil.descendant(self, edgr, 'xbrlFile', attrName=edgrSequence, attrValue='1')
        if htmlDocElt is not None:
            return htmlDocElt.get(edgrUrl)

    @property
    def url(self):
        try:
            return self._url
        except AttributeError:
            self._url = None
            for instDocElt in XmlUtil.descendants(self, edgr, 'xbrlFile'):
                if instDocElt.get(edgrType).endswith('.INS') or instDocElt.get(edgrInlineXBRL) == 'true':
                    self._url = instDocElt.get(edgrUrl)
                    break

            return self._url

    @property
    def enclosureUrl(self):
        return XmlUtil.childAttr(self, None, 'enclosure', 'url')

    @property
    def zippedUrl(self):
        enclosure = XmlUtil.childAttr(self, None, 'enclosure', 'url')
        if enclosure:
            _path, sep, file = (self.url or '').rpartition('/')
            return enclosure + sep + file
        else:
            return self.url

    @property
    def htmURLs(self):
        try:
            return self._htmURLs
        except AttributeError:
            self._htmURLs = [(instDocElt.get(edgrDescription), instDocElt.get(edgrUrl)) for instDocElt in XmlUtil.descendants(self, edgr, 'xbrlFile') if instDocElt.get(edgrFile).endswith('.htm')]
            return self._htmURLs

    @property
    def primaryDocumentURL(self):
        try:
            return self._primaryDocumentURL
        except AttributeError:
            formType = self.formType
            self._primaryDocumentURL = None
            for instDocElt in XmlUtil.descendants(self, edgr, 'xbrlFile'):
                if instDocElt.get(edgrType) == formType:
                    self._primaryDocumentURL = instDocElt.get(edgrUrl)
                    break

            return self._primaryDocumentURL

    def setResults(self, modelXbrl):
        self.results = []
        self.assertionUnsuccessful = False
        self.status = 'pass'
        for error in modelXbrl.errors:
            if isinstance(error, dict):
                self.assertions = error
                for countSuccessful, countNotsuccessful in error.items():
                    if countNotsuccessful > 0:
                        self.assertionUnsuccessful = True
                        self.status = 'unsuccessful'

            else:
                self.results.append(error)
                self.status = 'fail'

        self.results.sort()

    @property
    def propertyView(self):
        return (
         (
          'CIK', self.cikNumber),
         (
          'company', self.companyName),
         (
          'published', self.pubDate),
         (
          'form type', self.formType),
         (
          'filing date', self.filingDate),
         (
          'period', self.period),
         (
          'year end', self.fiscalYearEnd),
         (
          'status', self.status),
         (
          'instance', os.path.basename(self.url)))

    def __repr__(self):
        return 'rssItem[{0}]{1})'.format(self.objectId(), self.propertyView)