# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Fourchapy/BoardIndex.py
# Compiled at: 2012-12-26 16:21:49
"""
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
"""
import logging
logger = logging.getLogger('Fourchapy.' + __name__)
log = logger.log
from Fetcher import Fetch4chan
from Board import FourchapyBoard
from Errors import NoDataReturnedError

class FourchapyBoardIndex(Fetch4chan):
    """ Represent a list of all boards and info about those boards. 

    """

    def __init__(self, proto='http', **kw):
        self.Proto = proto
        log(10, 'Creating %r', self)
        self.URL = '%s://api.4chan.org/boards.json' % self.Proto
        Fetch4chan.__init__(self, **kw)

    @Fetch4chan.addLazyDataObjDec(attrName='Boards')
    def updateBoardsList(self, sleep=True):
        """ Download and update local data with data from 4chan. """
        json = self.fetchJSON(sleep=sleep)
        boards = []
        for boardData in json['boards']:
            board = FourchapyBoard(boardData=boardData, proto=self.Proto, proxies=self.Proxies)
            boards.append(board)
            log(5, 'Created board %r', board)

        log(10, 'Found %d boards', len(boards))
        return boards

    @Fetch4chan.addLazyDataObjDec(attrName='BoardsDict')
    def updateBoardsDict(self, sleep=True):
        ret = {}
        for board in self.Boards:
            ret[board.Board] = board

        return ret

    def __repr__(self):
        return '<BoardIndex Use:%r>' % self.Proto