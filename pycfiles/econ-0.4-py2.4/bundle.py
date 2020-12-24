# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/store/bundle.py
# Compiled at: 2007-04-18 06:57:54
"""
A DataBundle is a dataset along with its associated metadata

DataBundles are persisted and read from various backends:
  1. local file
  2. web
  3. database

At present only local file is supported.

Local File
**********

A DataBundle serialized to disk appears consists of:
  1. data file named data.<ext> where <ext> is the file type
    * (only ext=csv is presently supported)
  2. metadata file named metadata.txt
    * this file should conform to the python ConfigParser format (RFC 822) and 
    consist of a single section entitle [DEFAULT]
"""
import os, shutil, ConfigParser, uuid

def create(base_path):
    bndl = DataBundle()
    path = os.path.join(base_path, bndl.id)
    bndl.path = path
    bndl.write()
    return bndl


class DataBundle(object):
    """A 'Data Bundle' that is dataset with associated metadata.
    """
    __module__ = __name__

    def set_path(self, value):
        self._path = value
        if self._path:
            self._meta_path = os.path.join(self._path, 'metadata.txt')
            self.data_path = os.path.join(self._path, 'data.csv')

    def get_path(self):
        return self._path

    def del_path(self):
        del self._path

    def set_id(self, value):
        self.metadata['id'] = value

    def get_id(self):
        return self.metadata['id']

    def del_id(self):
        del self.metadata['id']

    path = property(get_path, set_path, del_path)
    id = property(get_id, set_id, del_id)

    def __init__(self, id=None, path=None):
        self.metadata = {}
        if id is None or id == '':
            self.id = str(uuid.uuid4())
        self._meta_path = None
        self.data_path = None
        self.path = path
        return

    def read(self, path):
        self.path = path
        self.id = os.path.basename(path)
        self.readMetadataFromFile(os.path.join(path, 'metadata.txt'))

    def readMetadataFromFile(self, path):
        cfp = ConfigParser.ConfigParser()
        cfp.read(path)
        filemeta = cfp.defaults()
        for key in filemeta:
            self.metadata[key] = filemeta[key]

    def write(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        cfp = ConfigParser.SafeConfigParser(self.metadata)
        fo = file(self._meta_path, 'w')
        cfp.write(fo)
        fo.close()

    def __repr__(self):
        return 'DataBundle: ' + self.id + '\n' + str(self.metadata)