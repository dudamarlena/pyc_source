# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/utils/json_wrapper.py
# Compiled at: 2012-02-14 23:34:00
"""In Python 2.5, the json module we use is an external module called
'simplejson'.  From Python 2.6, it is a standard module called 'json'.
Just to complicate things, in Debian's Python 2.5, there is an
entirely different module called 'json', so 'import json' might apeear
to work there but do the worng thing.

This module includes the logic for ensuring that the right module gets
imported.  For simplcity of backwards compatibility, the module it
finds is called both 'simplejson' and 'json'.

>>> from booki.utils.json_wrapper import json
>>> from booki.utils.json_wrapper import simplejson
>>> json is simplejson
True
"""
try:
    import json
    if not hasattr(json, 'loads'):
        raise ImportError('accidentally imported the wrong json module.')
except ImportError as e:
    from warnings import warn
    warn('json not found: "%s", trying simplejson' % e)
    del warn
    import simplejson as json

simplejson = json