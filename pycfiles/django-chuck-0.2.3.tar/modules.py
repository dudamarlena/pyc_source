# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/base/modules.py
# Compiled at: 2012-06-13 09:33:32
import os, imp

class BaseModule(object):

    def __init__(self, module_name, module_dir):
        self.name = module_name
        self.dir = module_dir
        cfg_file = os.path.join(self.dir, 'chuck_module.py')
        if os.access(cfg_file, os.R_OK):
            self.cfg = imp.load_source(self.name.replace('-', '_'), cfg_file)
        else:
            self.cfg = None
        return

    def get_priority(self):
        if self.cfg and hasattr(self.cfg, 'priority'):
            return self.cfg.priority
        return 100000

    priority = property(get_priority)

    def get_dependencies(self):
        if self.cfg and hasattr(self.cfg, 'depends'):
            return self.cfg.depends
        else:
            return

    dependencies = property(get_dependencies)

    def get_incompatibles(self):
        if self.cfg and hasattr(self.cfg, 'incompatible_with'):
            return self.cfg.incompatible_with
        else:
            return

    incompatibles = property(get_incompatibles)

    def get_description(self):
        if self.cfg and hasattr(self.cfg, 'description'):
            return self.cfg.description
        return ''

    description = property(get_description)

    def get_post_build(self):
        if self.cfg and hasattr(self.cfg, 'post_build'):
            return self.cfg.post_build
        else:
            return

    post_build = property(get_post_build)

    def get_post_setup(self):
        if self.cfg and hasattr(self.cfg, 'post_setup'):
            return self.cfg.post_build
        else:
            return

    post_setup = property(get_post_setup)