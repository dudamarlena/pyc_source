# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\FastGeo\parsers.py
# Compiled at: 2014-01-02 22:30:16


class DbParser(object):
    """
        DbParse parser is meant to serve as an interface for creating parsers to load data from a file or external source.
        """

    def parse(self, path=None):
        """
                Parses the CSV database into List((GeoNode, GeoValue), ...)

                Note: May take several seconds.
                """
        raise NotImplementedError

    def create_node(self, line):
        """
                Creates a GeoNode from a line of the parsed CSV file.

                Can be overriden for easy parsing of other similar CSV files.
                """
        raise NotImplementedError

    def create_value(self, line):
        """
                Creates a GeoValue from a line of the parsed CSV file.

                Can be overriden for easy parsing of other similar CSV files.
                """
        raise NotImplementedError