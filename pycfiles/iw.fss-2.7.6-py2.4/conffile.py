# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/conffile.py
# Compiled at: 2008-10-23 05:55:17
"""
The FileSystemStorage tool
$Id: conffile.py 66391 2008-06-09 17:38:35Z glenfant $
"""
__version__ = '$Revision$'
__docformat__ = 'restructuredtext'
import time
from zope.interface import implements
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from iw.fss.utils import rm_file
from iw.fss.FileSystemStorage import FileSystemStorage
from iw.fss.utils import getFieldValue
from iw.fss.config import ZCONFIG
from iw.fss import strategy as fss_strategy
from iw.fss.interfaces import IConf
_strategy_map = {'flat': fss_strategy.FlatStorageStrategy, 'directory': fss_strategy.DirectoryStorageStrategy, 'site1': fss_strategy.SiteStorageStrategy, 'site2': fss_strategy.SiteStorageStrategy2}

class ConfFile(object):
    """Tool for FileSystem storage"""
    __module__ = __name__
    implements(IConf)

    @property
    def fssPropertySheet(self):
        portal_properties = getToolByName(getSite(), 'portal_properties')
        return portal_properties.filesystemstorage_properties

    def isRDFEnabled(self):
        """Returns true if RDF is automaticaly generated when file added"""
        return bool(self.fssPropertySheet.rdf_enabled)

    def enableRDF(self, enabled):
        """Enable rdf or not"""
        self.fssPropertySheet.rdf_enabled = bool(enabled)

    rdfEnabled = property(isRDFEnabled, enableRDF)

    def getRDFScript(self):
        """Returns rdf script used to generate RDF on files"""
        return self.fssPropertySheet.rdf_script

    def setRDFScript(self, rdf_script):
        """Set rdf script used to generate RDF on files"""
        self.fssPropertySheet.rdf_script = rdf_script.strip()

    rdfScript = property(getRDFScript, setRDFScript)

    def usesGlobalConfig(self):
        """If the global configuration is in use for this site"""
        portal = getSite()
        return ZCONFIG.usesGlobalConfig(portal)

    def getStorageStrategy(self):
        """Returns the storage strategy"""
        global _strategy_map
        portal = getSite()
        portal_path = ('/').join(portal.getPhysicalPath())
        strategy_class = _strategy_map[ZCONFIG.storageStrategyForSite(portal_path)]
        return strategy_class(ZCONFIG.storagePathForSite(portal_path), ZCONFIG.backupPathForSite(portal_path))

    def getUIDToPathDictionnary(self):
        """Returns a dictionnary

        For one uid (key) give the correct path (value)
        """
        ctool = getToolByName(getSite(), 'uid_catalog')
        brains = ctool(REQUEST={})
        return dict([ (x['UID'], x.getPath()) for x in brains ])

    def getPathToUIDDictionnary(self):
        """Returns a dictionnary

        For one path (key) give the correct UID (value)
        """
        ctool = getToolByName(getSite(), 'uid_catalog')
        brains = ctool(REQUEST={})
        return dict([ (x.getPath(), x['UID']) for x in brains ])

    def getFSSBrains(self, items):
        """Returns a dictionnary.

        For one uid, returns a dictionnary containing of fss item stored on
        filesystem:
        - uid: UID of content
        - path: Path of content
        - name: Name of field stored on filesystem
        - size: Size in octets of field value stored on filesystem
        - fs_path: Path on filesystem where the field value is stored
        """
        if not items:
            return []
        if not items[0].has_key('uid'):
            path_to_uid = self.getPathToUIDDictionnary()
            for item in items:
                item['uid'] = path_to_uid.get(item['path'], None)

        uid_to_path = self.getUIDToPathDictionnary()
        for item in items:
            item['path'] = uid_to_path.get(item['uid'], None)

        return items

    def getStorageBrains(self):
        """Returns a list of brains in storage path"""
        strategy = self.getStorageStrategy()
        items = strategy.walkOnStorageDirectory()
        return self.getFSSBrains(items)

    def getStorageBrainsByUID(self, uid):
        """ Returns a list containing all brains related to fields stored
        on filesystem of object having the specified uid"""
        return [ x for x in self.getStorageBrains() if x['uid'] == uid ]

    def getBackupBrains(self):
        """Returns a list of brains in backup path"""
        strategy = self.getStorageStrategy()
        items = strategy.walkOnBackupDirectory()
        return self.getFSSBrains(items)

    def updateFSS(self):
        """
        Update FileSystem storage
        """
        storage_brains = self.getStorageBrains()
        backup_brains = self.getBackupBrains()
        not_valid_files = tuple([ x for x in storage_brains if x['path'] is None ])
        not_valid_backups = tuple([ x for x in backup_brains if x['path'] is not None ])
        strategy = self.getStorageStrategy()
        for item in not_valid_files:
            strategy.unsetValueFile(**item)

        for item in not_valid_backups:
            strategy.restoreValueFile(**item)

        return (
         len(not_valid_files), len(not_valid_backups))

    def removeBackups(self, max_days):
        """
        Remove backups older than specified days
        """
        backup_brains = self.getBackupBrains()
        valid_backups = [ x for x in backup_brains if x['path'] is None ]
        current_time = time.time()
        for item in valid_backups:
            one_day = 86400
            modified = item['modified']
            seconds = int(current_time) - int(modified.timeTime())
            days = int(seconds / one_day)
            if days >= max_days:
                rm_file(item['fs_path'])

        return

    def updateRDF(self):
        """Add RDF files to fss files"""
        rdf_script = self.getRDFScript()
        storage_brains = self.getStorageBrains()
        strategy = self.getStorageStrategy()
        for item in storage_brains:
            instance_path = item['path']
            if instance_path is None:
                continue
            try:
                instance = self.restrictedTraverse(instance_path)
            except AttributeError:
                continue

            name = item['name']
            field = instance.getField(name)
            if field is None:
                continue
            storage = field.getStorage(instance)
            if not isinstance(storage, FileSystemStorage):
                continue
            info = storage.getFSSInfo(name, instance)
            if info is None:
                continue
            rdf_value = info.getRDFValue(name, instance, rdf_script=rdf_script)
            strategy.setRDFFile(rdf_value, uid=item['uid'], name=name)

        return

    def getFSSItem(self, instance, name):
        """Get value of fss item.
        This method is called from fss_get script.

        @param instance: Object containing FSS item
        @param name: Name of FSS item to get
        """
        return getFieldValue(instance, name)