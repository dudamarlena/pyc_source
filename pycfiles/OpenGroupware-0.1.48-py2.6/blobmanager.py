# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/blobmanager.py
# Compiled at: 2012-10-12 07:02:39
import codecs, os, foundation, shelve, pickle
from datetime import datetime
from tempfile import SpooledTemporaryFile
from foundation import STORE_ROOT
from dbfs1 import DBFS1Manager

def blob_manager_for_ds(sky_url, project_id=None):
    if sky_url is None:
        return DBFS1Manager(project_id)
    else:
        driver = sky_url.split(':')[0]
        if driver == 'skyrix':
            return DBFS1Manager(project_id)
        if driver == 'file':
            return SkyFSManager(sky_url)
        raise ('Unknown Data Store driver type of {0}').format(driver)
        return


class BLOBManager(object):
    __slots__ = ()

    @staticmethod
    def _path_from_name(name):
        if isinstance(name, tuple):
            return ('{0}/{1}/{2}').format(foundation.STORE_ROOT, name[0], name[1])
        return ('{0}/{1}').format(foundation.STORE_ROOT, name)

    @staticmethod
    def Create(name, encoding='utf-8', version=None):
        if isinstance(name, tuple) or isinstance(name, list):
            path = foundation.STORE_ROOT
            for chunk in name[:-1]:
                path = ('{0}/{1}').format(path, chunk)
                if os.path.exists(path):
                    pass
                else:
                    os.makedirs(path)

            filename = ('{0}/{1}').format(path, name[-1:][0])
        else:
            filename = ('{0}/{1}').format(foundation.STORE_ROOT, name)
        if encoding == 'binary':
            return open(filename, 'w+b')
        else:
            return codecs.open(filename, 'w+', encoding=encoding)

    @staticmethod
    def Open(name, mode, encoding='utf-8', version='0', create=False):
        filename = ('{0}/{1}').format(foundation.STORE_ROOT, name)
        if os.path.exists(filename):
            if encoding == 'binary':
                return open(filename, mode + 'b')
            else:
                return codecs.open(filename, mode, encoding=encoding)
        elif create:
            return BLOBManager.Create(name.split('/'), encoding=encoding, version=version)
        return

    @staticmethod
    def Close(handle):
        if handle is not None:
            handle.close()
        return

    @staticmethod
    def Delete(name, version='0'):
        if name is None:
            raise Exception('Request to delete an object without name.')
        filename = ('{0}/{1}').format(foundation.STORE_ROOT, name)
        if os.path.exists(filename):
            os.remove(filename)
            return True
        else:
            return False

    @staticmethod
    def ScratchFile(suffix='.data'):
        return SpooledTemporaryFile(max_size=65535, prefix='Coils.', suffix=suffix, dir=('{0}/tmp').format(foundation.STORE_ROOT))

    @staticmethod
    def List(name):
        return os.listdir(('{0}/{1}').format(foundation.STORE_ROOT, name))

    @staticmethod
    def SizeOf(name, version='0'):
        return os.path.getsize(BLOBManager._path_from_name(name))

    @staticmethod
    def Exists(name, version='0'):
        return os.path.exists(BLOBManager._path_from_name(name))

    @staticmethod
    def Created(name):
        return datetime.fromtimestamp(os.path.getctime(BLOBManager._path_from_name(name)))

    @staticmethod
    def Modified(name):
        return datetime.fromtimestamp(os.path.getmtime(BLOBManager._path_from_name(name)))

    @staticmethod
    def OpenShelf(uuid=None, create=False):
        filepath = ('{0}/shelves/{1}.shelve').format(foundation.STORE_ROOT, str(uuid))
        if create:
            if os.path.exists(filepath):
                os.remove(filepath)
        shelf = shelve.open(filepath, flag='c', protocol=pickle.HIGHEST_PROTOCOL)
        return shelf

    @staticmethod
    def DeleteShelf(uuid=None):
        filepath = ('{0}/shelves/{1}.shelve').format(foundation.STORE_ROOT, str(uuid))
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False