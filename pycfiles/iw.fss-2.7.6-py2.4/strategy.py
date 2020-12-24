# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/strategy.py
# Compiled at: 2008-10-23 05:55:17
"""
$$
"""
__author__ = ''
__docformat__ = 'restructuredtext'
import re, os, sys
from StringIO import StringIO
from ConfigParser import RawConfigParser
from zope.interface import implements
from DateTime import DateTime
from iw.fss.interfaces import IStrategy
from iw.fss.utils import copy_file, move_file, rm_file

class BaseStorageStrategy:
    """Strategy of how field values are stored on filesystem"""
    __module__ = __name__
    implements(IStrategy)

    def __init__(self, storage_path, backup_path):
        """Initialize strategy

        @param storage_path: Filesystem path where field values are stored
        @param backup_path: Filesystem path where field values are backup
        """
        self.storage_path = storage_path
        self.backup_path = backup_path

    def createSubDirectories(self, path, root_path):
        """Create all sub directories if they don't exist"""
        path = os.path.abspath(path)
        root_path = os.path.abspath(root_path)
        if not path.startswith(root_path):
            raise ValueError, 'Path %s should be a part of %s' % (root_path, path)
        if not os.path.exists(root_path):
            raise ValueError, 'Path %s should exist' % root_path
        if not os.path.exists(path):
            os.makedirs(path)

    def removeSubDirectories(self, path, root_path):
        """Remove all sub directories if they are empty"""
        path = os.path.abspath(path)
        root_path = os.path.abspath(root_path)
        if not path.startswith(root_path):
            raise ValueError, 'Path %s should be a part of %s' % (root_path, path)

        def removeEmptyDirectory(cur_path, root_path):
            if cur_path == root_path:
                return
            if not os.path.exists(cur_path):
                return
            if os.listdir(cur_path):
                return
            os.rmdir(cur_path)
            parent_path = os.path.dirname(cur_path)
            removeEmptyDirectory(parent_path, root_path)

        removeEmptyDirectory(path, root_path)

    def walkOnStorageDirectory(self, **kwargs):
        """Walk on storage directory"""
        raise NotImplementedError('walkOnStorageDirectory')

    def walkOnBackupDirectory(self, **kwargs):
        """Walk on backup directory"""
        raise NotImplementedError('walkOnBackupDirectory')

    def walkOnValueDirectoryPath(self, **kwargs):
        """Get path of directory where the field value is stored"""
        raise NotImplementedError('getValueDirectoryPath')

    def getValueDirectoryPath(self, **kwargs):
        """Get path of directory where the field value is stored"""
        raise NotImplementedError('getValueDirectoryPath')

    def getValueFilename(self, **kwargs):
        """Get filename of the field value on filesystem"""
        raise NotImplementedError('getValueFilename')

    def getValueFilePath(self, **kwargs):
        """Get path of file where the field value is stored"""
        raise NotImplementedError('getValueFilePath')

    def getRDFDirectoryPath(self, **kwargs):
        """Get path of directory where the rdf value is stored"""
        raise NotImplementedError('getRDFDirectoryPath')

    def getRDFFilename(self, **kwargs):
        """Get filename of the rdf value on filesystem"""
        raise NotImplementedError('getRDFFilename')

    def getRDFFilePath(self, **kwargs):
        """Get path of file where the rdf value is stored"""
        raise NotImplementedError('getRDFFilePath')

    def getBackupDirectoryPath(self, **kwargs):
        """Get path of directory where the file value is backup"""
        raise NotImplementedError('getBackupDirectoryPath')

    def getBackupFilename(self, **kwargs):
        """Get filename of the file backup value on filesystem"""
        raise NotImplementedError('getBackupFilename')

    def getBackupFilePath(self, **kwargs):
        """Get path of file where the file value is backup"""
        raise NotImplementedError('getBackupFilePath')

    def setValueFile(self, value, **kwargs):
        """Copy file value on filesystem"""
        raise NotImplementedError('setValueFile')

    def unsetValueFile(self, **kwargs):
        """Remove file value if exists"""
        raise NotImplementedError('unsetValueFile')

    def moveValueFile(self, **kwargs):
        """File properties has changed, move it its new locations"""
        raise NotImplementedError('moveValueFile')

    def restoreValueFile(self, **kwargs):
        """Restore the backup value if exists"""
        raise NotImplementedError('restoreValueFile')

    def copyValueFile(self, **kwargs):
        """Duplicate file value on filesystem"""
        raise NotImplementedError('copyValueFile')


