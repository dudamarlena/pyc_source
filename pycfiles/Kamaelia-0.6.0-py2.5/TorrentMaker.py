# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/Torrent/TorrentMaker.py
# Compiled at: 2008-10-19 12:19:52
import os
os.environ['LANG'] = 'en_GB.UTF-8'
import sys, locale
from BitTorrent.makemetafile import make_meta_files
from BitTorrent.parseargs import parseargs, printHelp
from BitTorrent import BTFailure
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Protocol.Torrent.TorrentIPC import *
import time, os, tempfile

class TorrentMaker(threadedcomponent):
    """Limitations: Only one file per torrent file"""

    def __init__(self, defaulttracker=''):
        super(TorrentMaker, self).__init__()
        self.defaulttracker = defaulttracker

    def maketorrent(self, request):
        le = locale.getpreferredencoding()
        try:
            tmp = tempfile.mkstemp('', 'kamTorrentMaker')
            make_meta_files(url=request.trackerurl, files=[
             request.srcfile.decode(le)], piece_len_pow2=request.log2piecesizebytes, title=request.title, comment=request.comment, target=tmp[1], progressfunc=lambda x: None, filefunc=lambda x: None)
            tmpfile = os.fdopen(tmp[0])
            metadata = tmpfile.read()
            tmpfile.close()
            os.unlink(tmp[1])
            (tmp, tmpfile) = (None, None)
            self.send(metadata, 'outbox')
        except BTFailure, e:
            print str(e)

        return

    def main(self):
        unfinished = True
        while unfinished or self.dataReady('inbox'):
            if self.dataReady('inbox'):
                request = self.recv('inbox')
                if isinstance(request, str):
                    request = TIPCMakeTorrent(trackerurl=self.defaulttracker, srcfile=request, title=os.path.split(request)[1], comment='Created by Kamaelia', log2piecesizebytes=18)
                if isinstance(request, TIPCMakeTorrent):
                    self.maketorrent(request)
                else:
                    print 'TorrentMaker - what on earth is a ' + str(type(request)) + '!?'
            elif self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished):
                    unfinished = False
                elif isinstance(msg, shutdown):
                    return
            else:
                time.sleep(2.0)


__kamaelia_components__ = (TorrentMaker,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.File.Writing import SimpleFileWriter
    pipeline(ConsoleReader('>>> ', ''), TorrentMaker('http://example.com:12345/'), SimpleFileWriter('mytorrent.torrent')).run()