# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/hooks/metadata.py
# Compiled at: 2017-12-04 07:19:32
from pbr.hooks import base
from pbr import packaging

class MetadataConfig(base.BaseConfig):
    section = 'metadata'

    def hook(self):
        self.config['version'] = packaging.get_version(self.config['name'], self.config.get('version', None))
        packaging.append_text_list(self.config, 'requires_dist', packaging.parse_requirements())
        return

    def get_name(self):
        return self.config['name']