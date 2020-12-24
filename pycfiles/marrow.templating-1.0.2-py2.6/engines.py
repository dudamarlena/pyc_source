# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/engines.py
# Compiled at: 2012-05-16 12:10:40
import pkg_resources, warnings, inspect, collections
from marrow.templating.resolver import Resolver
__all__ = [
 'Engines']

class Engines(dict):
    """Engines is a dictionary subclass that allows easy reference to
    rendering engines.
    
    It also acts as an attribute dictionary for even easier reference.
    
    Rendering engines are stored internally as entry point references,
    and are .load()'ed on demand.  Support is present for both simple
    callable entry points and new-style classes whose instances are
    callable.  This allows your rendering engine to have startup code.
    """

    def __init__(self, default=None, cache=50, container=None, **kw):
        """Engines creates a Resolver instance and configures Distribute
        entry point iteration.
        
        The container argument allows you to supply an on-disk path
        which can contain .egg packages to search for engines.
        
        You may pass additional keyword arguments to pre-configure
        engine options.  Engine options will either be merged with
        the options passed at runtime or passed during engine
        initialization depending on if the engine is a simple callable
        or class, respectively.
        """
        super(Engines, self).__init__()
        self.resolve = Resolver(default, cache)
        self.options = collections.defaultdict(dict)
        self.options.update(kw)
        collection = pkg_resources.WorkingSet()
        if container:
            collection.add_entry(container)
        collection.subscribe(self._distributions)

    def __call__(self, template, data=None, **kw):
        """Resolve and execute the given template, passing data to the engine."""
        (engine, filename) = self.resolve(template)
        if not engine:
            raise ValueError('You must explicitly define an engine in each template path if no default is given.')
        if '/' in engine:
            raise ValueError('You can not currently request an engine by mimetype.')
        return self[engine](data=data, template=filename, **kw)

    def __getitem__(self, name):
        item = super(Engines, self).__getitem__(name)
        if inspect.isroutine(item):
            return item
        if hasattr(item, 'load'):
            item = item.load()
        if inspect.isclass(item):
            item = item(**self.options[name])
        self[name] = item
        return item

    def __getattr__(self, name):
        return self[name]

    def __delattr__(self, name):
        del self[name]

    def _distributions(self, dist):
        entries = dist.get_entry_map('web.templating')
        entries.update(dist.get_entry_map('alacarte'))
        if entries:
            warnings.warn('The %s package has declared "web.templating" or "alacarte" entry points.\nThe these entry_point namespaces have been deprecated in favor of "marrow.templating".' % dist.egg_name(), DeprecationWarning)
        entries.update(dist.get_entry_map('marrow.templating'))
        if not entries:
            return
        for (name, engine) in entries.items():
            self[name] = engine