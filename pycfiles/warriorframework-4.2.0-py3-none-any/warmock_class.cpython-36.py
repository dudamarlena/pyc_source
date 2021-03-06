# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/Classes/warmock_class.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 20081 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from warrior.Framework.Utils.testcase_Utils import pNote
from warrior.Framework.Utils.print_Utils import print_info, print_warning
from warrior.WarriorCore.Classes.war_cli_class import WarriorCliClass as WarCli
VERIFY_ONLY = [
 'verify_cmd_response', 'verify_inorder_cmd_response']

def mockready(func):
    """
        Decorator function that assign a mockready attrib to input func
        the attrib will be used to decide if the func is mockable or not
    """
    if not WarCli.mock:
        if not WarCli.sim:
            return func
    func.__dict__['mockready'] = True
    return func


def mocked(func):
    """
        Decorator function that route function to mocked function
    """

    def inner(*args, **kwargs):
        if not WarCli.mock and not WarCli.sim or WarCli.sim and func.__name__ in VERIFY_ONLY:
            return func(*args, **kwargs)
        else:
            if func.__name__ == 'get_command_details_from_testdata':
                if WarCli.sim:
                    if args[0] is not None:
                        if args[0] != '':
                            from warrior.Framework.Utils.data_Utils import cmd_params
                            cmd_params.update({'sim_response_list': 'simresp'})
                            get_response_file(args[0])
                return func(*args, **kwargs)
            else:
                if func.__name__ == '_get_cmd_details':
                    result = func(*args, **kwargs)
                    pNote('The non-substituted commands:')
                    for index, cmd in enumerate(result['command_list']):
                        pNote('#{}: {}'.format(index + 1, cmd))
                        if WarCli.sim:
                            if MockUtils.cli_Utils.response_reference_dict.get(cmd, None) is not None:
                                pNote('Command: {} is already linked to simresp: {}'.format(cmd, MockUtils.cli_Utils.response_reference_dict[cmd]))
                            else:
                                MockUtils.cli_Utils.response_reference_dict[cmd] = result['sim_response_list'][index]

                    return result
                func_name = func.__name__
                func_module = func.__module__.split('.')[(-1)]
                if func_module in dir(MockUtils):
                    func_module = getattr(MockUtils, func_module)
                    if func_name in dir(func_module):
                        function = getattr(func_module, func_name)
                    else:
                        print_warning('Cannot locate {} in {}'.format(func_name, dir(func_module)))
                        function = func
                else:
                    print_warning('Cannot locate {} in {}'.format(func_module, dir(MockUtils)))
                function = func
            return function(*args, **kwargs)

    return inner


def get_cmd_specific_response_file(root):
    """
        Map the commands block in the response file into a dict like this
        {
            "cmd1_text": {"default": "default response", "r1":"text"},
            "cmd2_text": {"default": "def resp for cmd2", "r2":"hello"}
        }
        :argument:
            root: response file root - xml elem
    """
    cmd_specific_response_dict = {}
    cmds = root.find('commands')
    if cmds is not None:
        for cmd in cmds:
            cmd_text = cmd.get('text', '')
            if cmd_text in cmd_specific_response_dict:
                pNote("The cmd: '{}' has been created beforePlease use one cmd block for the responses for same cmd".format(cmd_text))
            else:
                cmd_specific_response_dict[cmd_text] = {}
                for resp in cmd:
                    resp_name = resp.tag
                    resp_text = resp.get('text', '')
                    if resp_name in cmd_specific_response_dict[cmd_text]:
                        pNote('A response with tag name {} has been created before with value: {}Please rename with a different tag name'.format(resp_name, cmd_specific_response_dict[cmd_text][resp_name]))
                    else:
                        cmd_specific_response_dict[cmd_text][resp_name] = resp_text

    return cmd_specific_response_dict


def get_response_file(testdatafile):
    """
        Build the response dict with response tag name and response text
    """
    from warrior.Framework.Utils.xml_Utils import getRoot, getElementListWithSpecificXpath
    tmp_list = getElementListWithSpecificXpath(testdatafile, './global/response_file')
    response_file = tmp_list[0].text if tmp_list != [] else ''
    response_dict = {}
    cmd_specific_response_dict = {}
    if response_file != '':
        root = getRoot(response_file)
        responses = root.find('responses')
        if responses is not None:
            for resp in responses:
                resp_name = resp.tag
                resp_text = resp.get('text', '')
                if resp_name in response_dict:
                    pNote('A response with tag name {} has been created before with value: {}Please rename with a different tag name'.format(resp_name, response_dict[resp_name]))
                else:
                    response_dict[resp_name] = resp_text

        else:
            pNote('Unable to find responses, please put all responses inside a responses tag', 'ERROR')
        cmd_specific_response_dict = get_cmd_specific_response_file(root)
    else:
        pNote('Unable to retrieve response file from testdata file, please put the path in response_file tag inside global section of the testdata file', 'ERROR')
    MockUtils.cli_Utils.response_dict = response_dict
    MockUtils.cli_Utils.cmd_specific_response_dict = cmd_specific_response_dict


