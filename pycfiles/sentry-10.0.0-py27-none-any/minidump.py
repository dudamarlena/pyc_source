# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/lang/native/minidump.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import logging, dateutil.parser as dp
from msgpack import unpack, Unpacker, UnpackException, ExtraData
from sentry.attachments import attachment_cache
from sentry.coreapi import cache_key_for_event
from sentry.utils.safe import setdefault_path
minidumps_logger = logging.getLogger('sentry.minidumps')
MINIDUMP_ATTACHMENT_TYPE = 'event.minidump'
MAX_MSGPACK_BREADCRUMB_SIZE_BYTES = 50000
MAX_MSGPACK_EVENT_SIZE_BYTES = 100000

def write_minidump_placeholder(data):
    data['platform'] = 'native'
    setdefault_path(data, 'level', value='fatal')
    exception = {'type': 'Minidump', 
       'value': 'Invalid Minidump', 
       'mechanism': {'type': 'minidump', 'handled': False, 'synthetic': True}}
    data['exception'] = {'values': [exception]}


def merge_attached_event(mpack_event, data):
    if mpack_event.size > MAX_MSGPACK_EVENT_SIZE_BYTES:
        return
    else:
        try:
            event = unpack(mpack_event)
        except (UnpackException, ExtraData) as e:
            minidumps_logger.exception(e)
            return

        for key in event:
            value = event.get(key)
            if value is not None:
                data[key] = value

        return


def merge_attached_breadcrumbs(mpack_breadcrumbs, data):
    if mpack_breadcrumbs.size > MAX_MSGPACK_BREADCRUMB_SIZE_BYTES:
        return
    else:
        try:
            unpacker = Unpacker(mpack_breadcrumbs)
            breadcrumbs = list(unpacker)
        except (UnpackException, ExtraData) as e:
            minidumps_logger.exception(e)
            return

        if not breadcrumbs:
            return
        current_crumbs = data.get('breadcrumbs')
        if not current_crumbs:
            data['breadcrumbs'] = breadcrumbs
            return
        current_crumb = next((c for c in reversed(current_crumbs) if isinstance(c, dict) and c.get('timestamp') is not None), None)
        new_crumb = next((c for c in reversed(breadcrumbs) if isinstance(c, dict) and c.get('timestamp') is not None), None)
        cap = max(len(current_crumbs), len(breadcrumbs))
        if current_crumb is not None and new_crumb is not None:
            if dp.parse(current_crumb['timestamp']) > dp.parse(new_crumb['timestamp']):
                data['breadcrumbs'] = breadcrumbs + current_crumbs
            else:
                data['breadcrumbs'] = current_crumbs + breadcrumbs
        else:
            data['breadcrumbs'] = current_crumbs + breadcrumbs
        data['breadcrumbs'] = data['breadcrumbs'][-cap:]
        return


def get_attached_minidump(data):
    cache_key = cache_key_for_event(data)
    attachments = attachment_cache.get(cache_key) or []
    return next((a for a in attachments if a.type == MINIDUMP_ATTACHMENT_TYPE), None)