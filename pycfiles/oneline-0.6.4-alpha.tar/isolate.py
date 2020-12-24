# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/plugins/isolate.py
# Compiled at: 2014-09-06 21:58:19
"""The isolation plugin resets the contents of sys.modules after running
each test module or package. Use it by setting ``--with-isolation`` or the
NOSE_WITH_ISOLATION environment variable.

The effects are similar to wrapping the following functions around the
import and execution of each test module::

    def setup(module):
        module._mods = sys.modules.copy()
    
    def teardown(module):
        to_del = [ m for m in sys.modules.keys() if m not in
                   module._mods ]
        for mod in to_del:
            del sys.modules[mod]
        sys.modules.update(module._mods)

Isolation works only during lazy loading. In normal use, this is only
during discovery of modules within a directory, where the process of
importing, loading tests and running tests from each module is
encapsulated in a single loadTestsFromName call. This plugin
implements loadTestsFromNames to force the same lazy-loading there,
which allows isolation to work in directed mode as well as discovery,
at the cost of some efficiency: lazy-loading names forces full context
setup and teardown to run for each name, defeating the grouping that
is normally used to ensure that context setup and teardown are run the
fewest possible times for a given set of names.

.. warning ::

    This plugin should not be used in conjunction with other plugins
    that assume that modules, once imported, will stay imported; for
    instance, it may cause very odd results when used with the coverage
    plugin.

"""
import logging, sys
from nose.plugins import Plugin
log = logging.getLogger('nose.plugins.isolation')

class IsolationPlugin(Plugin):
    """
    Activate the isolation plugin to isolate changes to external
    modules to a single test module or package. The isolation plugin
    resets the contents of sys.modules after each test module or
    package runs to its state before the test. PLEASE NOTE that this
    plugin should not be used with the coverage plugin, or in any other case
    where module reloading may produce undesirable side-effects.
    """
    score = 10
    name = 'isolation'

    def configure(self, options, conf):
        """Configure plugin.
        """
        Plugin.configure(self, options, conf)
        self._mod_stack = []

    def beforeContext(self):
        """Copy sys.modules onto my mod stack
        """
        mods = sys.modules.copy()
        self._mod_stack.append(mods)

    def afterContext(self):
        """Pop my mod stack and restore sys.modules to the state
        it was in when mod stack was pushed.
        """
        mods = self._mod_stack.pop()
        to_del = [ m for m in sys.modules.keys() if m not in mods ]
        if to_del:
            log.debug('removing sys modules entries: %s', to_del)
            for mod in to_del:
                del sys.modules[mod]

        sys.modules.update(mods)

    def loadTestsFromNames(self, names, module=None):
        """Create a lazy suite that calls beforeContext and afterContext
        around each name. The side-effect of this is that full context
        fixtures will be set up and torn down around each test named.
        """
        if not names or len(names) == 1:
            return
        loader = self.loader
        plugins = self.conf.plugins

        def lazy():
            for name in names:
                plugins.beforeContext()
                yield loader.loadTestsFromName(name, module=module)
                plugins.afterContext()

        return (
         loader.suiteClass(lazy), [])

    def prepareTestLoader(self, loader):
        """Get handle on test loader so we can use it in loadTestsFromNames.
        """
        self.loader = loader