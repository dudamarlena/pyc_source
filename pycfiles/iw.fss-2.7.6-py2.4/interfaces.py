# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/interfaces.py
# Compiled at: 2008-10-23 05:55:17
"""
Interfaces exposed here
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import Interface
from zope.annotation.interfaces import IAttributeAnnotatable

class IFSSInfo(IAttributeAnnotatable):
    """Marker for FSSInfo"""
    __module__ = __name__


class IFSSTool(Interface):
    """Marker for FSS tool"""
    __module__ = __name__


class IConf(Interface):
    """Main configuration for fss"""
    __module__ = __name__

    def isRDFEnabled():
        """Returns true if RDF is automaticaly generated when file added"""
        pass

    def enableRDF(enabled):
        """Enable rdf or not"""
        pass

    def getRDFScript():
        """Returns rdf script used to generate RDF on files"""
        pass

    def setRDFScript(rdf_script):
        """Set rdf script used to generate RDF on files"""
        pass

    def getStorageStrategy():
        """Returns the storage strategy"""
        pass

    def getUIDToPathDictionnary():
        """Returns a dictionnary"""
        pass

    def getPathToUIDDictionnary():
        """Returns a dictionnary"""
        pass

    def getFSSBrains(items):
        """Returns a dictionnary."""
        pass

    def getStorageBrains():
        """Returns a list of brains in storage path"""
        pass

    def getStorageBrainsByUID(uid):
        """ Returns a list containing all brains related to fields stored
        on filesystem of object having the specified uid"""
        pass

    def getBackupBrains():
        """Returns a list of brains in backup path"""
        pass

    def updateFSS():
        """Update FileSystem storage"""
        pass

    def removeBackups(max_days):
        """Remove backups older than specified days"""
        pass

    def updateRDF():
        """Add RDF files to fss files"""
        pass

    def getFSSItem(instance, name):
        """Get value of fss item.
        This method is called from fss_get script."""
        pass

    def configletTabs(template_id):
        """Data for drawing tabs in FSS config panel"""
        pass

    def getFSStats():
        """Returns stats on FileSystem storage"""
        pass

    def patchedTypesInfo():
        """A TALES friendly summary of content types with storage changed to FSS"""
        pass

    def siteConfigInfo():
        """A TALES friendly configuration info mapping for this Plone site"""
        pass

    def globalConfigInfo():
        """A TALES friendly configuration info mapping for global configuration"""
        pass

    def formattedReadme():
        """README.txt (reStructuredText) transformed to HTML"""
        pass


class IStrategy(Interface):
    """Defines the way to store files"""
    __module__ = __name__

    def walkOnStorageDirectory(**kwargs):
        """Walk on storage directory"""
        pass

    def walkOnBackupDirectory(**kwargs):
        """Walk on backup directory"""
        pass

    def walkOnValueDirectoryPath(**kwargs):
        """Get path of directory where the field value is stored"""
        pass

    def getValueDirectoryPath(**kwargs):
        """Get path of directory where the field value is stored"""
        pass

    def getValueFilename(**kwargs):
        """Get filename of the field value on filesystem"""
        pass

    def getValueFilePath(**kwargs):
        """Get path of file where the field value is stored"""
        pass

    def getRDFDirectoryPath(**kwargs):
        """Get path of directory where the rdf value is stored"""
        pass

    def getRDFFilename(**kwargs):
        """Get filename of the rdf value on filesystem"""
        pass

    def getRDFFilePath(**kwargs):
        """Get path of file where the rdf value is stored"""
        pass

    def getBackupDirectoryPath(**kwargs):
        """Get path of directory where the file value is backup"""
        pass

    def getBackupFilename(**kwargs):
        """Get filename of the file backup value on filesystem"""
        pass

    def getBackupFilePath(**kwargs):
        """Get path of file where the file value is backup"""
        pass

    def setValueFile(value, **kwargs):
        """Copy file value on filesystem"""
        pass

    def unsetValueFile(**kwargs):
        """Remove file value if exists"""
        pass

    def moveValueFile(**kwargs):
        """File properties has changed, move it its new locations"""
        pass

    def restoreValueFile(**kwargs):
        """Restore the backup value if exists"""
        pass

    def copyValueFile(**kwargs):
        """Duplicate file value on filesystem"""
        pass