# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/theHarvester/discovery/yandexsearch.py
# Compiled at: 2013-12-09 06:41:17
import string, httplib, sys, myparser, re, time

class search_yandex:

    def __init__(self, word, limit, start):
        self.word = word
        self.results = ''
        self.totalresults = ''
        self.server = 'yandex.com'
        self.hostname = 'yandex.com'
        self.userAgent = '(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6'
        self.limit = limit
        self.counter = start

    def do_search(self):
        h = httplib.HTTP(self.server)
        h.putrequest('GET', '/search?text=%40' + self.word + '&numdoc=50&lr=' + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        self.totalresults += self.results
        print self.results

    def do_search_files(self, files):
        h = httplib.HTTP(self.server)
        h.putrequest('GET', '/search?text=%40' + self.word + '&numdoc=50&lr=' + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        self.totalresults += self.results

    def check_next(self):
        renext = re.compile('topNextUrl')
        nextres = renext.findall(self.results)
        if nextres != []:
            nexty = '1'
            print str(self.counter)
        else:
            nexty = '0'
        return nexty

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_files(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.fileurls(self.files)

    def process(self):
        while self.counter <= self.limit:
            self.do_search()
            self.counter += 50
            print 'Searching ' + str(self.counter) + ' results...'

    def process_files(self, files):
        while self.counter < self.limit:
            self.do_search_files(files)
            time.sleep(0.3)
            self.counter += 50