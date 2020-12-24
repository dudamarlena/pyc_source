# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DrAdm1/prjadd.py
# Compiled at: 2009-07-13 23:22:00
"""
  DrAdm1 utilities pack - www.dradm.org
  2009 (c) Axel <dev@axel.pp.ru>
  Under GPL v3
"""
import optparse, signal
from mod import changelog, project, utils
from mod.utils import *

def main():
    """ Add new project.
    """
    if not rootcheck():
        errexit('You need superuser privileges!')
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        config = Config()
        config.security()
    except (UtilityError, ConfigError), err:
        errexit(err.msg)

    cli = optparse.OptionParser(description='Setup directory for the new project. Part of DrAdm1 utilities pack. http://dradm.org', version='1.0', usage='%prog [options] <project>')
    cli.add_option('--verbose', '-v', help='verbose output to the console', action='store_true', default=False)
    (opt, arg) = cli.parse_args()
    try:
        chlog = changelog.Changelog(config, cli.get_prog_name())
    except changelog.ChangelogError, err:
        errexit(err.msg)

    if not arg:
        chlog.news()
        exit()
    try:
        prjname = sanity(arg[0])
        prj = project.Project(config, prjname)
        prj.add()
        chlog.project_set(prjname)
        chlog.add('Project %s created.' % prjname)
        if opt.verbose:
            print 'Project %s created OK.' % prjname
    except (project.ProjectError, changelog.ChangelogError, ConfigError), err:
        errexit(err.msg)
    except SystemExit:
        pass
    except:
        errexit('Utility internal error.')


if __name__ == '__main__':
    main()