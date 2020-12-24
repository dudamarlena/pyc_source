# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/PluginManagerDecorator.py
# Compiled at: 2015-09-12 09:09:22
# Size of source mod 2**32: 3598 bytes
"""
Role
====

Provide an easy way to build a chain of decorators extending the
functionalities of the default plugin manager, when it comes to
activating, deactivating or looking into loaded plugins.

The ``PluginManagerDecorator`` is the base class to be inherited by
each element of the chain of decorator.

.. warning:: If you want to customise the way the plugins are detected
             and loaded, you should not try to do it by implementing a
             new ``PluginManagerDecorator``. Instead, you'll have to
             reimplement the :doc:`PluginManager` itself. And if you
             do so by enforcing the ``PluginManager`` interface, just
             giving an instance of your new manager class to the
             ``PluginManagerDecorator`` should be transparent to the
             "stantard" decorators.

API
===
"""
import os
from yapsy.IPlugin import IPlugin
from yapsy import log

class PluginManagerDecorator(object):
    __doc__ = "\n\tAdd several responsibilities to a plugin manager object in a\n\tmore flexible way than by mere subclassing. This is indeed an\n\timplementation of the Decorator Design Patterns.\n        \n\t\n\tThere is also an additional mechanism that allows for the\n\tautomatic creation of the object to be decorated when this object\n\tis an instance of PluginManager (and not an instance of its\n\tsubclasses). This way we can keep the plugin managers creation\n\tsimple when the user don't want to mix a lot of 'enhancements' on\n\tthe base class.\n\n\t\n\tAbout the __init__:\n\n\tMimics the PluginManager's __init__ method and wraps an\n\tinstance of this class into this decorator class.\n\t\t\n\t  - *If the decorated_object is not specified*, then we use the\n\t    PluginManager class to create the 'base' manager, and to do\n\t    so we will use the arguments: ``categories_filter``,\n\t    ``directories_list``, and ``plugin_info_ext`` or their\n\t    default value if they are not given.\n\t  - *If the decorated object is given*, these last arguments are\n\t    simply **ignored** !\n\n\tAll classes (and especially subclasses of this one) that want\n\tto be a decorator must accept the decorated manager as an\n\tobject passed to the init function under the exact keyword\n\t``decorated_object``.\n\t"

    def __init__(self, decorated_object=None, categories_filter=None, directories_list=None, plugin_info_ext='yapsy-plugin'):
        if directories_list is None:
            directories_list = [
             os.path.dirname(__file__)]
        else:
            if categories_filter is None:
                categories_filter = {'Default': IPlugin}
            if decorated_object is None:
                log.debug('Creating a default PluginManager instance to be decorated.')
                from yapsy.PluginManager import PluginManager
                decorated_object = PluginManager(categories_filter, directories_list, plugin_info_ext)
        self._component = decorated_object

    def __getattr__(self, name):
        """
                Decorator trick copied from:
                http://www.pasteur.fr/formation/infobio/python/ch18s06.html
                """
        return getattr(self._component, name)

    def collectPlugins(self):
        """
                This function will usually be a shortcut to successively call
                ``self.locatePlugins`` and then ``self.loadPlugins`` which are
                very likely to be redefined in each new decorator.

                So in order for this to keep on being a "shortcut" and not a
                real pain, I'm redefining it here.
                """
        self.locatePlugins()
        self.loadPlugins()