class FlatStorageStrategy(BaseStorageStrategy):
    """All field values are stored in a flat structure

    Filename of these stored values: <uid of content>_<field name>
    Filename of rdf file: <uid of content>_<field name>.rdf
    Filename of backup values: <uid of content>_<field name>.bak
    Rdf files are not backup. They are automatically generated

    Example of storage:
    fssDirectory
    |
    |- f42ad00adb7d4580f929d734bf1ed3ab_image
    |
    |- f42ad00adb7d4580f929d734bf1ed3ab_image.rdf
    |
    |- f42ad00adb7d4580f929d734bf1ed3ab_file
    |
    |- f42ad00adb7d4580f929d734bf1ed3ab_file.rdf

    fssBackupDirectory
    |
    |- 9efeb7638fb35f5f9b9955da3e2dbfec_file.bak
    """
    __module__ = __name__

    def getValueDirectoryPath(self, **kwargs):
        """Get path of directory where the field value is stored"""
        return self.storage_path

    def getValueFilename(self, **kwargs):
        """Get filename of the field value on filesystem"""
        if kwargs.get('version', None) is not None:
            return '%s_%s.%s' % (kwargs['uid'], kwargs['name'], kwargs['version'])
        return '%s_%s' % (kwargs['uid'], kwargs['name'])

    def getValueFilePath(self, **kwargs):
        """Get path of file where the field value is stored"""
        return os.path.join(self.getValueDirectoryPath(**kwargs), self.getValueFilename(**kwargs))

    def getRDFDirectoryPath(self, **kwargs):
        """Get path of directory where the rdf value is stored"""
        return self.getValueDirectoryPath(**kwargs)

    def getRDFFilename(self, **kwargs):
        """Get filename of the rdf value on filesystem"""
        if kwargs.get('version', None) is not None:
            return '%s_%s.%s.rdf' % (kwargs['uid'], kwargs['name'], kwargs['version'])
        return '%s_%s.rdf' % (kwargs['uid'], kwargs['name'])

    def getRDFFilePath(self, **kwargs):
        """Get path of file where the rdf value is stored"""
        return os.path.join(self.getRDFDirectoryPath(**kwargs), self.getRDFFilename(**kwargs))

    def getBackupDirectoryPath(self, **kwargs):
        """Get path of directory where the file value is backup"""
        return self.backup_path

    def getBackupFilename(self, **kwargs):
        """Get filename of the file backup value on filesystem"""
        if kwargs.get('version', None) is not None:
            return '%s_%s.%s.bak' % (kwargs['uid'], kwargs['name'], kwargs['version'])
        return '%s_%s.bak' % (kwargs['uid'], kwargs['name'])

    def getBackupFilePath(self, **kwargs):
        """Get path of file where the file value is backup"""
        return os.path.join(self.getBackupDirectoryPath(**kwargs), self.getBackupFilename(**kwargs))

    def walkOnUIDDirectory(self, path, reg, **kwargs):
        """Return a list of dictionnary.

        Each dictionnary has this structure:
        - uid -> uid of linked content
        - name -> name of field
        - modified -> DateTime of last modification
        - path -> File path
        """
        items = []
        node_ids = os.listdir(path)
        for node_id in node_ids:
            match = reg.match(node_id)
            if match is None:
                continue
            uid = match.group('uid')
            name = match.group('name')
            file_path = os.path.join(path, node_id)
            modified = os.path.getmtime(file_path)
            size = os.path.getsize(file_path)
            item = {}
            item['uid'] = uid
            item['name'] = name
            item['fs_path'] = file_path
            item['modified'] = DateTime(modified)
            item['size'] = size
            items.append(item)

        return items

    def walkOnStorageDirectory(self, **kwargs):
        """Walk on storage directory"""
        reg = re.compile('^(?P<uid>.{32})_(?P<name>[^.]*)$')
        return self.walkOnUIDDirectory(self.storage_path, reg)

    def walkOnBackupDirectory(self, **kwargs):
        """Walk on backup directory"""
        reg = re.compile('^(?P<uid>.{32})_(?P<name>[^.]*).bak$')
        return self.walkOnUIDDirectory(self.backup_path, reg)

    def setValueFile(self, value, **kwargs):
        """Copy file value on filesystem"""
        buffer = StringIO(value)
        copy_file(buffer, self.getValueFilePath(**kwargs))
        buffer.close()

    def unsetValueFile(self, **kwargs):
        """Remove file value if exists"""
        if kwargs.get('is_moved', False):
            return
        value_path = self.getValueFilePath(**kwargs)
        if not os.path.exists(value_path):
            return
        backup_path = self.getBackupFilePath(**kwargs)
        move_file(value_path, backup_path)

    def restoreValueFile(self, **kwargs):
        """Restore the backup value if exists"""
        backup_path = self.getBackupFilePath(**kwargs)
        if not os.path.exists(backup_path):
            return
        value_path = self.getValueFilePath(**kwargs)
        move_file(backup_path, value_path)

    def moveValueFile(self, **kwargs):
        """File properties has changed, move it its new locations"""
        new_kwargs = kwargs.copy()
        del new_kwargs['uid']
        src_path = self.getValueFilePath(uid=kwargs['src_uid'], **new_kwargs)
        if not os.path.exists(src_path):
            return
        dst_path = self.getValueFilePath(**kwargs)
        move_file(src_path, dst_path)

    def copyValueFile(self, **kwargs):
        """Duplicate file value on filesystem"""
        src_path = self.getValueFilePath(uid=kwargs['src_uid'], name=kwargs['name'])
        if not os.path.exists(src_path):
            return
        dst_path = self.getValueFilePath(**kwargs)
        copy_file(src_path, dst_path)

    def setRDFFile(self, value, **kwargs):
        """Copy rdf file on filesystem"""
        buffer = StringIO(value)
        copy_file(buffer, self.getRDFFilePath(**kwargs))
        buffer.close()

    def unsetRDFFile(self, **kwargs):
        """Remove rdf file if exists"""
        if kwargs.get('is_moved', False):
            return
        rdf_path = self.getRDFFilePath(**kwargs)
        if not os.path.exists(rdf_path):
            return
        rm_file(rdf_path)


