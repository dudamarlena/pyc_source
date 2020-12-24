# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/download/get_now_datetime_filestamp.py
# Compiled at: 2020-04-17 06:44:40
"""
*Generate the datetime stamp for filenames*

:Author:
    David Young
"""
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools

def get_now_datetime_filestamp(longTime=False):
    """
    *A datetime stamp to be appended to the end of filenames: 'YYYYMMDDtHHMMSS'*

    **Key Arguments**

    - ``longTime`` -- make time string longer (more change of filenames being unique)

    **Return**

    - ``now`` -- current time and date in filename format

    **Usage**

    ```python
    from fundamentals.download import get_now_datetime_filestamp
    get_now_datetime_filestamp(longTime=False)
    #Out: '20160316t154635'

    get_now_datetime_filestamp(longTime=True)
    #Out: '20160316t154644133638' 
    ```
    """
    from datetime import datetime, date, time
    now = datetime.now()
    if longTime:
        now = now.strftime('%Y%m%dt%H%M%S%f')
    else:
        now = now.strftime('%Y%m%dt%H%M%S')
    return now