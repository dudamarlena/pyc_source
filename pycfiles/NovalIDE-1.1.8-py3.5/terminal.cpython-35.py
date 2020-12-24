# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/terminal.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 5478 bytes
import os, platform, shlex, noval.util.utils as utils
if utils.is_py2():
    from noval.util.which import which
elif utils.is_py3_plus():
    from shutil import which
import subprocess, noval.ui_utils as ui_utils

def run_in_terminal(cmd, cwd, env_overrides={}, keep_open=True, title=None, pause=False, overwrite_env=True):
    from noval.ui_utils import get_environment_with_overrides
    if overwrite_env:
        env = get_environment_with_overrides(env_overrides)
    else:
        env = env_overrides
        if not env:
            env = os.environ
        if platform.system() == 'Windows':
            _run_in_terminal_in_windows(cmd, cwd, env, keep_open, title, pause)
        else:
            if platform.system() == 'Linux':
                _run_in_terminal_in_linux(cmd, cwd, env, keep_open, pause)
            else:
                if platform.system() == 'Darwin':
                    _run_in_terminal_in_macos(cmd, cwd, env_overrides, keep_open)
                else:
                    raise RuntimeError("Can't launch terminal in " + platform.system())


def open_system_shell(cwd, env_overrides={}):
    env = ui_utils.get_environment_with_overrides(env_overrides)
    if platform.system() == 'Darwin':
        _run_in_terminal_in_macos([], cwd, env_overrides, True)
    else:
        if platform.system() == 'Windows':
            cmd = 'start cmd'
            subprocess.Popen(cmd, cwd=cwd, env=env, shell=True)
        else:
            if platform.system() == 'Linux':
                cmd = _get_linux_terminal_command()
                subprocess.Popen(cmd, cwd=cwd, env=env, shell=True)
            else:
                raise RuntimeError("Can't launch terminal in " + platform.system())


def _add_to_path(directory, path):
    if directory in path.split(os.pathsep) or platform.system() == 'Windows' and directory.lower() in path.lower().split(os.pathsep):
        return path
    else:
        return directory + os.pathsep + path


def _run_in_terminal_in_windows(cmd, cwd, env, keep_open, title=None, pause=False):
    if keep_open:
        quoted_args = ' '.join(map(lambda s: s if s == '&' else '"' + s + '"', cmd))
        cmd_line = 'start {title} /D "{cwd}" /W cmd /K "{quoted_args}" '.format(cwd=cwd, quoted_args=quoted_args, title='"' + title + '"' if title else '')
        subprocess.Popen(cmd_line, cwd=cwd, env=env, shell=True)
    else:
        if pause:
            command = 'cmd.exe /c call %s' % cmd
            command += ' &pause'
            subprocess.Popen(command, shell=False, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=cwd, env=env)
        else:
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=cwd, env=env)


def _run_in_terminal_in_linux(cmd, cwd, env, keep_open, pause=False):

    def _shellquote(s):
        return subprocess.list2cmdline([s])

    term_cmd = _get_linux_terminal_command()
    if isinstance(cmd, list):
        cmd = ' '.join(map(_shellquote, cmd))
    if keep_open:
        core_cmd = '{cmd}; exec bash -i'.format(cmd=cmd)
        in_term_cmd = 'bash -c {core_cmd}'.format(core_cmd=_shellquote(core_cmd))
    else:
        if pause:
            in_term_cmd = cmd + ";echo 'Please enter any to continue';read"
        else:
            in_term_cmd = cmd
        if term_cmd == 'lxterminal':
            whole_cmd = '{term_cmd} --command={in_term_cmd}'.format(term_cmd=term_cmd, in_term_cmd=_shellquote(in_term_cmd))
        else:
            if term_cmd == 'gnome-terminal':
                whole_cmd = '{term_cmd} -x bash -c {in_term_cmd}'.format(term_cmd=term_cmd, in_term_cmd=_shellquote(in_term_cmd))
            else:
                whole_cmd = '{term_cmd} {in_term_cmd}'.format(term_cmd=term_cmd, in_term_cmd=_shellquote(in_term_cmd))
    subprocess.Popen(whole_cmd, cwd=cwd, env=env, shell=True)


def _get_linux_terminal_command():
    if which('gnome-terminal'):
        return 'gnome-terminal'
    if which('x-terminal-emulator'):
        xte = which('x-terminal-emulator')
        if xte:
            if os.path.realpath(xte).endswith('/lxterminal') and which('lxterminal'):
                return 'lxterminal'
            return 'x-terminal-emulator'
    else:
        if which('xfce4-terminal'):
            return 'xfce4-terminal'
        if which('lxterminal'):
            return 'lxterminal'
        if which('xterm'):
            return 'xterm'
        raise RuntimeError("Don't know how to open terminal emulator")