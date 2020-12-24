# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/extensions/packaging.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, sys
from djblets.extensions.packaging import BuildStaticFiles as DjbletsBuildStaticFiles, build_extension_cmdclass
from setuptools import setup as setuptools_setup
from reviewboard import VERSION

class BuildStaticFiles(DjbletsBuildStaticFiles):
    extension_entrypoint_group = b'reviewboard.extensions'
    django_settings_module = b'reviewboard.settings'

    def get_lessc_global_vars(self):
        global_vars = DjbletsBuildStaticFiles.get_lessc_global_vars(self)
        global_vars.update({b'RB_MAJOR_VERSION': VERSION[0], 
           b'RB_MINOR_VERSION': VERSION[1], 
           b'RB_MICRO_VERSION': VERSION[2], 
           b'RB_PATCH_VERSION': VERSION[3], 
           b'RB_IS_RELEASED': VERSION[5]})
        return global_vars


def setup(**setup_kwargs):
    extensions_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(extensions_dir, b'conf'))
    os.environ[b'FORCE_BUILD_MEDIA'] = b'1'
    setup_kwargs.update({b'zip_safe': False, 
       b'include_package_data': True, 
       b'cmdclass': dict(build_extension_cmdclass(BuildStaticFiles), **setup_kwargs.get(b'cmdclass', {}))})
    setuptools_setup(**setup_kwargs)