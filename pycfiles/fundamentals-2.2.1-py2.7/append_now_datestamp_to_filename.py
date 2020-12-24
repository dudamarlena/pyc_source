# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/download/append_now_datestamp_to_filename.py
# Compiled at: 2020-04-17 06:44:40
"""
*Append a datetime stamp to the end of a filename to ensure uniqueness*

:Author:
    David Young
"""
from builtins import str
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools

def append_now_datestamp_to_filename(log, filename, longTime=False):
    """
    *append the current datestamp to the end of the filename (before the extension).*

    **Key Arguments**

    - ``log`` -- logger
    - ``filename`` -- the filename
    - ``longTime`` -- use a longer time-stmap. Default *False*

    Return:
        - ``dsFilename`` -- datestamped filename

    **Usage**

    ```python
    # APPEND TIMESTAMP TO THE FILENAME
    from fundamentals.download import append_now_datestamp_to_filename
    filename = append_now_datestamp_to_filename(
            log=log,
            filename="some_filename.html",
            longTime=True
    )

    # OUTPUT
    # 'some_filename_20160316t154123749472.html'
    ```
    """
    from fundamentals.download import get_now_datetime_filestamp
    try:
        sliced = filename.split('.')
        dsFilename = sliced[0] + '_' + get_now_datetime_filestamp(longTime=longTime)
        if len(sliced) == 2:
            dsFilename += '.' + sliced[1]
        else:
            dsFilename += '.xhtml'
    except Exception as e:
        log.error('could not append date stamp to the filename : ' + filename + ' : ' + str(e) + '\n')

    return dsFilename