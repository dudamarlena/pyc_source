# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\writers\json_writer.py
# Compiled at: 2018-01-08 04:59:40
# Size of source mod 2**32: 464 bytes
""" JSON writer """
import logging
from soccer.writers import BasicWriter

class JSONWriter(BasicWriter):
    __doc__ = '\n    JSON writer\n    '

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def league_table(self, table):
        return table

    def rank_table(self, table, position):
        return table

    def title_table(self, title_table):
        return title_table

    def fixture_list(self, fixtures):
        return fixtures