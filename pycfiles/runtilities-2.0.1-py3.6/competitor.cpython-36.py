# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\competitor.py
# Compiled at: 2020-01-13 13:07:04
# Size of source mod 2**32: 19386 bytes
"""
competitor - access methods for competitor.com
===================================================
"""
import argparse, os.path, urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import unicodedata, logging, pdb, copy
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
import httplib2
from IPython.core.debugger import Tracer
debug_here = Tracer()
from loutilities import timeu
from loutilities import csvu
from runningclub import render
from running import accessError, parameterError
PAGESIZE = 100
COMPETITOR_URL = 'http://running.competitor.com'
RESULTS_METHOD = 'cgiresults'
RESULTS_SEARCH = 'firstname={firstname}&lastname={lastname}&bib={bib}&gender={gender}&division={division}&city={city}&state={state}'
HTTPTIMEOUT = 10
MPERMILE = 1609.344
tindate = timeu.asctime('%m/%d/%Y %I:%M:%S %p')
toutdate = timeu.asctime('%Y-%m-%d')

def racenameanddist(soup):
    """
    get race name and distance from soup
    
    :param soup: BeautifulSoup object for whole page
    :rtype: racename, distmiles, distkm
    """
    ensoup = soup.find(class_='event-name')
    if ensoup:
        eventstring = ensoup.text
        rawparts = eventstring.split('-')
        eventparts = [p.strip() for p in rawparts]
        distfield = eventparts[(-1)].strip()
        racename = '-'.join(rawparts[0:-1]).strip()
    else:
        raise EventNotFound
    dist = 0
    startunits = 0
    for digit in distfield:
        if not digit.isdigit():
            break
        dist *= 10
        dist += int(digit)
        startunits += 1

    units = distfield[startunits:].strip()
    if distfield == 'Marathon':
        distmiles = 26.21875
        distkm = distmiles * (MPERMILE / 1000)
    else:
        if distfield == 'Half Marathon' or distfield == '1/2 Marathon':
            distmiles = 13.109375
            distkm = distmiles * (MPERMILE / 1000)
        else:
            if units == 'K':
                distkm = dist
                distmiles = dist * 1000 / MPERMILE
            else:
                if units == 'Miler':
                    if dist == 13:
                        distmiles = 13.109375
                    else:
                        if dist == 26:
                            distmiles = 26.21875
                        else:
                            distmiles = dist
                    distkm = distmiles * (MPERMILE / 1000)
                else:
                    distmiles = None
                    distkm = None
    return (
     racename, distmiles, distkm)


def racedate(soup):
    """
    get race date from soup
    
    :param soup: BeautifulSoup object for whole page
    :rtype: date of race
    """
    edsoup = soup.find(class_='event-date')
    if edsoup:
        eventdate = edsoup.text.strip()
    else:
        eventdate = None
    return eventdate


class competitorParse:
    __doc__ = '\n    gparseobject\n    \n    :param headingsoup: BeautifulSoup object for column header row\n    :param get: _get function from competitor() to retrieve additional information\n    :param racequery: dict with parameters to get correct race information\n    :rtype: competitorParse instance\n    '

    def __init__(self, headingsoup, get, racequery):
        self.headings = []
        for col in headingsoup.find_all('td', recursive=False):
            self.headings.append(col.text)

        self.racequery = copy.copy(racequery)
        self.get = get

    def details(self, detailurl):
        """
        get detail from url
        
        :param detailurl: url to retrieve result detail from
        :rtype: details dict
        """
        if detailurl[0:7] != 'http://':
            detailurl = COMPETITOR_URL + detailurl
        detail = self.get(detailurl)
        detailsoup = BeautifulSoup(detail)
        agegen = detailsoup.find(class_='detail-pptage').text
        detailsdict = {}
        for attrval in agegen.split('|'):
            attr, val = [av.strip() for av in attrval.split(':')]
            detailsdict[attr] = val

        perfsoup = detailsoup.find(class_='detail-performance-stats')
        for li in perfsoup.find_all('li'):
            attr, val = [av.strip() for av in li.text.split(':')]
            detailsdict['pf' + attr + 'Place'], detailsdict['pf' + attr + 'Count'] = [vo.strip() for vo in val.split('out of')]

        for attr in detailsdict:
            try:
                detailsdict[attr] = int(detailsdict[attr])
            except ValueError:
                pass

        return detailsdict

    def result(self, rowsoup):
        """
        get result from rowsoup
        
        :param headingsoup: BeautifulSoup object for column header row
        :param rowsoup: BeautifulSoup object for row
        :rtype: competitorResult instance
        """
        rowcells = []
        soupcells = []
        for cell in rowsoup.find_all('td'):
            rowcells.append(cell.text.strip())
            soupcells.append(cell)

        soupdict = dict(list(zip(self.headings, soupcells)))
        rowdict = dict(list(zip(self.headings, rowcells)))
        for attr in rowdict:
            try:
                rowdict[attr] = int(rowdict[attr])
            except ValueError:
                pass

        detailurl = soupdict['Name'].find('a')['href']
        details = self.details(detailurl)
        rowdict.update(details)
        irsattrs = competitorResult.result_attrs
        orsattrs = competitorResult.attrs
        attrvals = []
        for i in range(len(irsattrs)):
            inattr = irsattrs[i]
            outattr = orsattrs[i]
            attrvals.append((outattr, rowdict[inattr]))

        rowresult = competitorResult()
        rowresult.set(attrvals)
        return rowresult


