# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/webstarts/util.py
# Compiled at: 2017-09-29 15:01:16
# Size of source mod 2**32: 710 bytes
"""Applicable to webstarts"""
from threading import local
import requests
from structlog import get_logger
__author__ = 'john'
__all__ = ['req_session']
log = get_logger(__name__)

class Local(local):

    def __init__(self):
        super().__init__()
        self.cache = {}


sessions = Local()
_key = requests.Session

def clear_cache(back=False):
    sessions.cache = {}
    if back:
        log.debug('Clearing backend sessions')


def req_session(cls=None) -> requests.Session:
    """Thread local request sessions"""
    _cls = cls or _key
    s = sessions.cache.get(_cls)
    if s is None:
        s = sessions.cache[_cls] = _cls()
        log.debug('Creating session')
    return s