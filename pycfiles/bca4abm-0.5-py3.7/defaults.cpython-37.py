# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\defaults.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 962 bytes
import logging
from activitysim.core import inject
logger = logging.getLogger(__name__)

@inject.injectable(cache=True, override=True)
def chunk_size(settings):
    return int(settings.get('chunk_size', 0))


@inject.injectable(cache=True, override=True)
def trace_hh_id(settings):
    id = settings.get('trace_hh_id', None)
    if id:
        if not isinstance(id, int):
            logger.warn('setting trace_hh_id is wrong type, should be an int, but was %s' % type(id))
            id = None
    return id


@inject.injectable(cache=True, override=True)
def trace_od(settings):
    od = settings.get('trace_od', None)
    if od:
        if isinstance(od, list):
            if not (len(od) == 2 and all((isinstance(x, int) for x in od))):
                logger.warn('setting trace_od is wrong type, should be a list of length 2, but was %s' % od)
                od = None
    return od