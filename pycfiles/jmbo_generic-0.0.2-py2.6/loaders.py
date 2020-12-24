# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/generic/loaders.py
# Compiled at: 2011-09-23 05:40:09
import os
from django.conf import settings
from django.template.loaders.app_directories import Loader

class TypeLoader(Loader):

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Affixes the TEMPLATE_TYPE setting value to the template name thus
        allowing for template switching.
        """
        template_name = os.path.join(settings.TEMPLATE_TYPE, template_name)
        return super(TypeLoader, self).get_template_sources(template_name, template_dirs)