# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/write/tag.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 513 bytes
from tt.dataaccess.utils import get_data_store
from tt.actions.utils.utils import ensure_working

def action_tag(tags):
    data = get_data_store().load()
    ensure_working(data)
    current = data['work'][(-1)]
    current['tags'] = set(current.get('tags') or [])
    current['tags'].update(tags)
    current['tags'] = list(current['tags'])
    get_data_store().dump(data)
    tag_count = len(tags)
    print('Okay, tagged current work with %d tag%s.' % (
     tag_count, 's' if tag_count > 1 else ''))