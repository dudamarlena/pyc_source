# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/configfiles/local/filemon.py
# Compiled at: 2018-11-05 09:19:27
# Size of source mod 2**32: 3446 bytes
__doc__ = '\nFileManager:\n\ndeals with the files/ directory, as well as the saving/loading/restoring of config files\nbetween script runs.\n\n'
import os, shutil
from gzip import GzipFile
from .hashes import get_file_hash

class FileMon:

    def __init__(self, db):
        self.db = db

    def open(self, fhash, mode='rb'):
        """
        Open a file in the database by its hash
        """
        final_path = os.path.join(self.db.load_file, 'files', fhash + '.gz')
        return GzipFile(final_path, mode)

    def open_version(self, fname, mode, version=None):
        """
        Open the latest stored version of a file (override None for custom)
        """
        if version is None:
            version = self.db.get_at()
        fhash = self.db.index['files'][fname]['chain'][version]
        return self.open(fhash, mode)

    def open_local(self, fname, *args, **kwargs):
        """
        Open a file in the domain this configfiles refers to.

        *args and **kwargs go into open()
        """
        final_path = os.path.join(os.path.dirname(self.db.load_file), fname)
        return open(final_path, *args, **kwargs)

    def record_file(self, fname):
        """
        Record the current content in fname for the current at
        """
        hashname = get_file_hash(self.db.current_remote, fname, self.db.get_at())
        if os.path.exists(os.path.join(os.path.dirname(self.db.load_file), fname)):
            with self.open(hashname, 'wb') as (sink):
                with self.open_local(fname, 'rb') as (source):
                    shutil.copyfileobj(source, sink)
            self.db.index['files'][fname]['chain'][self.db.get_at()] = hashname
        else:
            self.db.index['files'][fname]['chain'][self.db.get_at()] = ''
        self.db.write()

    def record_original(self, fname, addedin):
        """
        Record the original version of fname.
        """
        hashname = get_file_hash(self.db.current_remote, fname, addedin + 'orig')
        if fname in self.db.index['files']:
            chain = self.db.index['files'][fname]['chain']
        else:
            chain = {}
        if os.path.exists(os.path.join(os.path.dirname(self.db.load_file), fname)):
            with self.open(hashname, 'wb') as (sink):
                with self.open_local(fname, 'rb') as (source):
                    shutil.copyfileobj(source, sink)
            self.db.index['files'][fname] = {'chain':chain,  'original':hashname, 
             'newin':addedin}
        else:
            self.db.index['files'][fname] = {'chain':chain,  'original':'', 
             'newin':addedin}
        self.db.write()

    def restore_version(self, fname, version):
        """
        Restore a version of a file
        
        :param fname: file name
        :param version: hash of version, or None for original
        """
        if version is None:
            hashname = self.db.index['files'][fname]['original']
        else:
            hashname = self.db.index['files'][fname]['chain'][version]
        if hashname is '':
            os.remove(os.path.join(os.path.dirname(self.db.load_file), fname))
        else:
            with self.open(hashname, 'rb') as (source):
                with self.open_local(fname, 'wb') as (sink):
                    shutil.copyfileobj(source, sink)


from .db import DotConfigFiles