# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mopidy_oe1/__init__.py
# Compiled at: 2017-06-11 07:35:55
from __future__ import unicode_literals
import logging, os
from mopidy import config, ext
__version__ = b'1.2.0'
logger = logging.getLogger(__name__)

class Extension(ext.Extension):
    dist_name = b'Mopidy-OE1'
    ext_name = b'oe1'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), b'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        return schema

    def setup(self, registry):
        from .backend import OE1Backend
        registry.add(b'backend', OE1Backend)