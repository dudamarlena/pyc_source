# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/claw/miniconda/lib/python2.7/site-packages/activegit/cli.py
# Compiled at: 2016-08-01 13:46:25
import click
from sh import git
import activegit

@click.command()
@click.argument('repopath', type=str)
@click.option('--bare', type=bool, default=True)
@click.option('--shared', type=str, default='group')
def initrepo(repopath, bare, shared):
    """ Initialize an activegit repo. 
    Default makes base shared repo that should be cloned for users """
    ag = activegit.ActiveGit(repopath, bare=bare, shared=shared)


@click.command()
@click.argument('barerepo', type=str)
@click.argument('userrepo', type=str)
def clonerepo(barerepo, userrepo):
    """ Clone a bare base repo to a user """
    git.clone(barerepo, userrepo)
    ag = activegit.ActiveGit(userrepo)