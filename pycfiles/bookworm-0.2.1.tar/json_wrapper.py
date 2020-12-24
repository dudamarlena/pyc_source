# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/utils/json_wrapper.py
# Compiled at: 2012-02-14 23:34:00
__doc__ = "In Python 2.5, the json module we use is an external module called\n'simplejson'.  From Python 2.6, it is a standard module called 'json'.\nJust to complicate things, in Debian's Python 2.5, there is an\nentirely different module called 'json', so 'import json' might apeear\nto work there but do the worng thing.\n\nThis module includes the logic for ensuring that the right module gets\nimported.  For simplcity of backwards compatibility, the module it\nfinds is called both 'simplejson' and 'json'.\n\n>>> from booki.utils.json_wrapper import json\n>>> from booki.utils.json_wrapper import simplejson\n>>> json is simplejson\nTrue\n"
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