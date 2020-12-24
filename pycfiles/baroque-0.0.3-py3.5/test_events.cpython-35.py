# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/defaults/test_events.py
# Compiled at: 2017-03-28 18:13:54
# Size of source mod 2**32: 445 bytes
from baroque.defaults.events import EventFactory
from baroque.defaults.eventtypes import GenericEventType

def test_new():
    payload = dict(test='value')
    description = 'a test event'
    owner = 'me'
    evt = EventFactory.new(payload=payload, description=description, owner=owner)
    assert isinstance(evt.type, GenericEventType)
    assert evt.payload == payload
    assert evt.owner == owner
    assert evt.description == description