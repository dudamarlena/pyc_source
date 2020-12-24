# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zerolog/commands/main.py
# Compiled at: 2016-09-30 02:06:36
# Size of source mod 2**32: 607 bytes
import argparse
from zerolog.commands.forwarder import forwarder_command
from zerolog.commands.receiver import receiver_command
from zerolog.commands.worker import worker_command
PARSERS = [
 forwarder_command,
 receiver_command,
 worker_command]

def build_parser():
    parser = argparse.ArgumentParser(prog='zerolog')
    subparsers = parser.add_subparsers(help='sub commands avaibles', dest='parser')
    subparsers.required = True
    for p in PARSERS:
        p(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)