# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\aliases.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import unicode_literals
import logging, re, shlex, sys, subprocess, six
from rbtools.commands import RB_MAIN
_arg_re = re.compile(b'\\$(\\d+)')
_SHLEX_SUPPORTS_UNICODE = sys.version_info >= (2, 7, 3)

def replace_arguments(cmd, args):
    """Do parameter substitution for the given command.

    The special variable $* is expanded to contain all filenames.
    """

    def arg_sub(m):
        """Replace a positional variable with the appropriate argument."""
        index = int(m.group(1)) - 1
        try:
            return args[index]
        except IndexError:
            return b''

    did_replacement = False
    shlex_convert_text_type = not _SHLEX_SUPPORTS_UNICODE and isinstance(cmd, six.text_type)
    if shlex_convert_text_type:
        cmd = cmd.encode(b'utf-8')
    for part in shlex.split(cmd):
        if part == b'$*':
            did_replacement = True
            for arg in args:
                yield arg

        else:
            part, subs = _arg_re.subn(arg_sub, part)
            if subs != 0:
                did_replacement = True
            if shlex_convert_text_type:
                part = part.decode(b'utf-8')
            yield part

    if not did_replacement:
        for arg in args:
            yield arg


def run_alias(alias, args):
    """Run the alias with the given arguments, after expanding parameters.

    Parameter expansion is done by the replace_arguments function.
    """
    use_shell = alias.startswith(b'!')
    try:
        if use_shell:
            cmd = subprocess.list2cmdline(replace_arguments(alias[1:], args))
        else:
            cmd = [
             RB_MAIN] + list(replace_arguments(alias, args))
        return subprocess.call(cmd, shell=use_shell)
    except ValueError as e:
        logging.error(b'Could not execute alias "%s"; it was malformed: %s', alias, e)

    return 1