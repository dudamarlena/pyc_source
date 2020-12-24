# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/tools/dist_program.py
# Compiled at: 2019-02-22 02:32:53
# Size of source mod 2**32: 1025 bytes
"""Define distant Program class."""
import reapy
from reapy.errors import DisabledDistAPIError, DisabledDistAPIWarning
from . import program
if not reapy.is_inside_reaper():
    try:
        from reapy.reascript_api.network import Client, WebInterface
        WEB_INTERFACE = WebInterface(reapy.config.WEB_INTERFACE_PORT)
        CLIENT = Client(WEB_INTERFACE.get_reapy_server_port())
    except DisabledDistAPIError:
        import warnings
        warnings.warn(DisabledDistAPIWarning())

class Program(program.Program):

    @staticmethod
    def from_function(function_name):
        code = 'result = {}(*args, **kwargs)'.format(function_name)
        program = Program(code, 'result')

        def g(*args, **kwargs):
            return program.run(args=args, kwargs=kwargs)[0]

        return g

    def run(self, **input):
        if reapy.is_inside_reaper():
            return super(DistProgram, self).run(**input)
        else:
            return CLIENT.run_program(self, input)