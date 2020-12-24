# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/registry/sites.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 6202 bytes
from builtins import str
import django.utils.translation as _
from django.urls import reverse
from django.utils.functional import lazy
from tendenci.apps.registry.exceptions import AlreadyRegistered, NotRegistered
from tendenci.apps.registry.cache import cache_reg_apps, get_reg_apps, delete_reg_apps_cache
from tendenci.apps.site_settings.utils import check_setting, get_setting
lazy_reverse = lazy(reverse, str)

class RegisteredApps(object):
    __doc__ = '\n    RegistredApps iterarable that represents all registered apps\n\n    All registered apps exist in the objects iterable and are also\n    categorized by core/plugins.\n\n    apps = site.get_registered_apps()\n\n    core_apps = registered_apps.core\n    addon_apps = registered_apps.addon\n    people_apps = registered_apps.people\n    '

    def __init__(self, apps, build_from_cache=False):
        self.all_apps = []
        self.core = []
        self.addons = []
        self.people = []
        if not build_from_cache:
            for model, registry in apps.items():
                setting_tuple = ('module',
                 registry.fields['model']._meta.app_label,
                 'enabled')
                if check_setting(*setting_tuple):
                    registry.fields['enabled'] = get_setting(*setting_tuple)
                    registry.fields['has_settings'] = True
                else:
                    registry.fields['enabled'] = True
                    registry.fields['has_settings'] = False
                if 'settings' not in registry.fields['url']:
                    registry.fields['url'].update({'settings': lazy_reverse('settings.index', args=[
                                  'module',
                                  registry.fields['model']._meta.app_label])})
                if registry.fields['app_type'] == 'addon':
                    self.addons.append(registry.fields)
                if registry.fields['app_type'] == 'people':
                    self.people.append(registry.fields)
                if registry.fields['app_type'] == 'core':
                    self.core.append(registry.fields)
                self.all_apps.append(registry.fields)

        else:
            for app in apps:
                setting_tuple = ('module',
                 app['model']._meta.app_label,
                 'enabled')
                if check_setting(*setting_tuple):
                    app['enabled'] = get_setting(*setting_tuple)
                    app['has_settings'] = True
                else:
                    app['enabled'] = True
                    app['has_settings'] = False
                if 'settings' not in app['url']:
                    app['url'].update({'settings': lazy_reverse('settings.index', args=[
                                  'module',
                                  app['model']._meta.app_label])})
                if app['app_type'] == 'addon':
                    self.addons.append(app)
                if app['app_type'] == 'people':
                    self.people.append(app)
                if app['app_type'] == 'core':
                    self.core.append(app)
                self.all_apps.append(app)

        def sort_by(app):
            return app['verbose_name'].lower()

        self.all_apps = sorted((self.all_apps), key=sort_by)
        self.core = sorted((self.core), key=sort_by)
        self.addons = sorted((self.addons), key=sort_by)
        self.people = sorted((self.people), key=sort_by)

    def __iter__(self):
        return iter(self.all_apps)

    def __len__(self):
        return len(self.all_apps)


class RegistrySite(object):
    __doc__ = '\n    Encapsulates all the registries that should be available.\n    This follows the django.contrib.admim model\n    '

    def __init__(self):
        self._registry = {}

    def register(self, model, registry_class=None):
        """
        Registers a model with the site.

        The model should be a Model class, not instances.

        If no registry_class is provided CoreRegistry will be applied
        to the model.
        """
        if not registry_class:
            from tendenci.apps.registry.base import CoreRegistry
            registry_class = CoreRegistry
        if not hasattr(model, '_meta'):
            raise AttributeError(_('The model being registered must derive from Model.'))
        if model in self._registry:
            raise AlreadyRegistered(_('The model %(cls)s is already registered' % {'cls': model.__class__}))
        self._registry[model] = registry_class(model)
        delete_reg_apps_cache()
        cache_reg_apps(self.get_registered_apps())

    def unregister(self, model):
        """
        Unregisters a model from the site.
        """
        if model not in self._registry:
            raise NotRegistered(_('The model %(cls)s is not registered' % {'cls': model.__class__}))
        del self._registry[model]
        delete_reg_apps_cache()
        cache_reg_apps(self.get_registered_apps())

    def get_registered_apps(self):
        cached_apps = get_reg_apps()
        if cached_apps:
            apps = RegisteredApps(cached_apps, build_from_cache=True)
        else:
            apps = RegisteredApps(self._registry)
        return apps


site = RegistrySite()