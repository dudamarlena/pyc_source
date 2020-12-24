# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nori/ssh.py
# Compiled at: 2013-11-08 15:28:40
"""
This is the SSH submodule for the nori library; see __main__.py for
license and usage information.

DOCSTRING CONTENTS:
-------------------

    1) About and Requirements
    2) API Classes

1) ABOUT AND REQUIREMENTS:
--------------------------

    This submodule provides SSH functionality, including remote command
    execution and tunnels.  It requires the 'ssh' command line utility,
    which must be in the execution search path.  If the utility is not
    available, the module will load, but SSH functionality will not be
    available.

2) API CLASSES:
-----------------

    SSH(object)
        This class wraps all of the SSH functionality.

        Startup and Config-file Processing:
        -----------------------------------

        create_settings()
            Add a block of SSH config settings to the script.

        validate_config()
            Validate SSH config settings.

        SSH Remote Commands and Tunnels:
        --------------------------------

        get_cmd()
            Assemble a list containing the ssh command and its
            arguments.

        get_tunnel_cmd()
            Assemble a list containing the ssh tunnel command and its
            args.

        open_tunnel()
            Open an SSH tunnel, including testing and logging.

        close_tunnel()
            Close an SSH tunnel, including logging.

"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from pprint import pprint as pp
import sys, atexit, shlex, time
from . import core
from . import which
core.exitvals['ssh_connect'] = dict(num=20, descr='\nError establishing SSH connection.\n')
core.exitvals['ssh_tunnel'] = dict(num=21, descr='\nError establishing SSH tunnel.\n')
core.supported_features['ssh'] = 'SSH command and tunnel support'
if which.which('ssh'):
    core.available_features.append('ssh')

class SSH(object):
    """This class wraps all of the SSH functionality."""
    _atexit_close_tunnels_registered = False
    _open_tunnels = []

    def __init__(self, prefix, delim='_'):
        """
        Populate instance variables.
        Parameters:
            prefix, delim: prefix and delimiter that start the setting
                           names to use
        """
        self._prefix = prefix
        self._delim = delim

    @classmethod
    def close_tunnels(cls):
        """
        Close all SSH tunnels.
        NOTE: * do not override in subclasses
              * call with SSH.close_tunnels()
        Dependencies:
            class vars: _open_tunnels
            instance methods: close_tunnel()
        """
        import threading
        for ssh_obj in cls._open_tunnels[:]:
            ssh_obj.close_tunnel()

    def create_settings(self, heading='', extra_text='', ignore=None, extra_requires=[], tunnel=False, default_local_port=None, default_remote_port=None):
        """
        Add a block of SSH config settings to the script.

        Makes the output log settings visible; to reverse this:
            # make output log settings invisible
            core.config_settings_no_print_output_log(True)
            core.config_settings['exec_path']['no_print'] = True
            core.config_settings['log_cmds']['no_print'] = True

        When modifying, remember to keep the setting_list at the bottom
        and validate_config() in sync with the config settings.

        Parameters:
            heading: if not blank, a heading entry with this value will
                     be added to the config settings
            extra_text: if not blank, this value is added to each
                        setting description (prepended with a blank
                        line; does not include the heading)
                        this is mainly intended to be used for things
                        like 'Ignored if [some setting] is not True.'
            ignore: if not None, a function; when this function is true,
                    don't bother validating the settings
            extra_requires: a list of features to be added to the
                            settings' requires attributes
            tunnel: if true, add tunnel-specific settings
            default_local_port: if tunnel is true, used as the default
                                local port number for the tunnel (and
                                must be set)
            default_remote_port: if tunnel is true, used as the default
                                 remote port number for the tunnel (and
                                 must be set)

        Dependencies:
            instance vars: _prefix, _delim, _tunnel_config, _ignore
            methods: validate_config()
            config settings: [_prefix+_delim+:] (heading), ssh_host,
                             ssh_port, ssh_user, ssh_key_file,
                             ssh_options, local_host, local_port,
                             remote_host, remote_port, tun_timeout
            globals: _config_blocks
            modules: core

        """
        core.config_settings_no_print_output_log(False)
        core.config_settings['exec_path']['no_print'] = False
        core.config_settings['log_cmds']['no_print'] = False
        pd = self._prefix + self._delim
        self._tunnel_config = tunnel
        self._ignore = ignore
        if heading:
            core.config_settings[pd + 'heading'] = dict(heading=heading)
        core.config_settings[pd + 'ssh_host'] = dict(descr='\nThe hostname of the remote SSH host.\n', cl_coercer=str)
        core.config_settings[pd + 'ssh_port'] = dict(descr='\nThe SSH port on the remote host.\n', default_descr="\nthe ssh utility's default (generally 22, the standard port)\n", cl_coercer=int)
        core.config_settings[pd + 'ssh_user'] = dict(descr='\nThe username on the remote SSH host.\n', default_descr="\nthe ssh utility's default (generally the username the script is\nrun by)\n", cl_coercer=str)
        core.config_settings[pd + 'ssh_key_file'] = dict(descr='\nThe path to the SSH key file.\n', default_descr=("\nthe ssh utility's default (generally ~/.ssh/id_*)\n").format(pd), cl_coercer=str)
        core.config_settings[pd + 'ssh_options'] = dict(descr="\nThe options to pass to the ssh utility.\n\nThis can be a string or a list of strings.  A string can be passed on the\ncommand line, but this isn't recommended unless it is very simple, due to\nquoting issues.\n", cl_coercer=str)
        if tunnel:
            core.config_settings[pd + 'local_host'] = dict(descr="\nThe hostname on the local end of the SSH tunnel.\n\nThis is generally 'localhost', but it may need to be (e.g.) '127.0.0.1'\nor '::1'.\n", default='localhost', cl_coercer=str)
            core.config_settings[pd + 'local_port'] = dict(descr='\nThe port number on the local end of the SSH tunnel.\n\nCan be any valid unused port.\n', default=default_local_port, cl_coercer=int)
            core.config_settings[pd + 'remote_host'] = dict(descr="\nThe hostname on the remote end of the SSH tunnel.\n\nConnected to from the remote host.\n\nThis is generally 'localhost', but it may need to be (e.g.) '127.0.0.1'\nor '::1'.  It can also be something else entirely, for example if the\npurpose of the tunnel is to get through a firewall, but a connection\ncannot be made directly to the necessary server.\n", default='localhost', cl_coercer=str)
            core.config_settings[pd + 'remote_port'] = dict(descr='\nThe port number on the remote end of the SSH tunnel.\n', default=default_remote_port, cl_coercer=int)
            core.config_settings[pd + 'tun_timeout'] = dict(descr='\nTimeout for establishing the SSH tunnel, in seconds.\n\nCan be None, to wait forever, or a number >= 2 (there is a minimum wait of\none second).\n', default=15, cl_coercer=--- This code section failed: ---

 L. 376         0  LOAD_FAST             0  'x'
                3  LOAD_CONST               'None'
                6  COMPARE_OP            2  ==
                9  POP_JUMP_IF_TRUE     24  'to 24'
               12  LOAD_FAST             0  'x'
               15  LOAD_CONST               'none'
               18  COMPARE_OP            2  ==
             21_0  COME_FROM             9  '9'
               21  POP_JUMP_IF_FALSE    28  'to 28'
               24  LOAD_CONST               None
               27  RETURN_VALUE_LAMBDA
             28_0  COME_FROM            21  '21'

 L. 377        28  LOAD_GLOBAL           1  'int'
               31  LOAD_FAST             0  'x'
               34  CALL_FUNCTION_1       1  None
               37  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
)
        setting_list = [
         'ssh_host', 'ssh_port', 'ssh_user', 'ssh_key_file',
         'ssh_options']
        if tunnel:
            setting_list += [
             'local_host', 'local_port', 'remote_host', 'remote_port',
             'tun_timeout']
        if extra_text:
            for s_name in setting_list:
                if 'descr' in core.config_settings[(pd + s_name)]:
                    core.config_settings[(pd + s_name)]['descr'] += '\n' + extra_text
                else:
                    core.config_settings[(pd + s_name)]['descr'] = extra_text

        for s_name in setting_list:
            if 'requires' in core.config_settings[(pd + s_name)]:
                core.config_settings[(pd + s_name)]['requires'] += [
                 'ssh'] + extra_requires
            else:
                core.config_settings[(pd + s_name)]['requires'] = ['ssh'] + extra_requires

        core.validate_config_hooks.append(self.validate_config)

    def validate_config(self):
        """
        Validate SSH config settings.
        Dependencies:
            instance vars: _prefix, _delim, _ignore, _tunnel_config
            config settings: [_prefix+_delim+:] (heading), ssh_host,
                             ssh_port, ssh_user, ssh_key_file,
                             ssh_options, local_host, local_port,
                             remote_host, remote_port, tun_timeout
            globals: _config_blocks
            modules: core
            Python: 2.0/3.2, for callable()
        """
        pd = self._prefix + self._delim
        if callable(self._ignore) and self._ignore():
            return
        core.setting_check_not_blank(pd + 'ssh_host')
        if core.setting_is_set(pd + 'ssh_port'):
            core.setting_check_num(pd + 'ssh_port', 1, 65535)
        if core.setting_is_set(pd + 'ssh_user'):
            core.setting_check_not_blank(pd + 'ssh_user')
        if core.setting_is_set(pd + 'ssh_key_file'):
            core.setting_check_file_read(pd + 'ssh_key_file')
        if core.setting_is_set(pd + 'ssh_options'):
            if core.setting_check_type(pd + 'ssh_options', core.STRING_TYPES + (list,)) is list:
                core.setting_check_not_empty(pd + 'ssh_options')
                for i, o in enumerate(core.cfg[(pd + 'ssh_options')]):
                    core.setting_check_type((pd + 'ssh_options', i), core.STRING_TYPES)

            else:
                core.setting_check_not_blank(pd + 'ssh_options')
        if self._tunnel_config:
            core.setting_check_not_blank(pd + 'local_host')
            core.setting_check_num(pd + 'local_port', 1, 65535)
            core.setting_check_not_blank(pd + 'remote_host')
            core.setting_check_num(pd + 'remote_port', 1, 65535)
            if core.setting_check_type(pd + 'tun_timeout', core.NUMBER_TYPES + (
             core.NONE_TYPE,)) is not core.NONE_TYPE:
                core.setting_check_num(pd + 'tun_timeout', 2)

    def get_cmd(self):
        """
        Assemble a list containing the ssh command and its arguments.
        Can be used with (e.g.) core.run_command() or
        core.run_with_logging().
        For remote commands, add the remote command/argument list to the
        list returned from this function.
        See also get_tunnel_cmd().
        Dependencies:
            instance vars: _prefix, _delim
            config settings: [_prefix+_delim+:] ssh_host, ssh_port,
                             ssh_user, ssh_key_file, ssh_options
            modules: shlex, core
            external commands: ssh
        """
        pd = self._prefix + self._delim
        cmd = ['ssh']
        if pd + 'ssh_port' in core.cfg:
            cmd += ['-p', str(core.cfg[(pd + 'ssh_port')])]
        if pd + 'ssh_key_file' in core.cfg:
            cmd += ['-i', core.fix_path(core.cfg[(pd + 'ssh_key_file')])]
        if pd + 'ssh_options' in core.cfg:
            if isinstance(core.cfg[(pd + 'ssh_options')], list):
                cmd += core.cfg[(pd + 'ssh_options')]
            else:
                cmd += shlex.split(core.cfg[(pd + 'ssh_options')])
        if pd + 'ssh_user' in core.cfg:
            cmd += ['-l', core.cfg[(pd + 'ssh_user')]]
        cmd.append(core.cfg[(pd + 'ssh_host')])
        return cmd

    def get_tunnel_cmd(self):
        """
        Assemble a list containing the ssh tunnel command and its args.
        Can be used with (e.g.) core.run_command() or
        core.run_with_logging(), but see open_tunnel(), below.
        Dependencies:
            instance vars: _prefix, _delim
            config settings: [_prefix+_delim+:] local_port, remote_host,
                             remote_port
            functions: get_cmd()
            modules: core
            external commands: ssh
        """
        pd = self._prefix + self._delim
        tunnel_arg = ['-L']
        tunnel_arg.append((':').join([
         str(core.cfg[(pd + 'local_port')]),
         core.cfg[(pd + 'remote_host')],
         str(core.cfg[(pd + 'remote_port')])]))
        tunnel_arg.append('-N')
        cmd = self.get_cmd()
        return [cmd[0]] + tunnel_arg + cmd[1:]

    def open_tunnel(self, descr, atexit_reg=True, use_logger=True, warn_only=False, exit_val=core.exitvals['ssh_tunnel']['num']):
        """
        Open an SSH tunnel, including testing and logging.

        Returns the tunnel's process object on success, otherwise False.

        Parameters:
            descr: a description of the tunnel's purpose (e.g. 'mysql
                   dumps' or 'rsync backups'); this is used in status
                   and error messages like 'running SSH tunnel for mysql
                   dumps'
            atexit_reg: if true, register a callback to kill the tunnel
                        on exit; see core.run_command()
            see core.generic_error_handler() for the rest

        Dependencies:
            class vars: _atexit_close_tunnels_registered, _open_tunnels
            instance vars: _prefix, _delim, descr, p_obj
            methods: get_tunnel_cmd(), close_tunnels()
            config settings: [_prefix+_delim+:] (remote_host),
                             (remote_port), local_host, local_port,
                             tun_timeout
            modules: (subprocess), atexit, time, core
            external commands: (ssh)

        """
        pd = self._prefix + self._delim
        self.descr = descr
        core.logging_stop_stdouterr()
        core.status_logger.info(('Running SSH tunnel command for {0}...').format(descr))
        core.logging_start_stdouterr()
        core.output_logger.info(('Running SSH tunnel command for {0}...').format(descr))
        p = core.run_with_logging(('SSH tunnel for {0}').format(descr), self.get_tunnel_cmd(), bg=True, atexit_reg=False, use_logger=use_logger, warn_only=warn_only, exit_val=exit_val)
        waited = 0
        while True:
            if core.test_remote_port(descr, (
             core.cfg[(pd + 'local_host')],
             core.cfg[(pd + 'local_port')]), timeout=0.1, use_logger=None, warn_only=True):
                connected = True
                break
            time.sleep(1)
            waited += 1
            if p.poll() is None:
                if waited >= core.cfg[(pd + 'tun_timeout')]:
                    core.kill_bg_command(p)
                    msg = ('could not establish SSH tunnel for {0} (timed out)').format(descr)
                    core.generic_error_handler(None, msg, core.render_command_exception, use_logger, warn_only, exit_val)
                    connected = False
                    break
            else:
                ssh_exit = p.wait()
                msg = ('could not establish SSH tunnel for {0} (status code {1})').format(descr, ssh_exit)
                core.generic_error_handler(None, msg, core.render_command_exception, use_logger, warn_only, exit_val)
                connected = False
                break

        if connected:
            self.p_obj = p
            core.status_logger.info(('SSH tunnel for {0} established.').format(descr))
            if self not in SSH._open_tunnels:
                SSH._open_tunnels.append(self)
            if not SSH._atexit_close_tunnels_registered:
                atexit.register(SSH.close_tunnels)
                SSH._atexit_close_tunnels_registered = True
            return p
        return False
        return

    def close_tunnel(self):
        """
        Close an SSH tunnel, including logging.
        For tunnels opened with open_tunnel().
        Can be called even if the tunnel already died / was closed / was
        killed.
        Dependencies:
            class vars: _open_tunnels
            instance vars: descr, p_obj
            modules: core
        """
        ret, already = core.kill_bg_command(self.p_obj)
        if already:
            core.status_logger.info(('SSH tunnel for {0} was already closed.').format(self.descr))
        else:
            core.status_logger.info(('SSH tunnel for {0} has been closed.').format(self.descr))
        if self in SSH._open_tunnels:
            SSH._open_tunnels.remove(self)