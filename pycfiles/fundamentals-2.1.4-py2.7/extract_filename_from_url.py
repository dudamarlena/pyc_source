# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/download/extract_filename_from_url.py
# Compiled at: 2020-04-17 06:44:40
"""
*Try and extract the name of the document located at the given URL*

:Author:
    David Young
"""
from builtins import str
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools

def extract_filename_from_url(log, url):
    """
    *get the filename from a URL.*

    *Will return 'untitled.html', if no filename is found.*

    **Key Arguments**

    - ``url`` -- the url to extract filename from
    

    Returns:
        - ``filename`` -- the filename

    **Usage**

    ```python
    from fundamentals.download import extract_filename_from_url
    name = extract_filename_from_url(
        log=log,
        url="https://en.wikipedia.org/wiki/Docstring"
    )
    print name
    # OUT: Docstring.html
    ```
    
    """
    import re
    try:
        log.debug('extracting filename from url ' + url)
        reEoURL = re.compile('([\\w\\.\\_\\-]*)$')
        filename = reEoURL.findall(url)[0]
        if len(filename) == 0:
            filename = 'untitled.html'
        if not re.search('\\.', filename):
            filename = filename + '.html'
    except Exception as e:
        filename = None
        log.warning('could not extracting filename from url : ' + str(e) + '\n')

    return filename