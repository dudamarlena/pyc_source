# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\main.py
# Compiled at: 2017-05-08 08:46:00
from __future__ import print_function, unicode_literals
import argparse, os, pkg_resources, signal, subprocess, sys
from rbtools import get_version_string
from rbtools.commands import Option, RB_MAIN
from rbtools.utils.aliases import run_alias
from rbtools.utils.filesystem import load_config
GLOBAL_OPTIONS = [
 Option(b'-v', b'--version', action=b'version', version=b'RBTools %s' % get_version_string()),
 Option(b'-h', b'--help', action=b'store_true', dest=b'help', default=False),
 Option(b'command', nargs=argparse.REMAINDER, help=b'The RBTools command to execute, and any arguments. (See below)')]

def build_help_text(command_class):
    """Generate help text from a command class."""
    command = command_class()
    parser = command.create_parser({})
    return parser.format_help()


def help(args, parser):
    if args:
        ep = pkg_resources.get_entry_info(b'rbthsc', b'rbtools_commands', args[0])
        if ep:
            help_text = build_help_text(ep.load())
            print(help_text)
            sys.exit(0)
        print(b'No help found for %s' % args[0])
        sys.exit(0)
    parser.print_help()
    entrypoints = pkg_resources.iter_entry_points(b'rbtools_commands')
    commands = list(set([ entrypoint.name for entrypoint in entrypoints ]))
    common_commands = [b'post', b'patch', b'close', b'diff']
    print(b'\nThe most commonly used commands are:')
    for command in common_commands:
        print(b'  %s' % command)

    print(b'\nOther commands:')
    for command in sorted(commands):
        if command not in common_commands:
            print(b'  %s' % command)

    print(b"See '%s help <command>' for more information on a specific command." % RB_MAIN)
    sys.exit(0)


def main():
    """Execute a command."""

    def exit_on_int(sig, frame):
        sys.exit(128 + sig)

    signal.signal(signal.SIGINT, exit_on_int)
    parser = argparse.ArgumentParser(prog=RB_MAIN, usage=b'%(prog)s [--version] <command> [options] [<args>]', add_help=False)
    for option in GLOBAL_OPTIONS:
        option.add_to(parser)

    opt = parser.parse_args()
    if not opt.command:
        help([], parser)
    command_name = opt.command[0]
    args = opt.command[1:]
    if command_name == b'help':
        help(args, parser)
    else:
        if opt.help or b'--help' in args or b'-h' in args:
            help(opt.command, parser)
        ep = pkg_resources.get_entry_info(b'rbthsc', b'rbtools_commands', command_name)
        if not ep:
            try:
                ep = next(pkg_resources.iter_entry_points(b'rbtools_commands', command_name))
            except StopIteration:
                pass

        if ep:
            try:
                command = ep.load()()
            except ImportError:
                sys.stderr.write(b'Could not load command entry point %s\n' % ep.name)
                sys.exit(1)
            except Exception as e:
                sys.stderr.write(b'Unexpected error loading command %s: %s\n' % (
                 ep.name, e))
                sys.exit(1)

            command.run_from_argv([RB_MAIN, command_name] + args)
        else:
            try:
                sys.exit(subprocess.call([b'%s-%s' % (RB_MAIN, command_name)] + args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, env=os.environ.copy()))
            except OSError:
                pass

        aliases = load_config().get(b'ALIASES', {})
        if command_name in aliases:
            sys.exit(run_alias(aliases[command_name], args))
        else:
            parser.error(b'"%s" is not a command' % command_name)


if __name__ == b'__main__':
    main()