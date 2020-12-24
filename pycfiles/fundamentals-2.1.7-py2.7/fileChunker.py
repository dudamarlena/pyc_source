# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/files/fileChunker.py
# Compiled at: 2020-04-17 06:44:40
"""
*Iterate through large line-based files in batches of lines*

:Author:
    David Young
"""
from builtins import range
from builtins import object
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
import codecs

class fileChunker(object):
    """
    *The fileChunker iterator - iterate over large line-based files to reduce memory footprint*

    **Key Arguments**

    - ``filepath`` -- path to the large file to iterate over
    - ``batchSize`` -- size of the chunks to return in lines
    

    **Usage**

    To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

    To initiate a fileChunker iterator and then process the file in batches of 100000 lines, use the following:

    ```python
    from fundamentals.files import fileChunker
    fc = fileChunker(
        filepath="/path/to/large/file.csv",
        batchSize=100000
    )
    for i in fc:
        print len(i)
    ```
    
    """

    def __init__(self, filepath, batchSize):
        self.filepath = filepath
        self.batchSize = batchSize
        try:
            self.readFile = codecs.open(self.filepath, encoding='utf-8', mode='r')
        except IOError as e:
            message = 'could not open the file %s' % (self.filepath,)
            raise IOError(message)

    def __iter__(self):
        return self

    def __next__(self):
        batch = []
        for lines in range(self.batchSize):
            l = self.readFile.readline()
            if len(l):
                batch.append(l)

        if len(batch) == 0:
            raise StopIteration
        return batch