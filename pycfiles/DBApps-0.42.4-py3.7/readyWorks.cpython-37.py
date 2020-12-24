# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/readyWorks.py
# Compiled at: 2020-04-14 15:22:04
# Size of source mod 2**32: 1320 bytes
"""
DbApp class to get ready works

"""
import sys
import DBApps.DbApp as DbApp
from DBApps.DbAppParser import DbAppParser, DbArgNamespace, writableExpandoFile

class GetReadyWorksParser(DbAppParser):
    __doc__ = '\n    Specifies arguments for get ready works\n    '

    def __init__(self, description, usage):
        super().__init__(description, usage)
        self._parser.add_argument('-n', '--numWorks', help='how many works to fetch',
          default=10,
          type=int)
        self._parser.add_argument('resultsPath', help='Output path name. May overwrite existing contents',
          type=writableExpandoFile)


class GetReadyWorks(DbApp):
    __doc__ = '\n    Fetch all ready works\n    '

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
        self.ExpectedColumns = ['WorkName', 'HOLLIS', 'Volume', 'OutlineUrn', 'PrintMasterUrn']