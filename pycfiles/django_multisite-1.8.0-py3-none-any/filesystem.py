# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/template/loaders/filesystem.py
# Compiled at: 2019-05-02 13:25:00
from __future__ import unicode_literals
from __future__ import absolute_import
import os
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django import VERSION as django_version

class Loader(FilesystemLoader):

    def get_template_sources(self, *args, **kwargs):
        template_name = args[0]
        domain = Site.objects.get_current().domain
        default_dir = getattr(settings, b'MULTISITE_DEFAULT_TEMPLATE_DIR', b'default')
        for tname in (os.path.join(domain, template_name),
         os.path.join(default_dir, template_name)):
            if django_version < (2, 0, 0):
                args = [
                 tname, None]
            else:
                args = [
                 tname]
            for item in super(Loader, self).get_template_sources(*args, **kwargs):
                yield item

        return