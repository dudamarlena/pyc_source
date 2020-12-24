# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/targetplugins/macrotarget.py
# Compiled at: 2019-06-18 14:37:15
# Size of source mod 2**32: 2596 bytes
"""
The module containing the classes describing the targets.
"""
import imp
from fastr import exceptions, api
from fastr.core.target import Target

class MacroTarget(Target):
    __doc__ = '\n    A target for MacroNodes. This target cannot be executed as the MacroNode handles\n    execution differently. But this contains the information for the MacroNode to\n    find the internal Network.\n    '

    def __init__(self, network_file, method=None, function='main'):
        """
        Define a new local binary target. Must be defined either using paths and optionally environment_variables
        and initscripts, or enviroment modules.
        """
        if method is None:
            if network_file.endswith(('.py', '.pyc')):
                method = 'python'
            elif network_file.endswith(('.xml', '.json', 'yml', 'yaml')):
                method = 'loads'
        else:
            if method == 'python':
                network_module = imp.load_source('macro_node.utils', network_file)
                network_function = getattr(network_module, function)
                network = network_function()
            else:
                if method == 'loads':
                    network = api.Network.load(network_file)
                else:
                    raise exceptions.FastrValueError('Method {} is not know for a MacroTarget'.format(method))
        if not network:
            raise exceptions.FastrValueError('Network not loaded correctly from "{}"'.format(network_file))
        self.network = network.parent

    @classmethod
    def test(cls):
        """
        Test if singularity is availble on the path
        """
        pass

    def run_command(self, command):
        raise exceptions.FastrNotImplementedError('This method is purposefully not implemented, MacroTarget is not mean for direct execution')