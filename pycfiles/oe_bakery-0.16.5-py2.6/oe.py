# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oebakery/oe.py
# Compiled at: 2010-01-22 08:58:51
import sys, dircache, subprocess, os, string, re, glob, hashlib

def main():
    usage = "Usage: oe <command> [options]*\n\nAllowed oe commands are:\n  init        Setup new OE Bakery development environment\n  clone       Clone an OE Bakery development environment into a new directory\n  update      Update OE Bakery development environment accoring to configuration\n  pull        Pull updates from remote repositories\n  tmp         Manage TMPDIR directories\n  bake        Build recipe (call bitbake)\n  ingredient  Manage ingredient (downloaded sources) files\n  prebake     Manage prebake (packaged staging) files\n\nSee 'oe <command> -h' or 'oe help <command> for more information on a\nspecific command."
    if len(sys.argv) < 2 or len(sys.argv) == 2 and sys.argv[1] == '-h':
        print usage
        return
    if sys.argv[1] == 'help':
        if len(sys.argv) == 3:
            sys.argv[1] = sys.argv[2]
            sys.argv[2] = '-h'
        else:
            print usage
            return
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    import oebakery
    from oebakery.cmd_init import InitCommand
    from oebakery.cmd_clone import CloneCommand
    from oebakery.cmd_update import UpdateCommand
    from oebakery.cmd_pull import PullCommand
    from oebakery.cmd_tmp import TmpCommand
    from oebakery.cmd_bake import BakeCommand
    from oebakery import misc
    if sys.argv[1] == 'init':
        cmd = InitCommand(sys.argv[2:])
        return cmd.run()
    if sys.argv[1] == 'clone':
        cmd = CloneCommand(sys.argv[2:])
        return cmd.run()
    topdir = oebakery.locate_topdir()
    if topdir != os.environ['PWD']:
        oebakery.chdir(topdir)
    config = oebakery.read_config()
    if sys.argv[1] == 'update':
        cmd = UpdateCommand(config, sys.argv[2:])
    elif sys.argv[1] == 'pull':
        cmd = PullCommand(config, sys.argv[2:])
    elif sys.argv[1] == 'tmp':
        cmd = TmpCommand(config, sys.argv[2:])
    elif sys.argv[1] == 'bake':
        cmd = BakeCommand(config, sys.argv[2:])
    elif sys.argv[1] == 'ingredient':
        cmd = IngredientCommand(config, sys.argv[2:])
    elif sys.argv[1] == 'prebake':
        cmd = PrebakeCommand(config, sys.argv[2:])
    else:
        print usage
        sys.exit(1)
    return cmd.run()


if __name__ == '__main__':
    main()