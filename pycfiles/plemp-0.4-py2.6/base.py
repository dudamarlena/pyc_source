# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plemp/base.py
# Compiled at: 2010-10-21 11:19:43
import os
from twisted.internet import defer
from twisted.python import log
from plemp.flickr import Flickr
from plemp import api_key, api_secret

class Uploader(object):
    """
    The uploader performs the actual uploading.
    """
    numUploaded = 0
    numUploading = 0
    uploadStarted = False
    currentFile = None

    def __init__(self, profile=None):
        self.files = []
        self.upload = {'is_public': 1, 'is_family': 0, 
           'is_friend': 0, 
           'search_hidden': 0}
        self.photoset = None
        self.exif = {}
        self.flickr = Flickr(api_key, api_secret, profile=profile, perms='write')
        self.profile = profile
        self.photosets = None
        self.ticket2filename = {}
        self.uploadErrors = []
        return

    def initializeAPI(self, authCallback, errback=None):
        """
        Initialize the Flickr API and perform the initial authorization, if needed.
        """

        def auth_1(state):
            if state is not None:
                if authCallback(state['url']):
                    return self.flickr.authenticate_2(state).addCallbacks(self.connected, errback)
            return self.connected(state)

        return self.flickr.authenticate_1().addCallback(auth_1)

    def connected(self, state):
        """ We are connected. """
        return self.loadPhotoSets()

    def setProgressCallback(self, cb):
        self.progressCallback = cb

    def addFile(self, file):
        if not os.path.exists(file):
            raise OSError, 'File does not exist.'
        self.files.append(file)
        if self.uploadStarted:
            self.progressCallback(self.currentFile, self.getProgress(), self.numUploaded + 1, self.numTotal)

    def setUploadOption(self, opt, value):
        if opt not in self.upload:
            raise ValueError('Invalid upload option: ' + opt)
        self.upload[opt] = value

    def canStart(self):
        if self.photoset == 'ask':
            return False
        return True

    def uploadSingle(self, f, uploaded):
        self.currentFile = f
        self.progressCallback(self.currentFile, self.getProgress(), self.numUploaded + 1, self.numTotal)

        def progress(client, p):
            self.progressCallback(self.currentFile, max(0.0, min(1.0, self.getProgress() + p / float(self.numTotal))), self.numUploaded + 1, self.numTotal)

        d = self.flickr.upload(filename=f, progressCallback=progress, async=1, **self.upload)

        def incr(rsp):
            ticketid = rsp.find('ticketid').text
            uploaded.append(ticketid)
            self.ticket2filename[ticketid] = f
            self.numUploading -= 1
            self.numUploaded += 1
            return uploaded

        d.addCallback(incr)
        return d

    def doUpload(self):
        """
        Upload the files in the current queue. When done, it checks
        for more files and continues to upload those as well.
        """
        self.uploadStarted = True

        def upload(uploaded=[]):
            files = self.files[:]
            self.numUploading = len(self.files)
            self.files = []

            def makeUploader(f):
                return lambda uploaded: self.uploadSingle(f, uploaded)

            d = defer.succeed(uploaded)
            for f in files:
                d.addCallback(makeUploader(f))

            return d

        d = upload()

        def checkForMore(uploaded):
            if self.files:
                return upload(uploaded)
            return uploaded

        d.addCallback(checkForMore)
        d.addCallback(self.checkTickets)
        d.addCallback(self.uploadFinished)
        return d

    def checkTickets(self, ticket_ids):
        """ Checks if all the tickets are uploaded. """

        def check(ts, photos):

            def parse(rsp):
                newtickets = []
                for ticket in rsp.findall('uploader/ticket'):
                    if ticket.get('complete') == '1':
                        photos.append(ticket.get('photoid'))
                    elif ticket.get('complete') == '2':
                        self.uploadErrors.append(ticket.get('id'))
                    elif ticket.get('complete') == '0':
                        newtickets.append(ticket.get('id'))

                if newtickets:
                    return check(newtickets, photos)
                return photos

            return self.flickr.photos_upload_checkTickets(tickets=(',').join(ts)).addCallback(parse)

        return check(ticket_ids, [])

    def uploadFinished(self, photos):
        self.progressCallback(self.currentFile, 1.0, self.numUploaded, self.numTotal)
        if not self.photoset or not photos:
            d = defer.succeed(True)
        else:
            d = self.createSets(photos)

        def complete(_):
            errorFiles = [ self.ticket2filename[t] for t in self.uploadErrors ]
            return (len(photos), errorFiles)

        d.addCallback(complete)
        return d

    def createSets(self, photos):
        """ Add all uploaded photos to the set. """
        if self.photoset not in self.photosets:
            d = self.flickr.photosets_create(title=self.photoset, primary_photo_id=photos[0])
            del photos[0]
            d.addCallback(lambda rsp: rsp.find('photoset').get('id'))
        else:
            d = defer.succeed(self.photosets[self.photoset])

        def addall2set(id):
            ds = []
            sem = defer.DeferredSemaphore(8)
            for photo in photos:
                d = sem.run(self.flickr.photosets_addPhoto, photoset_id=id, photo_id=photo)
                ds.append(d)

            return defer.DeferredList(ds)

        d.addCallback(addall2set)
        return d

    @property
    def numTotal(self):
        return self.numUploaded + self.numUploading + len(self.files)

    def getProgress(self):
        if not self.uploadStarted:
            return 0.0
        return self.numUploaded / float(self.numTotal)

    def loadPhotoSets(self):

        def got_photosets(rsp):
            self.photosets = {}
            for photoset in rsp.findall('photosets/photoset'):
                self.photosets[photoset.find('title').text] = photoset.get('id')

        return self.flickr.photosets_getList().addCallback(got_photosets)