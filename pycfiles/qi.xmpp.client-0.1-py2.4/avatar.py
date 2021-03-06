# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/xmpp/client/avatar.py
# Compiled at: 2008-08-01 13:19:37
import sha, base64, os, os.path, sys, Image, StringIO
from twisted.words.xish.domish import Element
from qi.xmpp.botfarm.logutil import LogEvent, ERROR

def convertToPNG(imageData):
    inbuff = StringIO.StringIO(imageData)
    outbuff = StringIO.StringIO()
    Image.open(inbuff).save(outbuff, 'PNG')
    outbuff.seek(0)
    imageData = outbuff.read()
    return imageData


def parsePhotoEl(photo):
    """ Pass the photo element as an avatar, returns the avatar imageData """
    imageData = ''
    imageType = ''
    for e in photo.elements():
        if e.name == 'BINVAL':
            imageData = base64.decodestring(e.__str__())
        elif e.name == 'TYPE':
            imageType = e.__str__()

    if imageType != 'image/png':
        imageData = convertToPNG(imageData)
    return imageData


def getDefaultAvatarData(filename):
    if os.path.isfile(filename):
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        return data
    else:
        LogEvent(ERROR, 'Could not load default avatar. Exiting...')
        sys.exit(1)


class Avatar:
    """ 
        Represents an Avatar. Does not store the image in memory.       
        """
    __module__ = __name__

    def __init__(self, imageData, avatarStorage):
        self.__imageHash = sha.sha(imageData).hexdigest()
        self.__avatarStorage = avatarStorage

    def getImageHash(self):
        """ Returns the SHA1 hash of the avatar. """
        return self.__imageHash

    def getImageData(self):
        """ Returns this Avatar's imageData. This loads data from a file. """
        return self.__avatarStorage.getImageData(self.__imageHash)

    def makePhotoElement(self):
        """ Returns an XML Element that can be put into the vCard. """
        photo = Element((None, 'PHOTO'))
        cType = photo.addElement('TYPE')
        cType.addContent('image/png')
        binval = photo.addElement('BINVAL')
        binval.addContent(base64.encodestring(self.getImageData()).replace('\n', ''))
        return photo

    def makeDataElement(self):
        """ Returns an XML Element that can be put into a jabber:x:avatar IQ stanza. """
        data = Element((None, 'data'))
        data['mimetype'] = 'image/png'
        data.addContent(base64.encodestring(self.getImageData()).replace('\n', ''))
        return data

    def __eq__(self, other):
        return other and self.__imageHash == other.__imageHash


class AvatarStorage:
    """
        Non-persistent RAM storage for Avatars
        """
    __module__ = __name__

    def __init__(self):
        self._avatarData = {}

    def setAvatar(self, imageData):
        avatar = Avatar(imageData, self)
        self._avatarData[avatar.getImageHash()] = imageData
        return avatar.getImageHash()

    def hasAvatar(self, key):
        return self._avatarData.has_key(key)

    def getAvatar(self, key):
        imageData = self.getAvatarData(key)
        if imageData:
            return Avatar(imageData, self)
        return

    def getAvatarData(self, key):
        try:
            return self._avatarData[key]
        except:
            return

        return

    def saveToDisk(self, key, filename=None):
        filename = filename or key + '.png'
        try:
            imageData = self._avatarData[key]
        except:
            return

        try:
            f = open(filename, 'wb')
            f.write(imageData)
            f.close()
        except (OSError, IOError), e:
            return