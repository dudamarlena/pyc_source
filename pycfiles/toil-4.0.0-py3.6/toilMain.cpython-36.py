# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilMain.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 2195 bytes
from __future__ import absolute_import, print_function
from past.builtins import map
from toil.version import version
import pkg_resources, os, sys, re
from six import iteritems, iterkeys

def main():
    modules = loadModules()
    try:
        command = sys.argv[1]
    except IndexError:
        printHelp(modules)
    else:
        if command == '--help':
            printHelp(modules)
        else:
            if command == '--version':
                try:
                    print(pkg_resources.get_distribution('toil').version)
                except:
                    print('Version gathered from toil.version: ' + version)

        try:
            module = modules[command]
        except KeyError:
            print(("Unknown option '%s'. Pass --help to display usage information.\n" % command),
              file=(sys.stderr))
            sys.exit(1)
        else:
            del sys.argv[1]
            module.main()


def loadModules():
    from toil.utils import toilKill, toilStats, toilStatus, toilClean, toilLaunchCluster, toilDestroyCluster, toilSshCluster, toilRsyncCluster, toilDebugFile, toilDebugJob
    commandMapping = {'-'.join(map(lambda x: x.lower(), re.findall('[A-Z][^A-Z]*', name))):module for name, module in iteritems(locals())}
    return commandMapping


def printHelp(modules):
    usage = '\nUsage: {name} COMMAND ...\n       {name} --help\n       {name} COMMAND --help\n\nwhere COMMAND is one of the following:\n\n{descriptions}\n\n'
    print(usage.format(name=(os.path.basename(sys.argv[0])),
      commands=('|'.join(iterkeys(modules))),
      descriptions=('\n'.join('%s - %s' % (n, str(m.__doc__).strip()) for n, m in iteritems(modules) if m is not None))))