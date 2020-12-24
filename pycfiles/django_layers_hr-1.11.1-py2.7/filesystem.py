# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/loaders/filesystem.py
# Compiled at: 2018-03-27 03:51:51
import os
from django.template.loaders.filesystem import Loader as BaseLoader
from django.template import Origin
from django.utils._os import safe_join
from django.core.exceptions import SuspiciousFileOperation
from django.conf import settings
from crum import get_current_request
from layers import get_current_layer_stack

class Loader(BaseLoader):

    def get_template_sources(self, template_name, template_dirs=None):
        """Make the loader layer aware"""
        if not template_dirs:
            template_dirs = self.get_dirs()
        layers = list(get_current_layer_stack(get_current_request()))
        layers.reverse()
        for template_dir in template_dirs:
            for layer in layers:
                l_template_name = os.path.join(layer, template_name)
                try:
                    name = safe_join(template_dir, l_template_name)
                except SuspiciousFileOperation:
                    continue

                yield Origin(name=name, template_name=template_name, loader=self)