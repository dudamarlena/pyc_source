# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/MultiprocessPluginManager.py
# Compiled at: 2019-07-27 12:21:18
# Size of source mod 2**32: 3287 bytes
"""
Role
====

Defines a plugin manager that runs all plugins in separate process
linked by pipes.

API
===
"""
import multiprocessing as mproc
from yapsy.IMultiprocessPlugin import IMultiprocessPlugin
from yapsy.IMultiprocessChildPlugin import IMultiprocessChildPlugin
from yapsy.MultiprocessPluginProxy import MultiprocessPluginProxy
from yapsy.PluginManager import PluginManager

class MultiprocessPluginManager(PluginManager):
    __doc__ = '\n\tSubclass of the PluginManager that runs each plugin in a different process\n\t'

    def __init__(self, categories_filter=None, directories_list=None, plugin_info_ext=None, plugin_locator=None):
        if categories_filter is None:
            categories_filter = {'Default': IMultiprocessPlugin}
        PluginManager.__init__(self, categories_filter=categories_filter,
          directories_list=directories_list,
          plugin_info_ext=plugin_info_ext,
          plugin_locator=plugin_locator)
        self.connections = []

    def instanciateElementWithImportInfo(self, element, element_name, plugin_module_name, candidate_filepath):
        """This method instanciates each plugin in a new process and links it to
                the parent with a pipe.

                In the parent process context, the plugin's class is replaced by
                the ``MultiprocessPluginProxy`` class that hold the information
                about the child process and the pipe to communicate with it.

                .. warning:: 
                    The plugin code should only use the pipe to
                        communicate with the rest of the applica`tion and should not
                        assume any kind of shared memory, not any specific functionality
                        of the `multiprocessing.Process` parent class (its behaviour is
                        different between platforms !)
                
                See ``IMultiprocessPlugin``.
                """
        if element is IMultiprocessChildPlugin:
            raise Exception('Preventing instanciation of a bar child plugin interface.')
        instanciated_element = MultiprocessPluginProxy()
        parent_pipe, child_pipe = mproc.Pipe()
        instanciated_element.child_pipe = parent_pipe
        instanciated_element.proc = MultiprocessPluginManager._PluginProcessWrapper(element_name, plugin_module_name, candidate_filepath, child_pipe)
        instanciated_element.proc.start()
        return instanciated_element

    class _PluginProcessWrapper(mproc.Process):
        __doc__ = "Helper class that strictly needed to be able to spawn the\n\t\tplugin on Windows but kept also for Unix platform to get a more\n\t\tuniform behaviour.\n\n\t\tThis will handle re-importing the plugin's module in the child\n\t\tprocess (again this is necessary on windows because what has\n\t\tbeen imported in the main thread/process will not be shared with\n\t\tthe spawned process.)\n\t\t"

        def __init__(self, element_name, plugin_module_name, candidate_filepath, child_pipe):
            self.element_name = element_name
            self.child_pipe = child_pipe
            self.plugin_module_name = plugin_module_name
            self.candidate_filepath = candidate_filepath
            mproc.Process.__init__(self)

        def run(self):
            module = PluginManager._importModule(self.plugin_module_name, self.candidate_filepath)
            element = getattr(module, self.element_name)
            e = element(self.child_pipe)
            e.run()