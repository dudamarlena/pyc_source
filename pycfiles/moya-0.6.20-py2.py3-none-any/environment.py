# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/template/environment.py
# Compiled at: 2017-06-20 11:42:28
from __future__ import unicode_literals
from __future__ import print_function
import weakref
from ..compat import text_type, string_types
from .errors import MissingTemplateError, BadTemplateError
from .moyatemplates import Template
from ..cache.dictcache import DictCache
from fs.path import abspath, normpath
from fs.opener import open_fs
from fs.errors import ResourceNotFound, NoSysPath
TEMPLATE_VERSION = 11

class Environment(object):
    name = b'moya'

    def __init__(self, template_fs, archive=None, cache=None):
        if isinstance(template_fs, string_types):
            template_fs = open_fs(template_fs)
        self.template_fs = template_fs
        if archive is not None:
            self._archive = weakref.ref(archive)
            self.cache = cache or archive.get_cache(b'templates')
        else:
            self._archive = lambda : None
            if cache is None:
                cache = DictCache(b'templates', b'')
            self.cache = cache
        self.templates = {}
        self._caches = {}
        return

    @classmethod
    def make_default(self):
        return Environment(open_fs(b'mem://'))

    @property
    def archive(self):
        return self._archive()

    def check_template(self, template_path):
        """Check if a template exists"""
        template_path = abspath(normpath(template_path))
        if template_path in self.templates:
            return
        if not self.template_fs.exists(template_path):
            raise MissingTemplateError(template_path)

    def get_template(self, template_path, parse=True):
        template_path = abspath(normpath(template_path))
        template = self.templates.get(template_path, None)
        if template is not None:
            return template
        else:
            if self.cache.enabled:
                try:
                    info = self.template_fs.getdetails(template_path)
                except ResourceNotFound:
                    raise MissingTemplateError(template_path)

                cache_name = b'%s$%s@%s' % (TEMPLATE_VERSION, template_path, info.modified)
                cached_template = self.cache.get(cache_name, None)
                if cached_template is not None:
                    template = Template.load(cached_template)
                    self.templates[template_path] = template
                    return template
            try:
                source = self.template_fs.gettext(template_path)
            except ResourceNotFound:
                raise MissingTemplateError(template_path)
            except Exception as error:
                raise BadTemplateError(template_path, diagnosis=(b'failed to read text ({})').format(text_type(error)))

            try:
                display_path = self.template_fs.getsyspath(template_path)
            except NoSysPath:
                display_path = template_path

            if self.archive is None:
                lib = None
            else:
                lib = self.archive.get_template_lib(template_path)
            template = Template(source, display_path, raw_path=template_path, lib=lib)
            template.parse(self)
            if self.cache.enabled:
                self.cache.set(cache_name, template.dump(self))
            self.templates[template_path] = template
            return template

    def compile_template(self, source, path):
        template = Template(source, path)
        return template

    def get_cache(self, cache_name):
        if self.archive is not None:
            return self.archive.get_cache(cache_name)
        else:
            if cache_name not in self._caches:
                self._caches[cache_name] = DictCache(cache_name, b'')
            return self._caches[cache_name]