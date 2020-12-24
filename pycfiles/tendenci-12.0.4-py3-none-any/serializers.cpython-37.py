# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/api_tasty/serializers.py
# Compiled at: 2020-02-26 14:47:57
# Size of source mod 2**32: 360 bytes
from tastypie.serializers import Serializer

class SafeSerializer(Serializer):
    __doc__ = '\n    Removes the optional serializers from the available formats\n    to avoid dependency errors.\n    '
    formats = ['json', 'jsonp', 'html']
    content_types = {'json':'application/json', 
     'jsonp':'text/javascript', 
     'html':'text/html'}