# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/viaggiatreno/siteintf.py
# Compiled at: 2009-02-02 06:01:34
import urllib, urllib2, re, datetime
from BeautifulSoup import BeautifulSoup

class SiteInterface(object):
    BASEURL = 'http://mobile.viaggiatreno.it/viaggiatreno/mobile/scheda'
    USERAGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8) Gecko/20051111 Firefox/1.5'

    def _queryByGet(self, idTreno):
        params = {'numeroTreno': idTreno, 'dettaglio': 'visualizza'}
        headers = {'User-Agent': self.USERAGENT}
        newurl = '%s?%s' % (self.BASEURL, urllib.urlencode(params))
        req = urllib2.Request(newurl, headers=headers)
        r = urllib2.urlopen(req)
        html = r.read()
        return html

    def _queryByFile(self, htmlfile='tmp.htm'):
        fp = open(htmlfile)
        html = fp.read()
        return html

    def timediff(self, t1, t2):
        """Returns the difference in minutes between t1 and 2.
                Both must be strings in the "%H:%M" format.
                If t2 < t1, result will be negative."""
        t1 = datetime.datetime.strptime(t1, '%H:%M')
        t2 = datetime.datetime.strptime(t2, '%H:%M')
        if t2 < t1:
            diff = (t1 - t2).seconds / -60
            if diff < -10:
                diff = (t2 - t1).seconds / 60
        else:
            diff = (t2 - t1).seconds / 60
        return diff

    def dumpHtml(self, html, dumpfile=None):
        """Dump HTML, if needed."""
        assert html is not None
        if dumpfile is not None:
            re.sub('"/viaggiatreno/css/mobile.css"', '"mobile.css"', html)
            re.sub('"/"', '"http://mobile.viaggiatreno.it/"', html)
            fp = open(dumpfile, 'w')
            fp.write(html)
            fp.close()
        return

    def _parse(self, html):
        """Parse HTML and extract the data of interest."""
        ret = []
        soup = BeautifulSoup(html)
        for div in soup.findAll('div', {'class': 'giaeffettuate'}) + soup.findAll('div', {'class': 'corpocentrale'}):
            station = div.find('h2')
            station = str(station.contents[0])
            prog = None
            real = None
            tag = None
            for p in div.findAll('p'):
                t = str(p.contents[0])
                time = p.find('strong')
                if len(time.contents) > 0:
                    time = str(time.contents[0])
                else:
                    time = '00:00'
                if re.search('(?i)programmat(a|o)', t):
                    prog = time
                elif re.search('(?i)effettiv(a|o)', t):
                    real = time
                    tag = 'eff'
                elif re.search('(?i)previst(a|o)', t):
                    real = time
                    tag = 'est'

            assert prog is not None and real is not None and tag is not None
            e = (station, prog, real, self.timediff(prog, real), tag)
            ret.append(e)

        return ret

    def query(self, trainId, dumpfile=None, infile=None):
        if infile is not None:
            html = self._queryByFile(infile)
        else:
            html = self._queryByGet(trainId)
        self.dumpHtml(html, dumpfile)
        return self._parse(html)


if __name__ == '__main__':
    si = SiteInterface()
    print si.query(2513)