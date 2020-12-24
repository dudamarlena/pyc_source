# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/main.py
# Compiled at: 2007-03-21 14:34:41
"""Main 'schevo' script runner.

For copyright, license, and warranty, see bottom of file.
"""
import pkg_resources
from schevo.script.command import CommandSet
dist = pkg_resources.get_distribution('Schevo')
NAME = dist.project_name
VERSION = dist.version

class Main(CommandSet):
    __module__ = __name__
    name = '%s %s' % (NAME, VERSION)

    def __init__(self):
        commands = self.commands = {}
        for p in pkg_resources.iter_entry_points('schevo.schevo_command'):
            name = p.name
            command = p.load()
            commands[name] = command


start = Main()

def start_hotshot():
    import hotshot, hotshot.stats, os, schevo
    filename = 'schevo.prof'
    prof = hotshot.Profile(filename)
    prof.runcall(start)
    prof.close()
    stats = hotshot.stats.load(filename)
    stats.sort_stats('cumulative', 'calls')
    stats.print_stats(50)
    stats.sort_stats('time', 'calls')
    stats.print_stats(50)
    stats.sort_stats('cumulative', 'calls')
    schevo_package_path = os.path.dirname(schevo.__file__)
    schevo_package_path = schevo_package_path.replace('\\', '\\\\')
    schevo_package_path = schevo_package_path.lower()
    stats.print_stats(schevo_package_path, 50)
    stats.sort_stats('time', 'calls')
    stats.print_stats(schevo_package_path, 50)