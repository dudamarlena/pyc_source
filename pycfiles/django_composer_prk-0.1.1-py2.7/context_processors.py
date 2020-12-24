# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/context_processors.py
# Compiled at: 2017-10-20 11:35:08
import re
from composer.models import Slot

def slots(request):
    """Get the available slots for this URL and return as a mapping."""
    slots = list(Slot.permitted.all())
    slots.sort(lambda a, b: cmp(len(b.url), len(a.url)))
    slot_map = {}
    request_path = request.get_full_path()
    for slot in slots:
        if slot.slot_name in slot_map:
            continue
        if re.search('%s' % slot.url, request_path):
            slot_map[slot.slot_name] = slot

    return {'composer_slots': slot_map}