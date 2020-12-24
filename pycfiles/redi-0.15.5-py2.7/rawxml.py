# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/utils/rawxml.py
# Compiled at: 2018-08-13 08:58:37
import os.path, time, datetime

class RawXml(object):
    """
    This class is used to store details about the input file
    @see redi.batch.check_input_file()
    """

    def __init__(self, project, path):
        """
        Parameters
        ----------
        project : string
            The project name - the owner of the xml file
        path : string
            The xml file path
        """
        self._project = project
        self._path = path

    def get_project(self):
        return self._project

    def get_creation_time(self):
        """ Get the OS creation time """
        tst = os.path.getctime(self._path)
        return datetime.datetime.fromtimestamp(tst)

    def get_last_modified_time(self):
        """ Get the OS modification time """
        tst = os.path.getmtime(self._path)
        return datetime.datetime.fromtimestamp(tst)

    def get_info(self):
        """
        Return a string containing all details available about the xml file
        """
        info = ('\nProject name: {0}\nFile path: {1}\nFile created: {2}\nFile last modified: {3} ').format(self._project, self._path, self.get_creation_time(), self.get_last_modified_time())
        return info