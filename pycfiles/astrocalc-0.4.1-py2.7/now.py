# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/astrocalc/times/now.py
# Compiled at: 2020-05-01 12:03:38
"""
*Report current time in various formats*

:Author:
    David Young
"""
from __future__ import division
from past.utils import old_div
from builtins import object
import sys, os, math, time
os.environ['TERM'] = 'vt100'
from fundamentals import tools

class now(object):
    """
    *Report the current time into various formats*

    **Key Arguments**

    - ``log`` -- logger
    - ``settings`` -- the settings dictionary
    
    """

    def __init__(self, log, settings=False):
        self.log = log
        log.debug("instansiating a new 'now' object")
        self.settings = settings
        return

    def get_mjd(self):
        """
        *Get the current time as an MJD*

        **Return**

        - ``mjd`` -- the current MJD as a float
        

        **Usage**

        
        .. todo::

            - add clutil
            - remove `getCurrentMJD` from all other code

        ```python
        from astrocalc.times import now
        mjd = now(
            log=log
        ).get_mjd()
        ```
        """
        self.log.debug('starting the ``get_mjd`` method')
        jd = old_div(time.time(), 86400.0) + 2440587.5
        mjd = jd - 2400000.5
        self.log.debug('completed the ``get_mjd`` method')
        return mjd