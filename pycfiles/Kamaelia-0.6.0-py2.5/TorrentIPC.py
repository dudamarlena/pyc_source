# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/Torrent/TorrentIPC.py
# Compiled at: 2008-10-19 12:19:52
"""(Bit)Torrent IPC messages"""
from Kamaelia.BaseIPC import IPC

class TIPCMakeTorrent(IPC):
    """Create a .torrent file"""
    Parameters = [
     'trackerurl', 'log2piecesizebytes', 'title', 'comment', 'srcfile']


class TIPCServicePassOn(IPC):
    """Add a client to TorrentService"""
    Parameters = [
     'replyService', 'message']


class TIPCServiceAdd(IPC):
    """Add a client to TorrentService"""
    Parameters = [
     'replyService']


class TIPCServiceRemove(IPC):
    """Remove a client from TorrentService"""
    Parameters = [
     'replyService']


class TIPCNewTorrentCreated(IPC):
    """New torrent %(torrentid)d created in %(savefolder)s"""
    Parameters = [
     'torrentid', 'savefolder']


class TIPCTorrentAlreadyDownloading(IPC):
    """That torrent is already downloading!"""
    Parameters = [
     'torrentid']


class TIPCTorrentStartFail(object):
    """Torrent failed to start!"""
    Parameters = []


class TIPCTorrentStatusUpdate(IPC):
    """Current status of a single torrent"""

    def __init__(self, torrentid, statsdictionary):
        super(TIPCTorrentStatusUpdate, self).__init__()
        self.torrentid = torrentid
        self.statsdictionary = statsdictionary

    def __str__(self):
        return 'Torrent %d status : %s' % (self.torrentid, str(int(self.statsdictionary.get('fractionDone', 0) * 100)) + '%')


class TIPCCreateNewTorrent(IPC):
    """Create a new torrent"""
    Parameters = [
     'rawmetainfo']


class TIPCCloseTorrent(IPC):
    """Close torrent %(torrentid)d"""
    Parameters = [
     'torrentid']