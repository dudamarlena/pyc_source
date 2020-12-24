# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\process.py
# Compiled at: 2012-09-04 05:45:40
import logging, os, subprocess, sys

def die(msg=None):
    """
    Cleanly exits the program with an error message. Erases all remaining
    temporary files.
    """
    from rbtools.utils.filesystem import cleanup_tempfiles
    cleanup_tempfiles()
    if msg:
        print msg
    sys.exit(1)


def execute(command, env=None, split_lines=False, ignore_errors=False, extra_ignore_errors=(), translate_newlines=True, with_errors=True, none_on_ignored_error=False):
    """
    Utility function to execute a command and return the output.
    """
    if isinstance(command, list):
        logging.debug('Running: ' + subprocess.list2cmdline(command))
    else:
        logging.debug('Running: ' + command)
    if env:
        env.update(os.environ)
    else:
        env = os.environ.copy()
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANGUAGE'] = 'en_US.UTF-8'
    if with_errors:
        errors_output = subprocess.STDOUT
    else:
        errors_output = subprocess.PIPE
    if sys.platform.startswith('win'):
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors_output, shell=False, universal_newlines=translate_newlines, env=env)
    else:
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors_output, shell=False, close_fds=True, universal_newlines=translate_newlines, env=env)
    if split_lines:
        data = p.stdout.readlines()
    else:
        data = p.stdout.read()
    rc = p.wait()
    if rc and not ignore_errors and rc not in extra_ignore_errors:
        die('Failed to execute command: %s\n%s' % (command, data))
    elif rc:
        logging.debug('Command exited with rc %s: %s\n%s---' % (
         rc, command, data))
    if rc and none_on_ignored_error:
        return None
    else:
        return data