class competitorResult:
    __doc__ = '\n    holds result from competitor.com\n    \n    :param oaplace: overall place\n    :param genplace: gender place\n    :param age: age on race day\n    :param gender: gender\n    :param racetime: finishing time h:mm:ss\n    :param racedate: date of race yyyy-mm-dd\n    :param raceloc: location of race\n    :param racename: name of race\n    :param distmiles: distance in miles\n    :param distkm: distance in kilometers\n    '
    result_attrs = 'pfOverallPlace,pfGenderPlace,pfDivisionPlace,Name'.split(',') + ['City, State'] + 'Age,Gender,Time'.split(',')
    attrs = 'oaplace,genplace,divplace,name,hometown,age,gender,racetime,racedate,raceloc,racename,distmiles,distkm'.split(',')

    def __init__(self, oaplace=None, genplace=None, divplace=None, name=None, hometown=None, age=None, gender=None, racetime=None, racedate=None, raceloc=None, racename=None, distmiles=None, distkm=None):
        self.oaplace = oaplace
        self.genplace = genplace
        self.divplace = divplace
        self.name = name
        self.hometown = hometown
        self.age = age
        self.gender = gender
        self.racetime = racetime
        self.racedate = racedate
        self.raceloc = raceloc
        self.racename = racename
        self.distmiles = distmiles
        self.distkm = distkm

    def __repr__(self):
        reprval = '{}('.format(self.__class__)
        for attr in self.attrs:
            reprval += '{}={},'.format(attr, getattr(self, attr))

        reprval = reprval[:-1]
        reprval += ')'
        return reprval

    def set(self, attrvals):
        """
        set attributes based on list of attr,val pairs
        
        :param attrvals: [(attr,val),...]
        """
        for attr, inval in attrvals:
            val = csvu.str2num(inval)
            if attr in ('racedate', ):
                val = toutdate.epoch2asc(tindate.asc2epoch(val))
            setattr(self, attr, val)


class Competitor:
    __doc__ = '\n    access methods for competitor.com\n    '

    def __init__(self, debug=False):
        """
        initialize http 
        """
        self.http = httplib2.Http(timeout=HTTPTIMEOUT)
        self.log = logging.getLogger('running.competitor')
        self.setdebug(debug)
        self.urlcount = 0
        self.racequery = {'eId':'', 
         'eiId':'',  'seId':''}

    def setdebug(self, debugval):
        """
        set debugging attribute for this class
        
        :param debugval: set to True to enable debugging
        """
        if not debugval:
            level = logging.INFO
        else:
            level = logging.DEBUG
        self.log.setLevel(level)

    def setraceyear(self, eventid, eventinstanceid, singleeventid):
        """
        set the raceid, yearid and eventid for subsequent requests
        
        :param eventid: event id from running.competitor.com
        :param eventinstanceid: event instance id from running.competitor.com
        :param singleeventid: single event id from running.competitor.com
        """
        self.racequery['eId'] = eventid
        self.racequery['eiId'] = eventinstanceid
        self.racequery['seId'] = singleeventid

    def geturlcount(self):
        """
        each time a url is retrieved, this counter is bumped
        
        :rtype: integer, number of url's retrieved
        """
        return self.urlcount

    def getresults(self, limit=None):
        """
        return results for the current race / event
        
        :param limit: limit number of records (for testing only)
        :rtype: list of competitorResult objects
        """
        first = True
        pagenum = 1
        results = []
        while 1:
            params = {'resultsPage':pagenum,  'rowCount':PAGESIZE}
            params.update(self.racequery)
            self.log.info(params)
            pagenum += 1
            page = (self._get)(RESULTS_METHOD, **params)
            soup = BeautifulSoup(page)
            if first:
                event, distmiles, distkm = racenameanddist(soup)
                eventdate = racedate(soup)
                first = False
            resulttable = soup.select('.cg-runnergrid-table tbody')[0]
            if not resulttable:
                raise ResultsNotFound
            resultrows = resulttable.find_all('tr', recursive=False)
            if len(resultrows) <= 1:
                break
            headerrow = resultrows[0]
            rr = competitorParse(headerrow, self._geturl, self.racequery)
            for resultrow in resultrows[1:]:
                result = rr.result(resultrow)
                result.racename = event
                result.distmiles = distmiles
                result.distkm = distkm
                results.append(result)
                if limit:
                    if len(results) >= limit:
                        break

            if limit:
                if len(results) >= limit:
                    break

        return results

    def _geturl(self, url):
        """
        get raw url
        
        :param url: url to retrieve
        :rtype: content (html)
        """
        retries = 10
        while retries > 0:
            retries -= 1
            try:
                self.log.debug(url)
                resp, content = self.http.request(url)
                self.urlcount += 1
                break
            except Exception as e:
                if retries == 0:
                    self.log.info('{} requests attempted'.format(self.geturlcount()))
                    self.log.error('http request failure, retries exceeded: {0}'.format(e))
                    raise
                self.log.warning('http request failure: {0}'.format(e))

        if resp.status != 200:
            raise accessError('URL response status = {0}'.format(resp.status))
        return content

    def _get(self, method='', **params):
        """
        get method for competitor access
        
        :param method: competitor method to call
        :param **params: parameters for the method
        :rtype: content (html)
        """
        body = urllib.parse.urlencode(params)
        url = '{}/{}?{}'.format(COMPETITOR_URL, method, body)
        content = self._geturl(url)
        return content


def main():
    descr = '\n    unit test for competitor.py\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    args = parser.parse_args()


if __name__ == '__main__':
    main()