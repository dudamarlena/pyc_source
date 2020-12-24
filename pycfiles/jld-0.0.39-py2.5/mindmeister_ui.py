# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\mindmeister_ui.py
# Compiled at: 2009-01-13 13:24:50
""" MindMeister User Interface
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mindmeister_ui.py 793 2009-01-13 18:26:52Z JeanLou.Dupont $'
import jld.tools.cmd_ui as ui

class MM_UI(ui.UIBase):
    """ Handles user interface
    """
    _map = {'jld.api.ErrorPopen': {'msg': 'error_eventmgr', 'help': 'help_eventmgr'}, 'jld.api.ErrorConfig': {'msg': 'error_defaults', 'help': 'help_defaults'}, 'jld.api.ErrorDb': {'msg': 'error_db', 'help': 'help_db'}, 'jld.api.ErrorAuth': {'msg': 'error_auth', 'help': 'help_auth'}, 'jld.api.ErrorNetwork': {'msg': 'error_network', 'help': 'help_network'}, 'jld.api.ErrorAccess': {'msg': 'error_access', 'help': 'help_access'}, 'jld.api.ErrorMethod': {'msg': 'error_method', 'help': 'help_method'}, 'jld.api.ErrorValidation': {'msg': 'error_validation', 'help': 'help_validation'}, 'jld.api.ErrorProtocol': {'msg': 'error_protocol', 'help': 'help_protocol'}, 'jld.api.ErrorInvalidCommand': {'msg': 'error_command', 'help': 'help_command'}, 'jld.registry.exception.RegistryException': {'msg': 'error_registry', 'help_win': 'help_registry_win', 'help_nix': 'help_registry_nix'}}


if __name__ == '__main__':
    import jld.backup.mindmeister_messages as msg
    msgs = msg.MM_Messages()
    ui = MM_UI(msgs)
    import jld.registry.exception as regExc
    e = regExc.RegistryException('test')
    ui.handleError(e)

    class NotDefined(Exception):
        pass


    nd = NotDefined('not defined...')
    ui.handleError(nd)
    ea = api.ErrorAuth()
    ui.handleError(ea)