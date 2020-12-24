# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Fourchapy/Post.py
# Compiled at: 2012-12-26 16:28:32
"""
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
"""
import logging
logger = logging.getLogger('Fourchapy.' + __name__)
log = logger.log
from Fetcher import Fetch4chan

class FourchapyPost(Fetch4chan):
    """ A 4chan post
    """
    POSTOBJECTS = {'no': dict(type=int, name='Number', desc='Post Number'), 
       'resto': dict(type=int, name='ReplyTo', desc='ReplyTo'), 
       'sticky': dict(type=bool, name='Sticky', desc='Stickied Thread'), 
       'closed': dict(type=bool, name='Closed', desc='Closed Thread'), 
       'now': dict(type=unicode, name='DateTime', desc='Date & Time'), 
       'time': dict(type=int, name='UnixDateTime', desc='Date & Time as a Unix Timestamp'), 
       'name': dict(type=unicode, name='Name', desc='Name'), 
       'trip': dict(type=unicode, name='Tripcode', desc='Tripcode'), 
       'id': dict(type=unicode, name='UserType', desc='User Type'), 
       'capcode': dict(type=unicode, name='Capcode', desc=''), 
       'country': dict(type=unicode, name='CountryCode', desc=''), 
       'country_name': dict(type=unicode, name='CountryName', desc=''), 
       'email': dict(type=unicode, name='Email', desc=''), 
       'sub': dict(type=unicode, name='Subject', desc=''), 
       'com': dict(type=unicode, name='Comment', desc='Comment'), 
       'tim': dict(type=int, name='RenamedFilename', desc='Renamed Filename'), 
       'filename': dict(type=unicode, name='OrgFilename', desc='Original Filename'), 
       'ext': dict(type=unicode, name='FileExtension', desc=''), 
       'fsize': dict(type=int, name='FileSize', desc='Size of the file in bytes'), 
       'md5': dict(type=unicode, name='MD5', desc=''), 
       'w': dict(type=int, name='ImageWidth', desc=''), 
       'h': dict(type=int, name='ImageHeight', desc=''), 
       'tn_w': dict(type=int, name='ThumbnailWidth', desc=''), 
       'tn_h': dict(type=int, name='ThumbnailHeight', desc=''), 
       'filedeleted': dict(type=bool, name='FileDeleted', desc=''), 
       'spoiler': dict(type=bool, name='SpoilerImage', desc=''), 
       'custom_spoiler': dict(type=int, name='CustomSpoiler', desc='')}

    def __init__(self, board, postData=None, proto='http', index=0, proxies={}):
        self.Board = board
        self.Proto = proto
        self._rawData = postData
        self.Index = index
        self.Proxies = proxies
        for (code, info) in self.POSTOBJECTS.items():
            if postData.has_key(code):
                value = info['type'](postData[code])
                log(5, 'Found %r. Set %r to %r', code, info['name'], value)
                setattr(self, info['name'], value)
            else:
                log(5, "Didn't find %r", code)
                setattr(self, info['name'], None)

        if self.RenamedFilename:
            self.ImageURL = '%s://images.4chan.org/%s/src/%d.%s' % (self.Proto, self.Board, self.RenamedFilename, self.FileExtension)
            self.ThumbImageURL = '%s://1.thumbs.4chan.org/%s/thumb/%d.jpg' % (self.Proto, self.Board, self.RenamedFilename)
        return

    def displayToString(self, nameWidth=15):
        """ Return a multi-line string that displays this post's info. """
        ret = '=' * 50 + '\n'
        ret += ' %s #%d: %r' % (self.Board, self.Number, self.Subject) + '\n'
        ret += '=' * 50 + '\n'
        for (code, info) in self.POSTOBJECTS.items():
            value = str(getattr(self, info['name']))
            if value == 'None':
                continue
            if value.count('\n') == 0:
                for line in value.split('<br>'):
                    ret += info['name'].rjust(nameWidth) + ': ' + line + '\n'

            else:
                for line in value.splitlines():
                    for line2 in line.split('<br>'):
                        ret += info['name'].rjust(nameWidth) + ': ' + line2 + '\n'

        return ret

    def display(self, nameWidth=15):
        """ Return a multi-line string that displays this post's info. """
        print self.displayToString(nameWidth=nameWidth)

    def getImageURL(self):
        """ Returns the URL to download the image at. None if there isn't one """
        if hasattr(self, 'RenamedFilename') and self.RenamedFilename and hasattr(self, 'FileExtension') and self.FileExtension:
            return '%s://images.4chan.org/%s/src/%s%s' % (self.Proto, self.Board, self.RenamedFilename, self.FileExtension)
        else:
            return

    def getImageThumbURL(self):
        """ Returns the URL to download the image at. None if there isn't one """
        import random
        if hasattr(self, 'RenamedFilename') and self.RenamedFilename:
            return '%s://%d.thumbs.4chan.org/%s/thumb/%s.jpg' % (self.Proto, random.randint(0, 2), self.Board, self.RenamedFilename)
        else:
            return

    def __repr__(self):
        return '<Post %r %r>' % (self.Board, self.Number)