# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/cli/primer.py
# Compiled at: 2017-11-16 20:28:40
import argparse, sys, os
from yac.lib.paths import get_root_path
from sets import Set
yac_commands = ['stack', 'service', 'prefs', 'primer', 'container']

def show_primer(command_array):
    path_elements = [
     get_root_path(), 'primer']
    path_elements = path_elements + command_array
    if len(Set(command_array) & Set(yac_commands)) != len(command_array):
        print 'Options cannot be used with the primer command. usage: yac <command> <subcommand> primer'
    else:
        with open(os.path.join(*path_elements)) as (primer_file):
            primer_file_content = primer_file.read()
        print primer_file_content