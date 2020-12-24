# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DrAdm1/prjuseradd.py
# Compiled at: 2009-07-09 16:11:54
"""
  DrAdm1 utilities pack - www.dradm.org
  2009 (c) Axel <dev@axel.pp.ru>
  Under GPL v3
"""
import optparse
from mod import project
from mod.utils import *

def main():
    """ Add user to the project.
    """
    if not rootcheck():
        errexit('You need superuser privileges!')
    config = Config()
    cli = optparse.OptionParser(description='Add user to the project. Part of DrAdm1 utilities pack. http://dradm.org', version='1.0', usage='%prog [options] <user> <project>')
    cli.add_option('--verbose', '-v', help='verbose output to the console', action='store_true', default=False)
    (opt, arg) = cli.parse_args()
    if not arg:
        cli.print_help()
        exit()
    try:
        name = sanity(arg[0])
        project = sanity(arg[1])
    except:
        errexit('Arguments error.')

    try:
        group = system.SysGroup(config, project)
        if not group.exists():
            group.add()
        user = system.SysUser(config, name, project, group.getname())
        user.add()
    except system.SysError, err:
        errexit(err.msg)
    except ConfigError, err:
        errexit(err.msg)
    except SystemExit:
        pass
    except:
        errexit('Utility internal error.')

    if opt.verbose:
        print 'User %s added to %s project.' % (name, project)


if __name__ == '__main__':
    main()