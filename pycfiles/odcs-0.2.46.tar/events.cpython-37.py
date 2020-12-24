# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/events.py
# Compiled at: 2018-06-04 03:42:23
# Size of source mod 2**32: 2770 bytes
from threading import Lock
from sqlalchemy.orm import attributes
from logging import getLogger
log = getLogger()
_cache_lock = Lock()
_cached_composes = {}

def cache_composes_if_state_changed(session, flush_context):
    """Prepare outgoing messages when compose state is changed"""
    from odcs.server.models import Compose
    composes = (item for item in session.new | session.dirty if isinstance(item, Compose))
    composes_state_changed = (compose for compose in composes if not attributes.get_history(compose, 'state').unchanged)
    with _cache_lock:
        for comp in composes_state_changed:
            if comp.id not in _cached_composes:
                _cached_composes[comp.id] = []
            _cached_composes[comp.id].append(comp.json())

    log.debug('Cached composes to be sent due to state changed: %s', _cached_composes.keys())


def start_to_publish_messages(session):
    """Publish messages after data is committed to database successfully"""
    import odcs.server.messaging as messaging
    with _cache_lock:
        msgs = []
        for compose_jsons in _cached_composes.values():
            for compose_json in compose_jsons:
                msgs.append({'event':'state-changed', 
                 'compose':compose_json})

        log.debug('Sending messages: %s', msgs)
        if msgs:
            try:
                messaging.publish(msgs)
            except Exception:
                log.exception('Cannot publish message to bus.')

        _cached_composes.clear()