def get_response_from_dict(cmd, simresp=None):
    """
        The order of getting response match is:
        cmd specific response with simresp > global response with simresp > 
        cmd specific response default > global response default
    """
    cmd_response_dict = MockUtils.cli_Utils.cmd_specific_response_dict.get(cmd, None)
    response = ''
    if simresp is not None:
        if cmd_response_dict is not None:
            if simresp in cmd_response_dict:
                response = cmd_response_dict[simresp]
    elif simresp is not None:
        if simresp in MockUtils.cli_Utils.response_dict:
            response = MockUtils.cli_Utils.response_dict[simresp]
    elif cmd_response_dict is not None:
        if 'default' in cmd_response_dict:
            response = cmd_response_dict['default']
    else:
        response = MockUtils.cli_Utils.response_dict.get('default', None)
    return response


def cmd_resp_lookup(cmd):
    """
        Takes in a raw simresp and substitute each part of it with the linked response
        based on the separator it combine responses differently
        , combine responses with space, + combine without space, # combine with newline
    """
    result = ''
    resp_tag = ''
    char_dict = {',':' ',  '+':'',  '#':os.linesep}
    simresp = MockUtils.cli_Utils.response_reference_dict.get(cmd, None)
    if simresp is not None:
        for char in simresp:
            if char == ',' or char == '+' or char == '#':
                response = get_response_from_dict(cmd, resp_tag)
                if response is not None:
                    result += response + char_dict[char]
                else:
                    pNote('Unable to find response tag: {} in response file'.format(resp_tag))
                resp_tag = ''
            else:
                resp_tag += char

        if resp_tag != '':
            response = get_response_from_dict(cmd, resp_tag)
            if response is not None:
                result += response
            else:
                pNote('Unable to find response tag: {} in response file'.format(resp_tag))
    else:
        response = get_response_from_dict(cmd)
        if response is not None:
            result += response
        else:
            pNote('Unable to find response tag: {} in response file'.format(resp_tag))
    return result


