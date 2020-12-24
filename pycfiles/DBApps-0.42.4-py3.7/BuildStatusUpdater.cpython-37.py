# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/BuildStatusUpdater.py
# Compiled at: 2020-04-14 15:22:04
# Size of source mod 2**32: 4024 bytes
"""
Update Build Status class
"""
import sys, datetime, os
from pathlib import Path
from typing import Tuple, Any, Union
from DBApps.DbAppParser import DbArgNamespace, str2date, DbAppParser, mustExistDirectory
import DBApps.DbApp as DbApp

class UpdateBuildParser(DbAppParser):
    __doc__ = '\n    Parser for the Get Ready Related class\n    Returns a structure containing fields:\n    .drsDbConfig: str (from base class DBAppArgs\n    .outline: bool\n    .printmaster: bool\n    .numResults: int\n    .results: str (which will have to resolve to a pathlib.Path\n    '

    def __init__(self, description, usage):
        """
        Constructor. Sets up the arguments
        """
        super().__init__(description, usage)
        self._parser.add_argument('buildPath', help='Folder containing batch.xml and objects', type=mustExistDirectory)
        self._parser.add_argument('result', help='String representing the result')
        self._parser.add_argument('buildDate', nargs='?', help='build date. Defaults to time this call was made.', default=(datetime.datetime.now()),
          type=str2date)


def volumesForBatch(batchFolder: str) -> list:
    """
    The folders in a batch build project represent the BDRC Volumes in the
    batch build.
    :param batchFolder:
    :return: list of the folders in a batch build project
    """
    for root, dirs, folders in os.walk(batchFolder):
        return dirs


class BuildStatusUpdater(DbApp):
    __doc__ = '\n    Sets up build status updating\n    '

    def __init__(self, options):
        """
        :param: self
        :param: options
        :rtype: object
        """
        try:
            super().__init__(options.drsDbConfig)
        except AttributeError:
            print('argument parsing error: drsDbConfig not found in args')
            sys.exit(1)

        self._options = options

    def DoUpdate(self) -> None:
        """
        Update each volume in the options' buildPath
        """
        self.start_connect()
        conn = self.connection
        uCursor = conn.cursor()
        hadBarf = False
        errVolPersist = ''
        try:
            try:
                buildPath = self._options.buildPath
                for volDir in volumesForBatch(buildPath):
                    fullBuildPath = str(Path(buildPath).resolve())
                    volPath = Path(fullBuildPath, volDir)
                    volFiles, volSize = self.get_tree_values(str(volPath))
                    errVolPersist = volDir
                    uCursor.execute(f'insert ignore BuildPaths ( `BuildPath`) values ("{buildPath}") ;')
                    conn.commit()
                    uCursor.callproc('UpdateBatchBuild', (
                     volDir, buildPath, self._options.buildDate, self._options.result, volFiles, volSize))

            except:
                import sys
                exc = sys.exc_info()
                print('unexpected error for volume, ', errVolPersist, (exc[0]), (exc[1]), file=(sys.stderr))
                conn.rollback()
                hadBarf = True

        finally:
            uCursor.close()
            if not hadBarf:
                conn.commit()
            conn.close()

    def get_tree_values(self, path: str) -> Tuple[(Union[(int, Any)], Union[(int, Any)])]:
        """
        Get file counts on directory and subdirectories.
        :param path: path containing files and folders to be counted
        :returns: total size of files and file count
        :rtype: tuple(int int)
        """
        total = 0
        fileCount = 0
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                subCount, subTotal = self.get_tree_values(entry.path)
            else:
                subTotal = entry.stat(follow_symlinks=False).st_size
                subCount = 1
            total += subTotal
            fileCount += subCount

        return (
         fileCount, total)