class DirectoryStorageStrategy(FlatStorageStrategy):
    """All field values are stored in a directory structure.
    Sub directories are defined on two level.
    First level of directory uses the 2 characters of content uid.
    Second level of directory uses the 4 characters of content uid.
    Backup files are stored in a flat structure.

    Filename of these stored values: <uid of content>_<field name>
    Filename of rdf file: <uid of content>_<field name>.rdf
    Filename of backup values: <uid of content>_<field name>.bak
    Rdf files are not backup. They are automatically generated

    Example of storage:
    fssDirectory
    |
    |- f42
       |
       |- f42ad
          |
          |- f42ad00adb7d4580f929d734bf1ed3ab_image
          |
          |- f42ad00adb7d4580f929d734bf1ed3ab_image.rdf
          |
          |- f42ad00adb7d4580f929d734bf1ed3ab_file
          |
          |- f42ad00adb7d4580f929d734bf1ed3ab_file.rdf

    fssBackupDirectory
    |
    |- 9efeb7638fb35f5f9b9955da3e2dbfec_file.bak
    """
    __module__ = __name__

    def walkOnStorageDirectory(self, **kwargs):
        """Walk on storage directory"""
        reg = re.compile('^(?P<uid>.{32})_(?P<name>[^.]*)$')
        paths = []
        for (root, dirs, files) in os.walk(self.storage_path):
            if dirs:
                continue
            paths.append(root)

        items = []
        for path in paths:
            items.extend(self.walkOnUIDDirectory(path, reg))

        return items

    def getValueDirectoryPath(self, **kwargs):
        """Get path of directory where the field value is stored"""
        uid = kwargs['uid']
        first_level = uid[:2]
        second_level = uid[:4]
        return os.path.join(self.storage_path, first_level, second_level)

    def setValueFile(self, value, **kwargs):
        """Copy file value on filesystem"""
        self.createSubDirectories(self.getValueDirectoryPath(**kwargs), self.storage_path)
        FlatStorageStrategy.setValueFile(self, value, **kwargs)

    def unsetValueFile(self, **kwargs):
        """Remove file value if exists"""
        FlatStorageStrategy.unsetValueFile(self, **kwargs)
        self.removeSubDirectories(self.getValueDirectoryPath(**kwargs), self.storage_path)

    def restoreValueFile(self, **kwargs):
        """Restore the backup value if exists"""
        self.createSubDirectories(self.getValueDirectoryPath(**kwargs), self.storage_path)
        FlatStorageStrategy.restoreValueFile(self, **kwargs)

    def moveValueFile(self, **kwargs):
        """File properties has changed, move it to its new location"""
        new_kwargs = kwargs.copy()
        del new_kwargs['uid']
        self.createSubDirectories(self.getValueDirectoryPath(uid=kwargs['uid'], **new_kwargs), self.storage_path)
        FlatStorageStrategy.moveValueFile(self, **kwargs)
        self.removeSubDirectories(self.getValueDirectoryPath(uid=kwargs['src_uid'], **new_kwargs), self.storage_path)

    def copyValueFile(self, **kwargs):
        """Duplicate file value on filesystem"""
        self.createSubDirectories(self.getValueDirectoryPath(**kwargs), self.storage_path)
        FlatStorageStrategy.copyValueFile(self, **kwargs)

    def setRDFFile(self, value, **kwargs):
        """Copy rdf file on filesystem"""
        self.createSubDirectories(self.getRDFDirectoryPath(**kwargs), self.storage_path)
        FlatStorageStrategy.setRDFFile(self, value, **kwargs)

    def unsetRDFFile(self, **kwargs):
        """Remove rdf file if exists"""
        FlatStorageStrategy.unsetRDFFile(self, **kwargs)
        self.removeSubDirectories(self.getRDFDirectoryPath(**kwargs), self.storage_path)


