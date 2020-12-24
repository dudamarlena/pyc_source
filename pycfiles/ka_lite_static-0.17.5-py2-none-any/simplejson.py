# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/simplejson.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import absolute_import
import warnings
warnings.warn('django.utils.simplejson is deprecated; use json instead.', PendingDeprecationWarning)
try:
    import simplejson
except ImportError:
    use_simplejson = False
else:
    from json import __version__ as stdlib_json_version
    use_simplejson = hasattr(simplejson, '_speedups') or simplejson.__version__.split('.') >= stdlib_json_version.split('.')

if use_simplejson:
    from simplejson import *
    from simplejson import __version__
else:
    from json import *
    from json import __version__