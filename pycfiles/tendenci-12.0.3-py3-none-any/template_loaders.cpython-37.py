# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme/template_loaders.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 6120 bytes
"""
Wrapper for loading template based on a selected Theme.
"""
import os, errno
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.base import Origin
import django.template.loaders.base as DjangoLoader
import django.template.loaders.cached as DjangoCachedLoader
from django.utils._os import safe_join
import django.core.cache as cache
from django.core.exceptions import SuspiciousFileOperation
from tendenci.apps.theme.utils import get_active_theme, get_theme, get_theme_search_order, is_builtin_theme, get_theme_root
from tendenci.apps.theme.middleware import get_current_request
from tendenci.libs.boto_s3.utils import read_theme_file_from_s3

class ThemeLoader(DjangoLoader):
    __doc__ = "\n    Loader that searches for templates in Tendenci themes.  This can be used to\n    override both the project's templates dir and the app templates dirs using\n    themes.\n    "

    def __init__(self, engine, *args, **kwargs):
        self.cached_theme_search_info = (None, None)
        super(ThemeLoader, self).__init__(engine)

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Return possible absolute paths to "template_name" in the current theme
        and any themes it inherits from.
        Any paths that don't lie inside one of the template dirs are excluded
        from the result set for security reasons.
        """
        request = get_current_request()
        mobile = request and request.mobile
        active_theme = get_active_theme()
        theme = get_theme(active_theme)
        cached_theme, theme_search_info = self.cached_theme_search_info
        if cached_theme != theme:
            theme_search_info = []
            for cur_theme in get_theme_search_order(theme):
                if not is_builtin_theme(cur_theme):
                    settings.USE_S3_THEME or theme_search_info.append((cur_theme, get_theme_root(cur_theme), False))
                else:
                    theme_search_info.append((cur_theme, cur_theme, True))

            if theme == active_theme:
                self.cached_theme_search_info = (
                 theme, theme_search_info)
        for cur_theme, cur_theme_root, use_s3_theme in theme_search_info:
            for template_path in ['mobile', 'templates'] if mobile else ['templates']:
                if not use_s3_theme:
                    try:
                        template_file = safe_join(cur_theme_root, template_path, template_name)
                    except SuspiciousFileOperation:
                        continue

                else:
                    template_file = os.path.join(cur_theme_root, template_path, template_name)
                origin = Origin(name=template_file, template_name=template_name, loader=self)
                origin.theme = cur_theme
                origin.use_s3_theme = use_s3_theme
                yield origin

    def get_contents(self, origin):
        if not origin.use_s3_theme:
            try:
                with open(origin.name) as (fp):
                    return fp.read()
            except IOError as e:
                try:
                    if e.errno == errno.ENOENT:
                        raise TemplateDoesNotExist(origin)
                    raise
                finally:
                    e = None
                    del e

        else:
            cache_key = '.'.join([settings.SITE_CACHE_KEY, 'theme', origin.name])
            cached_template = cache.get(cache_key)
            if cached_template == 'tried':
                raise TemplateDoesNotExist(origin)
            if cached_template:
                return cached_template
            try:
                template = read_theme_file_from_s3(origin.name)
            except:
                cache.set(cache_key, 'tried')
                raise TemplateDoesNotExist(origin)

            cache.set(cache_key, template)
            cache_group_key = '%s.theme_files_cache_list' % settings.SITE_CACHE_KEY
            cache_group_list = cache.get(cache_group_key)
            if cache_group_list is None:
                cache.set(cache_group_key, [cache_key])
            else:
                cache_group_list += [cache_key]
                cache.set(cache_group_key, cache_group_list)
            return template


class CachedLoader(DjangoCachedLoader):
    __doc__ = '\n    Wrapper around django.template.loaders.cached.Loader which allows caching to\n    be disabled on a per-request basis.  This is used to support theme previews.\n    '

    def get_template(self, *args, **kwargs):
        request = get_current_request()
        disable_cache = request and 'theme' in request.session
        if not disable_cache:
            return (super(CachedLoader, self).get_template)(*args, **kwargs)
        return (DjangoLoader.get_template)(self, *args, **kwargs)