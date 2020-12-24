# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bruc5529/git/fleece/fleece/cli/main.py
# Compiled at: 2019-11-06 12:49:13
import sys, pkg_resources
commands = [
 'build', 'run', 'config']

def print_help():
    print ('Available sub-commands: {}.').format((', ').join(commands))
    print 'Use "fleece <sub-command> --help" for usage.'


def main():
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
    if sys.argv[1] in commands:
        deps = pkg_resources.get_distribution('fleece')._dep_map.get('cli', [])
        for dep in deps:
            try:
                if dep.project_name == 'PyYAML':
                    __import__('yaml')
                else:
                    __import__(dep.project_name)
            except ImportError:
                print ('Dependency "{}" is not installed. Did you run "pip install fleece[cli]"?').format(dep)
                sys.exit(1)

        module = __import__('fleece.cli.' + sys.argv[1])
        module = getattr(module.cli, sys.argv[1])
        getattr(module, 'main')(sys.argv[2:])
    else:
        if sys.argv[1] not in ('--help', '-h'):
            print ('"{}" is not an available fleece sub-command.').format(sys.argv[1])
        print_help()