# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Fourchapy/ThreadPage.py
# Compiled at: 2012-12-26 16:06:50
"""
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
"""
import logging
logger = logging.getLogger('Fourchapy.' + __name__)
log = logger.log
from Fetcher import Fetch4chan
from Thread import FourchapyThread
from Errors import NoDataReturnedError, ThreadNotFoundError

class FourchapyThreadPage(Fetch4chan):
    """ Represent a page of threads for a given board.     
    """

    def __init__(self, boardID, pageID, proto='http', **kw):
        self.Proto = proto
        self.Board = boardID
        self.Page = int(pageID)
        log(10, 'Creating %r - board:%r page:%r', self, boardID, pageID)
        self.URL = '%s://api.4chan.org/%s/%d.json' % (self.Proto, self.Board, self.Page)
        Fetch4chan.__init__(self, **kw)

    @Fetch4chan.addLazyDataObjDec(attrName='Threads')
    def updateThreadsList(self, sleep=True):
        """ Download and update local data with data from 4chan. """
        threads = []
        try:
            json = self.fetchJSON(sleep=sleep)
        except NoDataReturnedError:
            raise ThreadNotFoundError, 'Page number %d from %r was not found on the server. ' % (self.Page, self.Board)

        for data in json['threads']:
            threads.append(FourchapyThread(boardID=self.Board, threadID=int(data['posts'][0]['no']), proto=self.Proto, proxies=self.Proxies))

        log(10, 'Found %d threads for %r', len(threads), self)
        return threads

    @Fetch4chan.addLazyDataObjDec(attrName='ThreadsDict')
    def updateThreadsDict(self, sleep=True):
        """ Download and update local data with data from 4chan. """
        ret = {}
        for thread in self.Threads:
            ret[thread.Thread] = thread

        log(10, 'Found %d threads for %r', len(ret), self)
        return ret

    def __repr__(self):
        return '<ThreadPage %r %r>' % (self.Board, self.Page)