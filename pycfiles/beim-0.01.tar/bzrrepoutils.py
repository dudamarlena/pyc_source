# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/bzrrepoutils.py
# Compiled at: 2013-12-08 21:45:16
import os

def checkoutCmd(server, repo, branch, revision=None, name=None):
    """checkoutCmd( "bzr+ssh://pyre.cacr.caltech.edu", "home/projects/pyre/web/repository", "1.0/pyre.db-jiao-experiment")
    """
    if name is None:
        raise ValueError('name is None')
    cmd = [
     'bzr branch']
    if revision:
        cmd.append('-r %s' % revision)
    cmd.append('%(server)s/%(repo)s/%(branch)s %(name)s' % locals())
    return (' ').join(cmd)


def updateCmd(revision=None):
    cmd = 'bzr pull'
    if revision:
        cmd += ' -r %s' % revision
    return cmd


def repourl(repo, branch, server='bzr://danse.us'):
    return '%(server)s/%(repo)s/%(branch)s' % locals()


def repoinfo(repo, branch, server=None, revision=None, name=None):
    if name is None:
        raise ValueError('name is None')
    path = name
    coCmd = checkoutCmd(server, repo, branch, revision=revision, name=name)
    updateCmd = 'bzr update'
    return (path, coCmd, updateCmd)