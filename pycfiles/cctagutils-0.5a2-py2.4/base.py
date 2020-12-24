# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/cctagutils/handler/base.py
# Compiled at: 2007-03-15 10:29:40


class BaseMetadata(object):
    __module__ = __name__

    def __init__(self, filename):
        self.filename = filename

    def getTitle(self):
        raise NotImplementedError()

    def getArtist(self):
        raise NotImplementedError()

    def getYear(self):
        raise NotImplementedError()

    def getMetadataUrl(self):
        """Return the URL where more metadata on this file may be found;
        this is provided by WCOP in ID3 and the webStatement in XMP."""
        pass

    def getClaim(self):
        raise NotImplementedError()

    def setClaim(self, claim):
        raise NotImplementedError()

    def getLicense(self):
        """Return the license URL."""
        raise NotImplementedError()

    def embed(self, license, verification, year, holder):
        """Embed a license claim in the audio file."""
        raise NotImplementedError()

    def isWritable(self):
        """Returns true if the user has permission to change the metadata."""
        raise NotImplementedError()

    def verify(self):
        """Attempt to verify the embedded claim.  Return one of the VERIFY_*
        constants defined in cctagutil."""
        import cctagutils.lookup
        return cctagutils.lookup.verify(self.filename)

    def properties(self):
        """Return a sequence of property keys for metadata on this object."""
        return []

    def __getitem__(self, key):
        """Return an additional metadata property for this object."""
        raise KeyError('Unknown key %s' % key)