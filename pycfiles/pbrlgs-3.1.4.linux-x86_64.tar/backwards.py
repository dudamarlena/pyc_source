# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/hooks/backwards.py
# Compiled at: 2017-12-04 07:19:32
from pbr.hooks import base
from pbr import packaging

class BackwardsCompatConfig(base.BaseConfig):
    section = 'backwards_compat'

    def hook(self):
        self.config['include_package_data'] = 'True'
        packaging.append_text_list(self.config, 'dependency_links', packaging.parse_dependency_links())
        packaging.append_text_list(self.config, 'tests_require', packaging.parse_requirements(packaging.TEST_REQUIREMENTS_FILES, strip_markers=True))