class SiteStorageStrategy(DirectoryStorageStrategy):
    """All field values are stored in a directory structure mirroring structure
    of PloneSite.
    Backup files are stored in a flat structure.

    Filename of these stored values: Filename of field value or field name
    if not defined
    Filename of rdf file: <field name>.rdf
    Filename of backup values: <uid of content>_<field name>.bak
    Rdf files are not backup. They are automatically generated

    Example of storage:
    fssDirectory
    |
    |- members
       |
       |- john
          |
          |- dummy-document
             |
             |- image
             |  |
             |  |- moutain.jpg
             |  |
             |  |- image.rdf
             |
             |- file
                |
                |- diary.odt
                |
                |- file.rdf

    fssBackupDirectory
    |
    |- 9efeb7638fb35f5f9b9955da3e2dbfec_file.bak
    """
    __module__ = __name__

    def walkOnStorageDirectory(self, **kwargs):
        """Walk on storage directory"""
        paths = []
        root_path = os.path.abspath(self.storage_path)
        for (root, dirs, files) in os.walk(root_path):
            if dirs:
                continue
            paths.append(root)

        items = []
        for path in paths:
            name = os.path.basename(path)
            obj_path = os.path.dirname(path)[len(root_path) + 1:]
            if sys.platform == 'win32':
                obj_path = obj_path.replace('\\', '/')
            node_ids = os.listdir(path)
            rdf_filename = self.getRDFFilename(name=name)
            for node_id in node_ids:
                if node_id == rdf_filename:
                    continue
                file_path = os.path.join(path, node_id)
                modified = os.path.getmtime(file_path)
                size = os.path.getsize(file_path)
                item = {}
                item['path'] = obj_path
                item['name'] = name
                item['fs_path'] = file_path
                item['modified'] = DateTime(modified)
                item['size'] = size
                items.append(item)

        return items

    def getValueFilename(self, **kwargs):
        """Get filename of the field value on filesystem"""
        filename = kwargs.get('title', '')
        if not filename:
            filename = kwargs['name']
        if kwargs.get('version', None) is not None:
            filename = '%s.%s' % (filename, kwargs['version'])
        rdf_filename = self.getRDFFilename(**kwargs)
        if rdf_filename == filename:
            filename = '-%s' % filename
        return filename

    def getValueDirectoryPath(self, **kwargs):
        """Get path of directory where the field value is stored"""
        path_list = []
        path_list.append(self.storage_path)
        path_list.extend(kwargs['path'].split('/'))
        path_list.append(kwargs['name'])
        return os.path.join(*path_list)

    def getRDFFilename(self, **kwargs):
        """Get filename of the rdf value on filesystem"""
        if kwargs.get('version', None) is not None:
            return '%s.%s.rdf' % (kwargs['name'], kwargs['version'])
        return '%s.rdf' % kwargs['name']

    def copyValueFile(self, **kwargs):
        """Duplicate file value on filesystem"""
        src_path = self.getValueFilePath(uid=kwargs['src_uid'], path=kwargs['src_path'], name=kwargs['name'], title=kwargs.get('title', ''))
        if not os.path.exists(src_path):
            return
        dst_path = self.getValueFilePath(**kwargs)
        self.createSubDirectories(self.getValueDirectoryPath(**kwargs), self.storage_path)
        copy_file(src_path, dst_path)

    def setValueFile(self, value, **kwargs):
        """Copy file value on filesystem"""
        path = self.getValueDirectoryPath(**kwargs)
        if os.path.exists(path):
            rdf_filename = self.getRDFFilename(**kwargs)
            for filename in os.listdir(path):
                if filename == rdf_filename:
                    continue
                file_path = os.path.join(path, filename)
                rm_file(file_path)

        DirectoryStorageStrategy.setValueFile(self, value, **kwargs)

    def unsetValueFile(self, **kwargs):
        """Remove file value if exists"""
        if kwargs.has_key('is_moved'):
            del kwargs['is_moved']
        DirectoryStorageStrategy.unsetValueFile(self, **kwargs)

    def unsetRDFFile(self, **kwargs):
        """Remove rdf file if exists"""
        if kwargs.has_key('is_moved'):
            del kwargs['is_moved']
        DirectoryStorageStrategy.unsetRDFFile(self, is_deleted=True, **kwargs)


