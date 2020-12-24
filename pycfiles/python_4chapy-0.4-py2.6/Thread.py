# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Fourchapy/Thread.py
# Compiled at: 2012-12-26 16:07:00
"""
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
"""
import logging
logger = logging.getLogger('Fourchapy.' + __name__)
log = logger.log
from Fetcher import Fetch4chan
from Post import FourchapyPost
from Errors import NoDataReturnedError, ThreadNotFoundError

class FourchapyThread(Fetch4chan):
    """ Represent a thread from a 4chan board
    
    """

    def __init__(self, boardID, threadID, proto='http', **kw):
        self.Proto = proto
        self.Board = boardID
        self.Thread = threadID
        log(10, 'Creating %r - board:%r thread:%r', self, boardID, threadID)
        self.URL = '%s://api.4chan.org/%s/res/%d.json' % (self.Proto, self.Board, self.Thread)
        Fetch4chan.__init__(self, **kw)

    @Fetch4chan.addLazyDataObjDec(attrName='Posts')
    def updatePostsList(self, sleep=True):
        """ Download and update local data with data from 4chan. """
        ret = []
        try:
            json = self.fetchJSON(sleep=sleep)
        except NoDataReturnedError:
            raise ThreadNotFoundError, 'Thread ID %r from %r was not found on the server. ' % (self.Thread, self.Board)

        index = 0
        for postData in json['posts']:
            ret.append(FourchapyPost(board=self.Board, postData=postData, proto=self.Proto, index=index, proxies=self.Proxies))
            index += 1

        log(10, 'Found %d posts for %r', len(ret), self)
        return ret

    @Fetch4chan.addLazyDataObjDec(attrName='PostsDict')
    def updatePostsDict(self, sleep=True):
        """ Download and update local data with data from 4chan. """
        ret = {}
        for post in self.Posts:
            ret[post.Number] = post

        log(10, 'Found %d posts for %r', len(ret), self)
        return ret

    def __repr__(self):
        return '<Thread %r %r>' % (self.Board, self.Thread)