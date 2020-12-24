# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/utils/distutils/commands/build_integration_docs.py
# Compiled at: 2019-09-04 11:05:35
from __future__ import absolute_import
import os.path
from distutils import log
from .base import BaseBuildCommand

class BuildIntegrationDocsCommand(BaseBuildCommand):
    description = 'build integration docs'

    def get_dist_paths(self):
        return [
         os.path.join(self.get_root_path(), 'src', 'sentry', 'integration-docs')]

    def _build(self):
        from sentry.utils.integrationdocs import sync_docs
        log.info('downloading integration docs')
        sync_docs()