class MockUtils(object):
    __doc__ = '\n        This class contains all the mocked Utils\n    '

    def __init__(self):
        """"""
        pass

    class cli_Utils:
        __doc__ = '\n            Mocked cli_Utils\n        '
        response_dict = {}
        response_reference_dict = {}
        cmd_specific_response_dict = {}

        @staticmethod
        def connect_ssh(ip, port='22', username='', password='', logfile=None, timeout=60, prompt='.*(%|#|\\$)', conn_options='', custom_keystroke='', **kwargs):
            """
                This function doesn't actually connect to the server
            """
            pNote('Mocking connect_ssh')
            sshobj = 'Mocking connect_ssh'
            conn_string = ''
            conn_options = '' if conn_options is False or conn_options is None else conn_options
            if not conn_options or conn_options is None:
                conn_options = ''
            command = 'ssh -p {0} {1}@{2} {3}'.format(port, username, ip, conn_options)
            pNote('connectSSH: cmd = %s' % command, 'DEBUG')
            pNote('MOCK MODE: No connection is made to the server')
            return (
             sshobj, conn_string)

        @staticmethod
        def connect_telnet(ip, port='23', username='', password='', logfile=None, timeout=60, prompt='.*(%|#|\\$)', conn_options='', custom_keystroke='', **kwargs):
            """
                This function doesn't actually connect to the server
            """
            pNote('Mocking connect_telnet')
            conn_options = '' if conn_options is False or conn_options is None else conn_options
            pNote('timeout is: %s' % timeout, 'DEBUG')
            pNote('port num is: %s' % port, 'DEBUG')
            command = 'telnet ' + ip + ' ' + port
            if not conn_options or conn_options is None:
                conn_options = ''
            command = command + str(conn_options)
            pNote('connectTelnet: cmd = %s' % command, 'DEBUG')
            pNote('MOCK MODE: No connection is made to the server')
            conn_string = ''
            telnetobj = 'Mocking connect_telnet'
            return (
             telnetobj, conn_string)

        @classmethod
        def _send_cmd(cls, *args, **kwargs):
            """
                This function pass the command to the mocked send_command function
            """
            command = kwargs.get('command')
            startprompt = kwargs.get('startprompt', '.*')
            endprompt = kwargs.get('endprompt', None)
            cmd_timeout = kwargs.get('cmd_timeout', None)
            result, response = cls.send_command('session_obj', startprompt, endprompt, command, cmd_timeout)
            return (result, response)

        @classmethod
        def send_command(cls, *args, **kwargs):
            """
                Get response from the processed response dict
            """
            print_warning("This method is obsolete and will be deprecated soon. Please use 'send_command' method of 'PexpectConnect' class in 'warrior/Framework/ClassUtils/WNetwork/warrior_cli_class.py'")
            return (MockUtils.warrior_cli_class.send_command)(*args, **kwargs)

        @classmethod
        def _send_cmd_by_type(cls, *args, **kwargs):
            """
                mocked command
            """
            pNote(':CMD: %s' % args[3])

        @classmethod
        def _send_command_retrials(cls, *args, **kwargs):
            """
                mocked command
            """
            pNote("_send_command_retrials shouldn't be called in this mode")
            return (True, '')

        @classmethod
        def send_command_and_get_response(cls, *args, **kwargs):
            """
                Get response from the processed response dict
            """
            print_warning("This method is obsolete and will be deprecated soon. Please use 'send_command' method of 'PexpectConnect' class in 'warrior/Framework/ClassUtils/WNetwork/warrior_cli_class.py'")
            _, response = (MockUtils.warrior_cli_class.send_command)(*args, **kwargs)
            return response

    class data_Utils:
        __doc__ = '\n            Mocked data utils\n        '

        @staticmethod
        def get_td_vc(datafile, system_name, td_tag, vc_tag):
            """
                This function is called in another mocked function
            """
            print_info('Mocked data_Utils.get_td_vs')
            return (None, None)

        @staticmethod
        def verify_cmd_response(match_list, context_list, command, response, verify_on_system, varconfigfile=None, endprompt='', verify_group=None, log='true'):
            """
                Trialmode only: it prints the verify text instead of doing actual verification
            """
            from warrior.Framework.Utils import string_Utils
            from warrior.Framework.Utils.data_Utils import get_no_impact_logic
            from warrior.Framework.Utils import testcase_Utils
            if varconfigfile:
                if varconfigfile is not None:
                    match_list = string_Utils.sub_from_varconfig(varconfigfile, match_list)
            for i in range(0, len(match_list)):
                if context_list[i] and match_list[i]:
                    _, found = get_no_impact_logic(context_list[i])
                    found = testcase_Utils.pConvertLogical(found)
                    if found:
                        pNote("Looking for '{}' in response to command '{}'".format(match_list[i], command))
                    else:
                        pNote("Not Looking for '{}' in response to command '{}'".format(match_list[i], command))

            return 'RAN'

        @staticmethod
        def verify_inorder_cmd_response(match_list, verify_list, system, command, verify_dict):
            """
                Trialmode only: it prints the verify text instead of doing actual verification
            """
            pNote('Verifying {} on system {}'.format(command, system))
            pNote('match list: {}'.format(str(match_list)))
            pNote('verify_list: {}'.format(str(verify_list)))
            return 'RAN'

    class warrior_cli_class:
        __doc__ = '\n            Mocked cli_Utils\n        '

        @staticmethod
        def connect_ssh(ip, port='22', username='', password='', logfile=None, timeout=60, prompt='.*(%|#|\\$)', conn_options='', custom_keystroke='', **kwargs):
            """
                This function doesn't actually connect to the server
            """
            pNote('Mocking connect_ssh')
            sshobj = 'Mocking connect_ssh'
            conn_string = ''
            conn_options = '' if conn_options is False or conn_options is None else conn_options
            if not conn_options or conn_options is None:
                conn_options = ''
            command = 'ssh -p {0} {1}@{2} {3}'.format(port, username, ip, conn_options)
            pNote('connectSSH: cmd = %s' % command, 'DEBUG')
            pNote('MOCK MODE: No connection is made to the server')
            return (
             sshobj, conn_string)

        @staticmethod
        def connect_telnet(ip, port='23', username='', password='', logfile=None, timeout=60, prompt='.*(%|#|\\$)', conn_options='', custom_keystroke='', **kwargs):
            """
                This function doesn't actually connect to the server
            """
            pNote('Mocking connect_telnet')
            conn_options = '' if conn_options is False or conn_options is None else conn_options
            pNote('timeout is: %s' % timeout, 'DEBUG')
            pNote('port num is: %s' % port, 'DEBUG')
            command = 'telnet ' + ip + ' ' + port
            if not conn_options or conn_options is None:
                conn_options = ''
            command = command + str(conn_options)
            pNote('connectTelnet: cmd = %s' % command, 'DEBUG')
            pNote('MOCK MODE: No connection is made to the server')
            conn_string = ''
            telnetobj = 'Mocking connect_telnet'
            return (
             telnetobj, conn_string)

        @classmethod
        def _send_cmd(cls, *args, **kwargs):
            """
                This function pass the command to the mocked send_command function
            """
            command = kwargs.get('command')
            startprompt = kwargs.get('startprompt', '.*')
            endprompt = kwargs.get('endprompt', None)
            cmd_timeout = kwargs.get('cmd_timeout', None)
            result, response = cls.send_command('session_obj', startprompt, endprompt, command, cmd_timeout)
            return (result, response)

        @classmethod
        def send_command(cls, *args, **kwargs):
            """
                Get response from the processed response dict

                The order of getting response match is:
                cmd specific response with simresp > global response with simresp > 
                cmd specific response default > global response default
            """
            pNote(':CMD: %s' % args[3])
            if WarCli.sim:
                response = cmd_resp_lookup(args[3])
            else:
                response = ''
            pNote('Response:\n{0}\n'.format(response))
            return (True, response)

        @classmethod
        def _send_cmd_by_type(cls, *args, **kwargs):
            """
                mocked command
            """
            pNote(':CMD: %s' % args[3])