class SiteStorageStrategy2(DirectoryStorageStrategy):
    """All field values are stored in a directory structure mirroring structure
    of PloneSite.
    Backup files are stored in a flat structure.

    Filename of these stored values: Filename of field value or field name
    if not defined
    Filename of rdf file: <field filename>.rdf
    Filename of backup values: <uid of content>_<field name>.bak
    Rdf files are not backup. They are automatically generated

    Example of storage:
    fssDirectory
    |
    |- members
       |
       |- john
          |
          |- dummy-document
             |
             |- fss.cfg
             |
             |- moutain.jpg
             |
             |- mountain.jpg.rdf
             |
             |- diary.odt
             |
             |- diary.odt.rdf

    fssBackupDirectory
    |
    |- 9efeb7638fb35f5f9b9955da3e2dbfec_file.bak
    """
    __module__ = __name__
    cfg_filename = 'fss.cfg'
    cfg_filename_section = 'FILENAME'

    def walkOnStorageDirectory(self, **kwargs):
        """Walk on storage directory"""
        paths = []
        root_path = os.path.abspath(self.storage_path)
        for (root, dirs, files) in os.walk(root_path):
            if dirs:
                continue
            paths.append(root)

        items = []
        for path in paths:
            cfg_path = os.path.join(path, self.cfg_filename)
            if not os.path.exists(cfg_path):
                continue
            config = RawConfigParser()
            fd = open(cfg_path, 'r')
            try:
                config.readfp(fd)
            finally:
                fd.close()
            obj_path = path[len(root_path) + 1:]
            if sys.platform == 'win32':
                obj_path = obj_path.replace('\\', '/')
            names = config.options(self.cfg_filename_section)
            for name in names:
                filename = config.get(self.cfg_filename_section, name)
                file_path = os.path.join(path, filename)
                modified = os.path.getmtime(file_path)
                size = os.path.getsize(file_path)
                item = {}
                item['path'] = obj_path
                item['name'] = name
                item['fs_path'] = file_path
                item['modified'] = DateTime(modified)
                item['size'] = size
                items.append(item)

        return items

    def getFilenameInConfigFile(self, root_path, name):
        """Get filename field association in config file

        @root_path: Path where config file is stored
        @param name: Field name
        """
        path = os.path.join(root_path, self.cfg_filename)
        if not os.path.exists(path):
            return
        fd = open(path, 'r')
        value = None
        try:
            config = RawConfigParser()
            config.readfp(fd)
            if config.has_section(self.cfg_filename_section) and config.has_option(self.cfg_filename_section, name):
                value = config.get(self.cfg_filename_section, name)
        finally:
            fd.close()
        return value

    def setFilenameInConfigFile(self, root_path, name, filename):
        """Add new filename association in config file

        @root_path: Path where config file is stored
        @param name: Field name
        @param filename: Filename of value stored in field
        """
        path = os.path.join(root_path, self.cfg_filename)
        config = RawConfigParser()
        if os.path.exists(path):
            fd = open(path, 'r')
            try:
                config.readfp(fd)
            finally:
                fd.close()
        if not config.has_section(self.cfg_filename_section):
            config.add_section(self.cfg_filename_section)
        config.set(self.cfg_filename_section, name, filename)
        fd = open(path, 'w')
        try:
            config.write(fd)
        finally:
            fd.close()

    def unsetFilenameInConfigFile(self, root_path, name):
        """Remove filename field association in config file

        @root_path: Path where config file is stored
        @param name: Field name
        """
        path = os.path.join(root_path, self.cfg_filename)
        if not os.path.exists(path):
            return
        config = RawConfigParser()
        fd = open(path, 'r')
        try:
            config.readfp(fd)
        finally:
            fd.close()
        if config.has_section(self.cfg_filename_section):
            config.remove_option(self.cfg_filename_section, name)
        if not config.options(self.cfg_filename_section):
            rm_file(path)
        else:
            fd = open(path, 'w')
            try:
                config.write(fd)
            finally:
                fd.close()

    def getValueFilename(self, **kwargs):
        """Get filename of the field value on filesystem"""
        path = self.getValueDirectoryPath(**kwargs)
        name = kwargs['name']
        if os.path.exists(path):
            filename = self.getFilenameInConfigFile(path, name)
            if filename is not None:
                return filename
        filename = kwargs.get('title', '')
        if not filename:
            filename = name
        if kwargs.get('version', None) is not None:
            filename = '%s.%s' % (filename, kwargs['version'])
        if not os.path.exists(path):
            return filename
        node_ids = os.listdir(path)
        orig_filename = filename
        filename_created = False
        index = 0
        while not filename_created:
            if filename not in node_ids:
                filename_created = True
            else:
                index += 1
                filename = '%d-%s' % (index, filename)

        return filename

    def getValueDirectoryPath(self, **kwargs):
        """Get path of directory where the field value is stored"""
        path_list = []
        path_list.append(self.storage_path)
        path_list.extend(kwargs['path'].split('/'))
        return os.path.join(*path_list)

    def getRDFFilename(self, **kwargs):
        """Get filename of the rdf value on filesystem"""
        if kwargs.get('version', None) is not None:
            return '%s.%s.rdf' % (self.getValueFilename(**kwargs), kwargs['version'])
        return '%s.rdf' % self.getValueFilename(**kwargs)

    def setValueFile(self, value, **kwargs):
        """Copy file value on filesystem"""
        name = kwargs['name']
        path = self.getValueDirectoryPath(**kwargs)
        file_path = self.getValueFilePath(**kwargs)
        if os.path.exists(file_path):
            rm_file(file_path)
        rdf_path = self.getRDFFilePath(**kwargs)
        if os.path.exists(rdf_path):
            rm_file(rdf_path)
        self.unsetFilenameInConfigFile(path, name)
        filename = self.getValueFilename(**kwargs)
        self.createSubDirectories(path, self.storage_path)
        self.setFilenameInConfigFile(path, name, filename)
        FlatStorageStrategy.setValueFile(self, value, **kwargs)

    def unsetValueFile(self, **kwargs):
        """Remove file value if exists"""
        name = kwargs['name']
        path = self.getValueDirectoryPath(**kwargs)
        if kwargs.has_key('is_moved'):
            del kwargs['is_moved']
        FlatStorageStrategy.unsetValueFile(self, **kwargs)
        self.unsetRDFFile(**kwargs)
        self.unsetFilenameInConfigFile(path, name)
        self.removeSubDirectories(path, self.storage_path)

    def restoreValueFile(self, **kwargs):
        """Restore the backup value if exists"""
        name = kwargs['name']
        path = self.getValueDirectoryPath(**kwargs)
        filename = self.getValueFilename(**kwargs)
        self.createSubDirectories(path, self.storage_path)
        self.setFilenameInConfigFile(path, name, filename)
        FlatStorageStrategy.restoreValueFile(self, **kwargs)

    def copyValueFile(self, **kwargs):
        """Duplicate file value on filesystem"""
        src_path = self.getValueFilePath(uid=kwargs['src_uid'], path=kwargs['src_path'], name=kwargs['name'], title=kwargs.get('title', ''))
        if not os.path.exists(src_path):
            return
        name = kwargs['name']
        path = self.getValueDirectoryPath(**kwargs)
        filename = self.getValueFilename(**kwargs)
        self.createSubDirectories(path, self.storage_path)
        self.setFilenameInConfigFile(path, name, filename)
        dst_path = self.getValueFilePath(**kwargs)
        copy_file(src_path, dst_path)