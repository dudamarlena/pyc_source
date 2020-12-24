# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/projects/pythonunited/provgroningen/buildout/src/djinn_core/djinn_core/skintemplateloader.py
# Compiled at: 2015-11-18 16:25:46
import io, os, sys, pkg_resources
from django.template.loaders.base import Loader as BaseLoader
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.template import Engine
from django.template import TemplateDoesNotExist
fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
app_template_dirs = []
for entrypoint in pkg_resources.iter_entry_points(group='djinn.skin'):
    app = entrypoint.module_name
    try:
        mod = import_module(app)
    except ImportError as e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))

    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    if os.path.isdir(template_dir):
        app_template_dirs.append(template_dir.decode(fs_encoding))

app_template_dirs = tuple(app_template_dirs)

class SkinTemplateLoader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        tried = []
        for filedir in app_template_dirs:
            filepath = '%s/%s' % (filedir, template_name)
            try:
                with io.open(filepath, encoding=self.engine.file_charset) as (fp):
                    return (
                     fp.read(), filepath)
            except IOError:
                tried.append(filepath)

        if tried:
            error_msg = 'Tried %s' % tried
        else:
            error_msg = 'Your template directories configuration is empty. Change it to point to at least one template directory.'
        raise TemplateDoesNotExist(error_msg)

    load_template_source.is_usable = True


_loader = SkinTemplateLoader(Engine())