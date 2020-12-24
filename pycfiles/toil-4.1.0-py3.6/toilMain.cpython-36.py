# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilMain.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 1749 bytes
import os, sys, re, textwrap, pkg_resources
from toil.version import version

def main():
    modules = loadModules()
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        printHelp(modules)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == '--version':
        printVersion()
        sys.exit(0)
    try:
        module = modules[cmd]
        del sys.argv[1]
        module.main()
    except KeyError:
        sys.stderr.write(f'Unknown option "{cmd}".  Pass --help to display usage information.\n')
        sys.exit(1)


def loadModules():
    from toil.utils import toilKill, toilStats, toilStatus, toilClean, toilLaunchCluster, toilDestroyCluster, toilSshCluster, toilRsyncCluster, toilDebugFile, toilDebugJob
    return {'-'.join([i.lower() for i in re.findall('[A-Z][^A-Z]*', name)]):module for name, module in locals().items()}


def printHelp(modules):
    name = os.path.basename(sys.argv[0])
    descriptions = '\n        '.join(f"{cmd} - {mod.__doc__.strip()}" for cmd, mod in modules.items() if mod)
    print(textwrap.dedent(f"\n        Usage: {name} COMMAND ...\n               {name} --help\n               {name} COMMAND --help\n\n        Where COMMAND is one of the following:\n        \n        {descriptions}\n        "[1:]))


def printVersion():
    try:
        print(pkg_resources.get_distribution('toil').version)
    except:
        print(f"Version gathered from toil.version: {version}")