# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/testing.py
# Compiled at: 2008-04-29 08:14:25
import os, shutil, iw.email.testing, zc.buildout.testing
from zc.buildout.testing import system, rmdir, mkdir
from zc.buildout.testing import normalize_path

def svn_start(test, project=None):
    """create a test server
    """
    sample = test.globs['sample_buildout']
    base = os.path.split(sample)[0]
    root = os.path.split(base)[0]
    os.chdir(root)
    system('svnadmin create %s/repos' % root)
    svn = 'file://%s' % os.path.join(root, 'repos')
    if project:
        sample = project
    project = os.path.split(sample)[1]
    mkdir(root, 'tmp')
    mkdir(root, 'tmp', project)
    mkdir(root, 'tmp', project, 'tags')
    mkdir(root, 'tmp', project, 'branches')
    shutil.copytree(sample, os.path.join(root, 'tmp', project, 'trunk'))
    os.chdir(os.path.join(root, 'tmp'))
    system('svn import %s/ -m ""' % svn)
    rmdir(root, 'tmp')
    os.chdir(base)
    rmdir(sample)
    test.globs.update(test_dir=base, svn_url=svn)


def customBuildoutSetup(test):
    """default buildout differs a bit"""
    zc.buildout.testing.buildoutSetUp(test)
    base = test.globs['sample_buildout']
    buildout_cfg = os.path.join(base, 'buildout.cfg')
    content = open(buildout_cfg).read()
    content = content.replace('[buildout]', '[buildout]\ndownload-cache=downloads')
    f = open(buildout_cfg, 'w')
    try:
        f.write(content)
    finally:
        f.close()
    dnl = os.path.join(base, 'downloads')
    os.mkdir(dnl)
    source = os.path.join(os.path.dirname(__file__), 'bootstrap.py')
    target = os.path.join(base, 'bootstrap.py')
    shutil.copyfile(source, target)


def releaserSetUp(test):
    customBuildoutSetup(test)
    test.globs['test'] = test
    test.globs['svn_start'] = svn_start
    iw.email.testing.smtpSetUp()


def releaserTearDown(test):
    zc.buildout.testing.buildoutTearDown(test)
    iw.email.testing.smtpTearDown()


def clearBuildout(test=None):
    zc.buildout.testing.buildoutTearDown(test)
    customBuildoutSetup(test)


def clearRepository(test, project=''):
    zc.buildout.testing.buildoutTearDown(test)
    customBuildoutSetup(test)
    svn_start(test, project)