# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/tools/main.py
# Compiled at: 2015-11-17 11:55:31
import argparse
from elasticgit.tools import add_command, run
from springboard.tools.commands import CloneRepoTool
from springboard.tools.commands import CreateIndexTool
from springboard.tools.commands import CreateMappingTool
from springboard.tools.commands import SyncDataTool
from springboard.tools.commands import BootstrapTool
from springboard.tools.commands import StartAppTool
from springboard.tools.commands import ImportContentTool
from springboard.tools.commands import UpdateMessagesTool

def get_parser():
    parser = argparse.ArgumentParser(description='Springboard command line tools.')
    subparsers = parser.add_subparsers(help='Commands')
    add_command(subparsers, BootstrapTool)
    add_command(subparsers, CloneRepoTool)
    add_command(subparsers, CreateIndexTool)
    add_command(subparsers, CreateMappingTool)
    add_command(subparsers, SyncDataTool)
    add_command(subparsers, StartAppTool)
    add_command(subparsers, ImportContentTool)
    add_command(subparsers, UpdateMessagesTool)
    return parser


def main():
    run(get_parser())