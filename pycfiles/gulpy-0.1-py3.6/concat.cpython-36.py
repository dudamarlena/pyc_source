# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\gulpy\pipes\concat.py
# Compiled at: 2017-01-18 19:07:08
# Size of source mod 2**32: 925 bytes
r"""This module is a pipe to concatenate all received files in one.

>>> Stream().src(['file1', 'file2'])\
...         .pipe(Concat('file_concat'))\
...         .dest('./dist')

"""
from itertools import chain

class Concat(object):
    __doc__ = 'Pipe class to concat the stream.'

    def __init__(self, file_name: str):
        """Constructor."""
        self.file_name = file_name
        self.dict = {}

    def run(self, files: list) -> list:
        """Pipe execution.

        :param files: A list of object containing the files of the stream
        :returns: A list with only one object containing the file name given
            and the concatenated stream

        """
        iterators = [file['iterator'] for file in files]
        result = chain.from_iterable(iterators)
        self.dict['name'] = self.file_name
        self.dict['iterator'] = result
        return [
         self.dict]