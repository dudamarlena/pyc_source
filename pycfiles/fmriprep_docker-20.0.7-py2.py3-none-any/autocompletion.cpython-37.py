# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/cli/autocompletion.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 6547 bytes
"""Logic that powers autocompletion installed by ``pip completion``.
"""
import optparse, os, sys
from itertools import chain
from pip._internal.cli.main_parser import create_main_parser
from pip._internal.commands import commands_dict, create_command
from pip._internal.utils.misc import get_installed_distributions
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Any, Iterable, List, Optional

def autocomplete():
    """Entry Point for completion of main and subcommand options.
    """
    if 'PIP_AUTO_COMPLETE' not in os.environ:
        return
        cwords = os.environ['COMP_WORDS'].split()[1:]
        cword = int(os.environ['COMP_CWORD'])
        try:
            current = cwords[(cword - 1)]
        except IndexError:
            current = ''

        parser = create_main_parser()
        subcommands = list(commands_dict)
        options = []
        subcommand_name = None
        for word in cwords:
            if word in subcommands:
                subcommand_name = word
                break

        if subcommand_name is not None:
            if subcommand_name == 'help':
                sys.exit(1)
            should_list_installed = subcommand_name in ('show', 'uninstall') and not current.startswith('-')
            if should_list_installed:
                installed = []
                lc = current.lower()
                for dist in get_installed_distributions(local_only=True):
                    if dist.key.startswith(lc) and dist.key not in cwords[1:]:
                        installed.append(dist.key)

                if installed:
                    for dist in installed:
                        print(dist)

                    sys.exit(1)
            subcommand = create_command(subcommand_name)
            for opt in subcommand.parser.option_list_all:
                if opt.help != optparse.SUPPRESS_HELP:
                    for opt_str in opt._long_opts + opt._short_opts:
                        options.append((opt_str, opt.nargs))

            prev_opts = [x.split('=')[0] for x in cwords[1:cword - 1]]
            options = [(x, v) for x, v in options if x not in prev_opts]
            options = [(k, v) for k, v in options if k.startswith(current)]
            completion_type = get_path_completion_type(cwords, cword, subcommand.parser.option_list_all)
            if completion_type:
                paths = auto_complete_paths(current, completion_type)
                options = [(path, 0) for path in paths]
            for option in options:
                opt_label = option[0]
                if option[1]:
                    if option[0][:2] == '--':
                        opt_label += '='
                print(opt_label)

    else:
        opts = [i.option_list for i in parser.option_groups]
        opts.append(parser.option_list)
        flattened_opts = chain.from_iterable(opts)
        if current.startswith('-'):
            for opt in flattened_opts:
                if opt.help != optparse.SUPPRESS_HELP:
                    subcommands += opt._long_opts + opt._short_opts

        else:
            completion_type = get_path_completion_type(cwords, cword, flattened_opts)
            if completion_type:
                subcommands = list(auto_complete_paths(current, completion_type))
        print(' '.join([x for x in subcommands if x.startswith(current)]))
    sys.exit(1)


def get_path_completion_type(cwords, cword, opts):
    """Get the type of path completion (``file``, ``dir``, ``path`` or None)

    :param cwords: same as the environmental variable ``COMP_WORDS``
    :param cword: same as the environmental variable ``COMP_CWORD``
    :param opts: The available options to check
    :return: path completion type (``file``, ``dir``, ``path`` or None)
    """
    return cword < 2 or cwords[(cword - 2)].startswith('-') or None
    for opt in opts:
        if opt.help == optparse.SUPPRESS_HELP:
            continue
        for o in str(opt).split('/'):
            if cwords[(cword - 2)].split('=')[0] == o:
                if not opt.metavar or any((x in ('path', 'file', 'dir') for x in opt.metavar.split('/'))):
                    return opt.metavar


def auto_complete_paths(current, completion_type):
    """If ``completion_type`` is ``file`` or ``path``, list all regular files
    and directories starting with ``current``; otherwise only list directories
    starting with ``current``.

    :param current: The word to be completed
    :param completion_type: path completion type(`file`, `path` or `dir`)i
    :return: A generator of regular files and/or directories
    """
    directory, filename = os.path.split(current)
    current_path = os.path.abspath(directory)
    if not os.access(current_path, os.R_OK):
        return
    filename = os.path.normcase(filename)
    file_list = (x for x in os.listdir(current_path) if os.path.normcase(x).startswith(filename))
    for f in file_list:
        opt = os.path.join(current_path, f)
        comp_file = os.path.normcase(os.path.join(directory, f))
        if completion_type != 'dir':
            if os.path.isfile(opt):
                yield comp_file
        if os.path.isdir(opt):
            yield os.path.join(comp_file, '')