# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adam/Projects/crowdcomms/gb-openapi-codec/gb_openapi_codec/__init__.py
# Compiled at: 2017-08-11 01:03:09
# Size of source mod 2**32: 401 bytes
import importlib
openapi_codec = importlib.import_module('gb_openapi_codec.python-openapi-codec.openapi_codec')
module_dict = openapi_codec.__dict__
try:
    to_import = openapi_codec.__all__
except AttributeError:
    to_import = [name for name in module_dict if not name.startswith('_')]

locals().update({name:module_dict[name] for name in to_import})