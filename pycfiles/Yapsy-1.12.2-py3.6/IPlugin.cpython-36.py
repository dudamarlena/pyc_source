# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/IPlugin.py
# Compiled at: 2015-09-12 09:09:22
# Size of source mod 2**32: 1186 bytes
"""
Role
====

Defines the basic interfaces for a plugin. These interfaces are
inherited by the *core* class of a plugin. The *core* class of a
plugin is then the one that will be notified the
activation/deactivation of a plugin via the ``activate/deactivate``
methods.

For simple (near trivial) plugin systems, one can directly use the
following interfaces.

Extensibility
=============

In your own software, you'll probably want to build derived classes of
the ``IPlugin`` class as it is a mere interface with no specific
functionality.

Your software's plugins should then inherit your very own plugin class
(itself derived from ``IPlugin``).

Where and how to code these plugins is explained in the section about
the :doc:`PluginManager`.

API
===
"""

class IPlugin(object):
    __doc__ = '\n\tThe most simple interface to be inherited when creating a plugin.\n\t'

    def __init__(self):
        self.is_activated = False

    def activate(self):
        """
                Called at plugin activation.
                """
        self.is_activated = True

    def deactivate(self):
        """
                Called when the plugin is disabled.
                """
        self.is_activated = False