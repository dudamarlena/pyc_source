# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\file\xmind-sdk-python-master\xmind\core\loader.py
# Compiled at: 2019-07-01 23:22:26
# Size of source mod 2**32: 1527 bytes
"""
    xmind.core.loader
    ~~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""
__author__ = 'aiqi@xmind.net <Woody Ai>'
from . import const
from .workbook import WorkbookDocument
from .. import utils

class WorkbookLoader(object):

    def __init__(self, path):
        super(WorkbookLoader, self).__init__()
        self._input_source = utils.get_abs_path(path)
        file_name, ext = utils.split_ext(self._input_source)
        if ext != const.XMIND_EXT:
            raise Exception("The XMind filename is missing the '%s' extension!" % const.XMIND_EXT)
        self._content_stream = None
        try:
            with utils.extract(self._input_source) as (input_stream):
                for stream in input_stream.namelist():
                    if stream == const.CONTENT_XML:
                        self._content_stream = utils.parse_dom_string(input_stream.read(stream))

        except:
            pass

    def get_workbook(self):
        """ Parse XMind file to `WorkbookDocument` object and return
        """
        content = self._content_stream
        path = self._input_source
        workbook = WorkbookDocument(content, path)
        return workbook


def main():
    pass


if __name__ == '__main__':
    main()