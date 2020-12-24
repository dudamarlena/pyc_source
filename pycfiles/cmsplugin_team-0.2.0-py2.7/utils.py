# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cmsplugin_team/utils.py
# Compiled at: 2013-03-15 08:35:17
import glob, os
from django.conf import settings
from . import TEMPLATES_SETTING_NAME, TEMPLATES_DIR_NAME
TEMPLATES = tuple()

def autodiscover_templates():
    """
    Autodiscovers cmsplugin_ templates the way
    'django.template.loaders.filesystem.Loader' and
    'django.template.loaders.app_directories.Loader' work.
    """

    def sorted_templates(templates):
        """
        Sorts templates
        """
        TEMPLATES = sorted(templates, key=lambda template: template[1])
        return TEMPLATES

    if TEMPLATES:
        return TEMPLATES
    else:
        override_dir = getattr(settings, TEMPLATES_SETTING_NAME, None)
        if override_dir:
            return sorted_templates(override_dir)
        templates = []
        dirs_to_scan = []
        if 'django.template.loaders.app_directories.Loader' in settings.TEMPLATE_LOADERS:
            for app in settings.INSTALLED_APPS:
                _ = __import__(app)
                dir = os.path.dirname(_.__file__)
                if dir not in dirs_to_scan:
                    dirs_to_scan.append(os.path.join(dir, 'templates'))

        if 'django.template.loaders.filesystem.Loader' in settings.TEMPLATE_LOADERS:
            for dir in settings.TEMPLATE_DIRS:
                if dir not in dirs_to_scan:
                    dirs_to_scan.append(dir)

        for dir in dirs_to_scan:
            dir_glob = TEMPLATES_DIR_NAME
            found = glob.glob(os.path.join(dir, ('{}/*.html').format(dir_glob)))
            for file in found:
                dir, file = os.path.split(file)
                dir_count = len(dir_glob.split('/'))
                key, value = os.path.join(*(dir.split('/')[-dir_count:] + [file])), file
                f = False
                for _, template in templates:
                    if template == file:
                        f = True

                if not f:
                    templates.append((key, value))

        return sorted_templates(templates)