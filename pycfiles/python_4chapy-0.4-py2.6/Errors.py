# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Fourchapy/Errors.py
# Compiled at: 2012-12-26 16:47:43
""" Fetch 4chan API data in a 4chan-friendly fashion
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
"""
import logging
logger = logging.getLogger('Fourchapy.' + __name__)
log = logger.log
from urllib import urlopen
import datetime
from json import loads
import time

class InvalidDataReturnedError(ValueError):
    """ The data from 4chan's servers isn't valid """
    pass


class NoDataReturnedError(InvalidDataReturnedError):
    """ An empty JSON file was downloaded from 4chan. This usually means that the thread
    is dead/deleted. 
    """
    pass


class Fetch404Error(ValueError):
    """ Got a 404 when trying to load a URL """
    pass


class ThreadNotFoundError(Fetch404Error):
    """ The requested thread doens't exist anymore. 
    """
    pass


class RequestRateTooHigh(RuntimeError):
    """ We're making requests faster than 4chan allows. 
    See https://github.com/4chan/4chan-API#api-rules for request rate details.
    """
    pass