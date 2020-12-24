# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/mbs.py
# Compiled at: 2019-02-21 06:10:25
# Size of source mod 2**32: 8359 bytes
import requests
from collections import defaultdict
from odcs.server.utils import retry, to_text_type
from odcs.server import log
import gi
gi.require_version('Modulemd', '1.0')
from gi.repository import Modulemd

class ModuleLookupError(Exception):
    pass


class MBS(object):

    def __init__(self, config):
        self.mbs_url = config.mbs_url.rstrip('/')

    @retry(wait_on=(requests.ConnectionError,), logger=log)
    def get_modules(self, **params):
        url = self.mbs_url + '/1/module-builds/'
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def get_latest_modules(self, nsvc):
        """
        Query MBS and return the latest version of the module specified by nsvc.

        :param nsvc: N:S:V[:C] of a module to include in a compose.
        :raises ModuleLookupError: if the module couldn't be found
        :return: the latest version of the module.
        """
        params = {'nsvc':nsvc, 
         'state':5, 
         'verbose':True, 
         'order_desc_by':'version'}
        modules = (self.get_modules)(**params)
        devel_module = False
        if not modules['meta']['total']:
            n = nsvc.split(':')[0]
            if n.endswith('-devel'):
                params['nsvc'] = n[:-len('-devel')] + params['nsvc'][len(n):]
                modules = (self.get_modules)(**params)
                devel_module = True
        if not modules['meta']['total']:
            raise ModuleLookupError('Failed to find module %s in the MBS.' % nsvc)
        ret = []
        for module in modules['items']:
            if ret:
                if ret[0]['version'] != module['version']:
                    break
            if devel_module:
                module['name'] += '-devel'
                mmd = Modulemd.Module.new_from_string(module['modulemd'])
                mmd.upgrade()
                for dep in mmd.get_dependencies():
                    dep.add_requires_single(mmd.get_name(), mmd.get_stream())

                module['modulemd'] = to_text_type(mmd.dumps())
            ret.append(module)

        return ret

    def _add_new_dependencies(self, module_map, modules):
        """
        Helper for ``validate_module_list()`` - scans ``modules`` and adds any missing
        requirements to ``module_map``.

        :param module_map: dict mapping module name:stream to module.
        :param modules: the list of modules to scan for dependencies.
        :return: a list of any modules that were added to ``module_map``.
        """
        new_modules = []
        for module in modules:
            mmd = Modulemd.Module.new_from_string(module['modulemd'])
            mmd.upgrade()
            for deps in mmd.get_dependencies():
                for name, streams in deps.peek_requires().items():
                    for stream in streams.get():
                        key = '%s:%s' % (name, stream)
                        if key not in module_map:
                            new_module = self.get_latest_modules(key)
                            new_modules += new_module
                            module_map[key] = [new_modules]

        return new_modules

    def validate_module_list(self, modules, expand=True):
        """
        Given a list of modules as returned by `get_modules()`, checks that
        there are no conflicting duplicates, removes any exact duplicates,
        and if ``expand`` is set, recursively adds in required modules until
        all dependencies are specified.

        :param modules: a list of modules as returned by ``get_modules()`` or
                ``get_latest_module()``
        :param expand: if required modules should be included in the returned
                list.
        :return: the list of modules with deduplication and expansion.
        :raises ModuleLookupError: if a required module couldn't be found, or a
                conflict occurred when resolving dependencies.
        """
        new_modules = []
        module_map = defaultdict(list)
        for module in modules:
            key = '%s:%s' % (module['name'], module['stream'])
            old_modules = module_map[key]
            if not old_modules:
                module_map[key].append(module)
                new_modules.append(module)
                continue
            if module['version'] != old_modules[0]['version']:
                raise ModuleLookupError('%s:%s:%s:%s conflicts with %s:%s:%s:%s' % (
                 module['name'], module['stream'], module['version'],
                 module['context'], old_modules[0]['name'],
                 old_modules[0]['stream'], old_modules[0]['version'],
                 old_modules[0]['context']))
            if module['context'] in [m['context'] for m in old_modules]:
                continue
            module_map[key].append(module)
            new_modules.append(module)

        if expand:
            added_module_list = new_modules
            while True:
                added_module_list = self._add_new_dependencies(module_map, added_module_list)
                if len(added_module_list) == 0:
                    break
                new_modules.extend(added_module_list)

        return new_modules