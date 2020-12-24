# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webdb/files/dispatcher.py
# Compiled at: 2018-02-22 05:39:39
# Size of source mod 2**32: 5014 bytes
"""
File dispatchers for serving files for web applications.
"""
from abc import abstractmethod, ABCMeta
from .file import FileOverlay
import os, logging
logger = logging.getLogger(__name__)

class AbstractFileDispatcher(metaclass=ABCMeta):
    __doc__ = '\n\tAbstract base class for file dispatchers.\n\t'

    @abstractmethod
    def dispatch_file(self, path, *args):
        """
                Dispatch the file. This **must always** return 
                a ``FileOverlay``. Even if the file must not be accessed,
                or does not exist. In this case the ``modes`` must be emtpy.
                """
        pass

    def cleanup_path(self, path):
        """
                Clean up the path. Remove any ".."s and a leading "/".

                ``dispatch_file`` **must** call this method before actually dispatching the
                file.
                """
        if path[0] == '/':
            path = path[1:]
        return path.replace('..', '')


class UserFileDispatcher(AbstractFileDispatcher):
    __doc__ = '\n\tThis file dispatcher has a seperated path for\n\tevery user. The user is allowed to do anything\n\tin this path (read, write, create, create parents).\n\n\tOnly use this for "reliable" clients.\n\t'

    def __init__(self, root):
        self._root = root

    def dispatch_file(self, path, username):
        path = self.cleanup_path(path)
        root = os.path.join(self._root, username)
        return FileOverlay(path, root, 'rwcp', path)


class QuotaUserFileDispatcher(UserFileDispatcher):
    __doc__ = '\n\tThis file dispatcher has a seperated path for\n\tevery user. The user is allowed to do anything\n\tin this path (read, write, create, create parents).\n\n\tThis file dispatcher will refuse changes, if a quota has\n\tbeen exceeded.\n\n\tOnly use this for "semi reliable" clients.\n\t'

    def __init__(self, root, quota):
        UserFileDispatcher.__init__(self, root)
        self._quota = quota

    def dispatch_file(self, path, username):
        path = self.cleanup_path(path)
        root = os.path.join(self._root, username)
        current_size = 0
        for directory in os.walk(root):
            for f in directory[1]:
                if not os.path.isfile(f):
                    pass
                else:
                    current_size += os.stat(f).st_size

        return FileOverlay(path, root, 'rwcp', path, self._quota - current_size)


class SQLFileDispatcher(AbstractFileDispatcher):
    __doc__ = '\n\tThis is a nice dispatcher for controlled environments,\n\tsuch as sharing files between users or a limited set of \n\tfiles.\n\n\tThe dispatcher looks up the files in a database, dispatchs the real\n\tpath and returns the according FileOverlay.\n\n\tThe commands for creating the tables are::\n\n\t\tCREATE TABLE files(path text UNIQUE,\n\t\t\t\tid integer PRIMARY KEY AUTOINCREMENT,\n\t\t\t\tmax_size integer);\n\n\t\tCREATE TABLE access(file_id integer,\n\t\t\t\tusername text,\n\t\t\t\tmodes text);\n\n\t\tCREATE TABLE nicknames(name text PRIMARY KEY,\n\t\t\t\tfile_id integer);\n\n\t\tCREATE INDEX access_index ON access(file_id);\n\n\t\tCREATE TABLE root(root text UNIQUE);\n\n\n\t**NOTE**: This dispatcher does NOT allow creating files.\n\n\t**NOTE**: if ``max_size`` is ``-1`` it will be interpreted as\n\t\t"has no max size".\n\t\t\n\t'

    def __init__(self, db_connection):
        self._db = db_connection
        cursor = self._db.cursor()
        try:
            cursor.execute('SELECT root from root')
            self._root = cursor.fetchone()[0]
        except:
            pass

        if not self._root:
            logger.error('Root directory is not set. You have forgotten to insert the absolute root path into the database.')
            raise IOError('root directory is not set')

    def dispatch_file(self, nickname, username):
        """
                This method looks up the file in the sqlite database and
                resolves the real path, the access rights and the modes

                """
        cursor = self._db.cursor()
        cursor.execute('SELECT file_id FROM nicknames WHERE name = ?', [nickname])
        result = cursor.fetchone()
        if not result:
            raise IOError('unknown file')
        file_id = result[0]
        cursor.execute('SELECT path, max_size FROM files WHERE id = ?', [file_id])
        result = cursor.fetchone()
        if not result:
            logger.error('XXX: file database is desynced. This is most propably a DELETE anomaly there is a nickname pointing to file_id={}, but this file_id is not in files.'.format(file_id))
            raise IOError('unknown file')
        else:
            path, maxsize = result
            if maxsize == -1:
                max_size = float('inf')
            cursor.execute('SELECT modes FROM access WHERE file_id = ? AND username = ?', [file_id, username])
            result = cursor.fetchone()
            if not result:
                modes = ''
            else:
                modes = result[0]
        modes = modes.replace('c', '').replace('p', '')
        logger.info('dispatched: path: {}, root: {}, modes: {}, nickname: {}, maxsize: {}'.format(path, self._root, modes, nickname, max_size))
        return FileOverlay(path, self._root, modes, nickname, max_size)