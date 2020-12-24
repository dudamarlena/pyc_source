# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/readyRelated.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 2348 bytes
"""
Get Ready Related works class
"""
import sys
from abc import ABC
from DBApps.DbAppParser import DbAppParser, DbArgNamespace, writableExpandoFile
import DBApps.DbApp as DbApp

class ReadyRelatedParser(DbAppParser):
    __doc__ = '\n    Parser for the Get Ready Related class\n    Returns a structure containing fields:\n    .drsDbConfig: str (from base class DBAppArgs\n    .outline: bool\n    .printmaster: bool\n    .numResults: int\n    .results: str (which will have to resolve to a pathlib.Path\n    '

    def __init__(self, description, usage):
        """
        Constructor. Sets up the arguments
        """
        super().__init__(description, usage)
        group = self._parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-o', '--outline', action='store_true', help='Chooses works with outlines')
        group.add_argument('-p', '--printmaster', action='store_true', help='Chooses works with print masters')
        self._parser.add_argument('-n', '--numResults', help='maximum number to download', default=10,
          type=int)
        self._parser.add_argument('results', help='Output path name. May overwrite existing contents',
          type=writableExpandoFile)


class ReadyRelated(DbApp, ABC):
    __doc__ = '\n    Gets related works\n    '
    _options: DbArgNamespace

    @property
    def TypeString(self) -> str:
        """
        Map the option to a string. Calculated, readonly property
        Case sensitive, since this is used to build a call to a SPROC in a mySQL
        database, which has a mixed case namespace
        :return:
        """
        rs = None
        if self._options.outline:
            rs = 'Outlines'
        if self._options.printmaster:
            rs = 'PrintMasters'
        return rs

    def __init__(self, options):
        """
        :param: self
        :param: DbArguments
        :rtype: object
        """
        try:
            super().__init__(options.drsDbConfig)
        except AttributeError:
            print('argument parsing error: drsDbConfig not found in args')
            sys.exit(1)

        self._options = options
        self.ExpectedColumns = ['WorkName', 'HOLLIS', 'Volume']