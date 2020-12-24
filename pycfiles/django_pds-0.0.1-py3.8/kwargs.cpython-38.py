# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/controllers/kwargs.py
# Compiled at: 2020-04-29 12:02:39
# Size of source mod 2**32: 520 bytes
KWARGS_BUILDER_SECRET = 'FXV/#X=>fMT,pc-wm3BYaxqoZ7VOA+'

class KwargsBuilder:

    def purify(self, **kwargs):
        _dict = {}
        for key, value in kwargs.items():
            if value is not KWARGS_BUILDER_SECRET:
                _dict[key] = value
            return _dict

    def build(self, _dict, data, data_key, dict_key=None):
        if dict_key:
            _dict[dict_key] = data.get(data_key, KWARGS_BUILDER_SECRET)
        else:
            _dict[data_key] = data.get(data_key, KWARGS_BUILDER_SECRET)