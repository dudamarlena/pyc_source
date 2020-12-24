# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/meya_cli.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import logging, os, sys
from meya_cli.cat_command import CatCommand
from meya_cli.delete_command import DeleteCommand
from meya_cli.download_command import DownloadCommand
from meya_cli.meya_api import MeyaAPIException
from meya_cli.meya_config import find_meya_config, MEYA_CONFIG_FILE
from meya_cli.upload_command import UploadCommand
from meya_cli.watch_command import WatchCommand
from meya_cli.list_command import ListCommand
from meya_cli.init_command import InitCommand
COMMAND_TYPES = [
 InitCommand,
 DownloadCommand,
 UploadCommand,
 WatchCommand,
 DeleteCommand,
 ListCommand,
 CatCommand]

def valid_command_invocations():
    return [ cls.INVOCATION for cls in COMMAND_TYPES ] + ['help']


def get_command(config, command_name, argv):
    for cls in COMMAND_TYPES:
        if command_name == cls.INVOCATION:
            return cls(config, argv)

    raise Exception("Unsupported command '" + command_name + "'!")


def configure_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def print_generic_help(show_help):
    print('Manage Meya apps from command-line.')
    if not show_help:
        print('Full help: meya-cli help')
    for cls in COMMAND_TYPES:
        parser = cls.arg_parser()
        print('')
        print('-- ' + cls.INVOCATION.upper() + ':')
        if show_help:
            parser.print_help()
        else:
            parser.print_usage()


def main():
    try:
        configure_logger()
        if len(sys.argv) <= 1:
            print_generic_help(False)
            return
        if sys.argv[1] in ('help', '--help', '-h'):
            print_generic_help(True)
            return
        if sys.argv[1] not in valid_command_invocations():
            print(("Error: '{command}' is not a valid command! See usage below.\n").format(command=sys.argv[1]))
            print_generic_help(False)
            return
        start_path = os.path.abspath('.')
        config = find_meya_config(start_path)
        if not config and sys.argv[1] != 'init':
            print(("Could not find '{config_file}' in '{path}' or any parent folders!").format(config_file=MEYA_CONFIG_FILE, path=start_path))
            sys.exit(1)
        command = get_command(config, sys.argv[1], sys.argv[2:])
        command.perform()
    except MeyaAPIException as err:
        print(err)