# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/package/host.py
# Compiled at: 2019-01-22 13:34:55
# Size of source mod 2**32: 5287 bytes
import os, pkg_resources
from typeguard import check_argument_types
from typing import Sequence
from pkg_resources import Distribution
from .canonical import name as _name
from .cache import PluginCache
from .loader import traverse
from .tarjan import robust_topological_sort
log = __import__('logging').getLogger(__name__)

class PluginManager:

    def __init__(self, namespace, folders=None):
        assert check_argument_types()
        self.namespace = namespace
        self.folders = folders if folders else list()
        self.plugins = list()
        self.named = PluginCache(namespace)
        self.ws = ws = pkg_resources.working_set
        for container in self.folders:
            path = os.path.abspath(os.path.expanduser(container))
            log.info(('Adding ' + path + ' to plugin search path.'), extra=dict(path=path, namespace=(self.namespace)))
            ws.add_entry(path)
            env = pkg_resources.Environment([path])
            (ws.require)(*env)

        ws.subscribe(self._register)
        super(PluginManager, self).__init__()

    def register(self, name: str, plugin: object) -> None:
        assert check_argument_types()
        log.info(('Registering plugin' + name + ' in namespace ' + self.namespace + '.'), extra=dict(plugin_name=name, namespace=(self.namespace), plugin=(_name(plugin))))
        self.named[name] = plugin
        self.plugins.append(plugin)

    def _register(self, dist: Distribution) -> None:
        if not check_argument_types():
            raise AssertionError
        else:
            entries = dist.get_entry_map(self.namespace)
            if not entries:
                return
            try:
                for name in entries:
                    plugin = entries[name].load()
                    self.register(name, plugin)

            except pkg_resources.UnknownExtra:
                log.warning(("Skipping registration of '{!r}' due to missing dependencies.".format(dist)), exc_info=True)
            except ImportError:
                log.error(("Skipping registration of '{!r}' due to uncaught error on import.".format(dist)), exc_info=True)

    def __iter__(self):
        for plugin in self.plugins:
            yield plugin

    def __getattr__(self, name: str):
        return self.named[name]

    def __getitem__(self, name: str):
        return self.named[name]


class ExtensionManager(PluginManager):
    __doc__ = 'More advanced plugin architecture using structured "extensions".\n\t\n\tExtensions describe their dependencies using an expressive syntax:\n\t\n\t* ``provides`` — declare tags describing the features offered by the plugin\n\t* ``needs`` — delcare the tags that must be present for this extension to function\n\t* ``uses`` — declare the tags that must be evaluated prior to this extension, but aren\'t hard requirements\n\t* ``first`` — declare that this extension is a dependency of all other non-first extensions\n\t* ``last`` — declare that this extension depends on all other non-last extensions\n\t\n\t'

    def order(self, config=None, prefix=''):
        extensions = traverse(config if config else self.plugins, prefix)
        provided = (set().union)(*(traverse(ext, 'provides', ()) for ext in extensions))
        needed = (set().union)(*(traverse(ext, 'needs', ()) for ext in extensions))
        if not provided.issuperset(needed):
            raise LookupError('Extensions providing the following features must be configured:\n' + ', '.join(needed.difference(provided)))
        universal = list()
        inverse = list()
        provides = dict()
        excludes = dict()
        for ext in extensions:
            for feature in traverse(ext, 'provides', ()):
                provides[feature] = ext

            for feature in traverse(ext, 'excludes', ()):
                excludes.setdefault(feature, []).append(ext)

            if traverse(ext, 'first', False):
                universal.append(ext)
            elif traverse(ext, 'last', False):
                inverse.append(ext)

        for conflict in set(provides) & set(excludes):
            raise RuntimeError("{!r} precludes use of '{!s}', which is defined by {!r}".format(excludes[conflict], conflict, provides[conflict]))

        dependencies = dict()
        for ext in extensions:
            requirements = set(traverse(ext, 'needs', ()))
            requirements.update(set(traverse(ext, 'uses', ())).intersection(provided))
            dependencies[ext] = set((provides[req] for req in requirements))
            if universal:
                if ext not in universal:
                    dependencies[ext].update(universal)
                if inverse and ext in inverse:
                    dependencies[ext].update(set(extensions).difference(inverse))

        dependencies = robust_topological_sort(dependencies)
        extensions = []
        for ext in dependencies:
            if len(ext) > 1:
                raise LookupError('Circular dependency found: ' + repr(ext))
            extensions.append(ext[0])

        extensions.reverse()
        return extensions