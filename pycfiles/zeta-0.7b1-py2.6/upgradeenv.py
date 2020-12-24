# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/upgradeenv.py
# Compiled at: 2010-07-16 08:45:23
"""Functions to upgrade environment directory to the latest version."""
import os
from os.path import join, isfile, isdir, samefile, exists
import shutil as sh
from pylons import config
from zeta.model.upgrade import upgradesw, rmsw

def cleardata(appenv):
    """Clear the application data directories, cache/ and templates/"""
    from zeta.lib.cache import cleancache
    from zeta.config.environment import cleantmplmodules
    cleancache(appenv)
    cleantmplmodules()


def upgradeenv(appver_db, defenv, appenv):
    """Upgrade to the latest version"""
    cleardata(appenv)
    if appver_db == '0.42dev':
        _upgrade_0_5b1(appver_db, defenv, appenv)
        _upgrade_0_5b2(appver_db, defenv, appenv)
        _upgrade_0_6b1(appver_db, defenv, appenv)
        _upgrade_0_6b2(appver_db, defenv, appenv)
        _upgrade_0_61b1(appver_db, defenv, appenv)
        _upgrade_0_7b1(appver_db, defenv, appenv)
    elif appver_db == '0.43dev':
        _upgrade_0_5b1(appver_db, defenv, appenv)
        _upgrade_0_5b2(appver_db, defenv, appenv)
        _upgrade_0_6b1(appver_db, defenv, appenv)
        _upgrade_0_6b2(appver_db, defenv, appenv)
        _upgrade_0_61b1(appver_db, defenv, appenv)
        _upgrade_0_7b1(appver_db, defenv, appenv)
    elif appver_db == '0.5b1':
        _upgrade_0_5b2(appver_db, defenv, appenv)
        _upgrade_0_6b1(appver_db, defenv, appenv)
        _upgrade_0_6b2(appver_db, defenv, appenv)
        _upgrade_0_61b1(appver_db, defenv, appenv)
        _upgrade_0_7b1(appver_db, defenv, appenv)
    elif appver_db == '0.5b2':
        _upgrade_0_6b1(appver_db, defenv, appenv)
        _upgrade_0_6b2(appver_db, defenv, appenv)
        _upgrade_0_61b1(appver_db, defenv, appenv)
        _upgrade_0_7b1(appver_db, defenv, appenv)
    elif appver_db == '0.6b1':
        _upgrade_0_6b2(appver_db, defenv, appenv)
        _upgrade_0_61b1(appver_db, defenv, appenv)
        _upgrade_0_7b1(appver_db, defenv, appenv)
    elif appver_db == '0.6b2':
        _upgrade_0_61b1(appver_db, defenv, appenv)
        _upgrade_0_7b1(appver_db, defenv, appenv)
    elif appver_db == '0.61b1':
        _upgrade_0_7b1(appver_db, defenv, appenv)
    else:
        print 'No upgrade required for environment directory'


def _upgradedir(defenv, appenv, relpath, overwrite=False):
    """Copy directory tree from package to deployment's environment directory"""
    srcdir = join(defenv, relpath)
    dstdir = join(appenv, relpath)
    if exists(srcdir) and exists(dstdir) and samefile(srcdir, dstdir):
        pass
    elif isdir(dstdir) and overwrite:
        sh.rmtree(dstdir)
        sh.copytree(srcdir, dstdir)
    elif isfile(dstdir) and overwrite:
        os.remove(dstdir)
        sh.copytree(srcdir, dstdir)
    else:
        sh.copytree(srcdir, dstdir)
    if not isdir(dstdir):
        raise Exception('%s is not copied' % dstfile)
    print '  Pulled dir, `%s`' % relpath


def _upgradefile(defenv, appenv, relpath, overwrite=False):
    """Copy the files from package to deployment's environment directory"""
    srcfile = join(defenv, relpath)
    dstfile = join(appenv, relpath)
    if not isfile(dstfile):
        sh.copy(srcfile, dstfile)
    elif overwrite and srcfile != dstfile:
        sh.copy(srcfile, dstfile)
    if not isfile(dstfile):
        raise Exception('%s is not copied' % dstfile)
    print '  Pulled file, `%s`' % relpath


def _rmfile(defenv, appenv, relpath):
    """Remove files from deployment's environment directory"""
    file = join(appenv, relpath)
    if isfile(file):
        os.remove(file)
    if isfile(file):
        raise Exception('%s is not removed' % file)
    print '  removed file, `%s`' % relpath


def _rmsw(paths):
    """Remove static wiki pages identified by lists of `paths`"""
    from zeta.comp.system import SystemComponent
    compmgr = config['compmgr']
    syscomp = SystemComponent(compmgr)
    for path in paths:
        syscomp = syscomp.remove_staticwiki(paths=paths, byuser='admin')
        print '  removed static wiki, `%s`' % path


def _upgrade_0_7b1(appver_db, defenv, appenv):
    """Upgrade the environment directory to 0.7b1 application version"""
    print 'Upgrading environment to 0.7b1 ...'
    print '  Copying files to environment directory ...'
    files = [('public/zdojo/zdojo.css', True),
     (
      'public/zdojo/zdojoGrid.css', True),
     (
      'public/zdojo/zdojowikiGrid.css', True),
     (
      'public/zdojo/zlib.js', True),
     (
      'public/zdojo/zwidgets.js', True),
     (
      'staticfiles/aboutus', True),
     (
      'staticfiles/frontpage', True),
     (
      'staticfiles/help/features', True),
     (
      'staticfiles/help/IniConfig', True),
     (
      'staticfiles/help/InstallPostfix', True),
     (
      'staticfiles/help/UserRegistration', True),
     (
      'staticfiles/help/installation', True),
     (
      'staticfiles/help/pms', True),
     (
      'staticfiles/help/project', True),
     (
      'staticfiles/help/ticket', True),
     (
      'staticfiles/help/pygments', True),
     (
      'staticfiles/help/PasterAdmin', True),
     (
      'staticfiles/help/StructuredText', True),
     (
      'staticfiles/help/wiki', True),
     (
      'staticfiles/help/XmlRpcApi', True),
     (
      'staticfiles/help/zwiki/ZWExtensions', True),
     (
      'staticfiles/help/zwiki/ZWMacros', True),
     (
      'staticfiles/help/zwiki/ZWTemplateTags', True),
     (
      'staticfiles/help/commercial', True),
     (
      'staticfiles/help/VimIntegration', True),
     (
      'staticfiles/help/CronJobs', True)]
    [ _upgradefile(defenv, appenv, file, overwrite=overwrite) for (file, overwrite) in files
    ]
    print '\n'
    print '  Upgrading static wiki pages to database ...'
    paths = ['aboutus',
     'frontpage',
     'help/features',
     'help/IniConfig',
     'help/InstallPostfix',
     'help/UserRegistration',
     'help/installation',
     'help/pms',
     'help/project',
     'help/ticket',
     'help/pygments',
     'help/PasterAdmin',
     'help/StructuredText',
     'help/wiki',
     'help/XmlRpcApi',
     'help/zwiki/ZWExtensions',
     'help/zwiki/ZWMacros',
     'help/zwiki/ZWTemplateTags',
     'help/commercial',
     'help/VimIntegration',
     'help/CronJobs']
    [ upgradesw(join(defenv, 'staticfiles', path), path) for path in paths ]
    print '\n'


def _upgrade_0_61b1(appver_db, defenv, appenv):
    """Upgrade the environment directory to 0.61b1 application version"""
    print 'Upgrading environment to 0.61b1 ...'
    print '  Copying directories to environment directory ...'
    dirs = [('staticfiles/help/zwiki', True),
     (
      'public/highcharts', True),
     (
      'public/zdojo/release', True),
     (
      'public/screenshots', True)]
    [ _upgradedir(defenv, appenv, dir, overwrite=overwrite) for (dir, overwrite) in dirs
    ]
    print '\n'
    print '  Copying files to environment directory ...'
    files = [('public/tckfilters.pyd', True),
     (
      'public/mstnccodes.json', True),
     (
      'public/favicon.ico', True),
     (
      'public/zeta-110x45.png', True),
     (
      'public/zenofzeta.png', True),
     (
      'public/zhighcharts.js', True),
     (
      'public/jquery-1.4.2.min.js', True),
     (
      'public/zdojo/build/zdojo.profile.js', True),
     (
      'public/zetaicons/rotating_arrow.gif', True),
     (
      'public/zetaicons/server_go.png', True),
     (
      'public/zetaicons/arrow_right.png', True),
     (
      'public/zetaicons/quote.png', True),
     (
      'public/zetaicons/chart_bar.png', True),
     (
      'public/zetaicons/star_deselected.png', True),
     (
      'public/zetaicons/star_selected.png', True),
     (
      'public/zetaicons/thumbsdown.png', True),
     (
      'public/zetaicons/thumbsdown_x.png', True),
     (
      'public/zetaicons/thumbsup.png', True),
     (
      'public/zetaicons/thumbsup_x.png', True),
     (
      'public/zetaicons/comment_add.png', True),
     (
      'public/zetaicons/comment_delete.png', True),
     (
      'public/zetaicons/time.png', True),
     (
      'public/zetaicons/tooltips.png', True),
     (
      'public/zdojo/zdojo.css', True),
     (
      'public/zdojo/zlib.js', True),
     (
      'public/zdojo/zwidgets.js', True),
     (
      'staticfiles/help/features', True),
     (
      'staticfiles/help/PasterAdmin', True),
     (
      'staticfiles/help/pygments', True),
     (
      'staticfiles/help/pms', True),
     (
      'staticfiles/help/UrlMapping', True),
     (
      'staticfiles/help/UserRegistration', True),
     (
      'staticfiles/help/GuestWiki', True),
     (
      'staticfiles/help/IniConfig', True),
     (
      'staticfiles/help/ZenOfZeta', True),
     (
      'staticfiles/help/project', True),
     (
      'staticfiles/help/XmlRpcApi', True),
     (
      'staticfiles/help/admin', True),
     (
      'staticfiles/help/review', True),
     (
      'staticfiles/help/ticket', True),
     (
      'staticfiles/help/vcs', True),
     (
      'staticfiles/help/ColorValue', True),
     (
      'staticfiles/help/InstallPostfix', True),
     (
      'staticfiles/help/acknowledgement', True),
     (
      'staticfiles/help/commercial', True),
     (
      'staticfiles/help/installation', True),
     (
      'staticfiles/help/packaging', True),
     (
      'staticfiles/help/upgradeInstallation', True),
     (
      'staticfiles/help/wiki', True),
     (
      'staticfiles/help/zwiki/ZWiki', True),
     (
      'staticfiles/help/zwiki/ZWTemplateTags', True),
     (
      'staticfiles/help/zwiki/ZWExtensions', True),
     (
      'staticfiles/help/zwiki/ZWMacros', True),
     (
      'staticfiles/help/zwiki/zetalink', True),
     (
      'staticfiles/aboutus', True),
     (
      'staticfiles/frontpage', True),
     (
      'staticfiles/p_homepage', True),
     (
      'staticfiles/tos', True)]
    [ _upgradefile(defenv, appenv, file, overwrite=overwrite) for (file, overwrite) in files
    ]
    print '\n'
    print '  Upgrading static wiki pages to database ...'
    paths = ['help/PasterAdmin',
     'help/zwiki/ZWiki',
     'help/zwiki/ZWTemplateTags',
     'help/zwiki/ZWExtensions',
     'help/zwiki/ZWMacros',
     'help/zwiki/zetalink',
     'help/features',
     'help/pygments',
     'help/pms',
     'help/UrlMapping',
     'help/UserRegistration',
     'help/GuestWiki',
     'help/IniConfig',
     'help/ZenOfZeta',
     'help/project',
     'help/XmlRpcApi',
     'help/admin',
     'help/review',
     'help/ticket',
     'help/vcs',
     'help/ColorValue',
     'help/InstallPostfix',
     'help/acknowledgement',
     'help/commercial',
     'help/installation',
     'help/packaging',
     'help/upgradeInstallation',
     'help/wiki',
     'aboutus',
     'frontpage',
     'p_homepage',
     'tos']
    [ upgradesw(join(defenv, 'staticfiles', path), path) for path in paths ]
    print '\n'
    print '  Removing static wiki pages from database ...'
    paths = ['help/ZWTemplateTags',
     'help/ZWExtensions',
     'help/ZWMacros',
     'help/zwiki']
    rmsw(paths)
    print '\n'
    print '  Removing static wiki pages from environment ...'
    files = ['staticfiles/help/ZWTemplateTags',
     'staticfiles/help/ZWExtensions',
     'staticfiles/help/ZWMacros']
    [ _rmfile(defenv, appenv, file) for file in files ]
    print '\n'


def _upgrade_0_6b2(appver_db, defenv, appenv):
    """Upgrade the environment directory to 0.6b2 application version"""
    print 'Upgrading environment to 0.6b2 ...'
    print '  Copying files to environment directory ...'
    files = [('public/zdojo/zwidgets.js', True)]
    [ _upgradefile(defenv, appenv, file, overwrite=overwrite) for (file, overwrite) in files
    ]


def _upgrade_0_6b1(appver_db, defenv, appenv):
    """Upgrade the environment directory to 0.6b1 application version"""
    print 'Upgrading environment to 0.6b1 ...'
    print '  Copying files to environment directory ...'
    files = [('public/zetaicons/plus_exp.gif', True),
     (
      'public/zdojo/ztundra.css', True),
     (
      'public/zdojo/zdojo.css', True),
     (
      'public/zdojo/zdojoGrid.css', True),
     (
      'public/zdojo/zdojowikiGrid.css', True),
     (
      'public/zdojo/zlib.js', True),
     (
      'public/zdojo/zwidgets.js', True),
     (
      'staticfiles/help/pms', True),
     (
      'staticfiles/help/vcs', True),
     (
      'staticfiles/p_homepage', True)]
    [ _upgradefile(defenv, appenv, file, overwrite=overwrite) for (file, overwrite) in files
    ]


def _upgrade_0_5b2(appver_db, defenv, appenv):
    """Upgrade the environment directory to 0.5b2 application version"""
    print 'Upgrading environment to 0.5b2 ...'
    print '  Copying files to environment directory ...'
    files = [('public/zdojo/zdojo.css', True),
     (
      'public/zdojo/ztundra.css', True),
     (
      'public/zdojo/zlib.js', True),
     (
      'public/zdojo/zwidgets.js', True)]
    [ _upgradefile(defenv, appenv, file, overwrite=overwrite) for (file, overwrite) in files
    ]
    print '  Copying directories to environment directory ...'
    dirs = [('public/zdojo/release', True)]
    [ _upgradedir(defenv, appenv, dir, overwrite=overwrite) for (dir, overwrite) in dirs
    ]


def _upgrade_0_5b1(appver_db, defenv, appenv):
    """Upgrade the environment directory to 0.5b1 application version"""
    print 'Upgrading environment to 0.5b1 ...'
    print '  Copying files to environment directory ...'
    files = [('public/tckfilters.pyd', False),
     (
      'public/zetaicons/arrow_refresh.png', False),
     (
      'staticfiles/help/ColorValue', True),
     (
      'staticfiles/help/PasterAdmin', True),
     (
      'staticfiles/help/XmlRpcApi', True),
     (
      'staticfiles/help/ZWExtensions', True),
     (
      'staticfiles/help/ZWMacros', True),
     (
      'staticfiles/help/ZWTemplateTags', True),
     (
      'staticfiles/help/admin', True),
     (
      'staticfiles/help/features', True),
     (
      'staticfiles/help/pms', True),
     (
      'staticfiles/help/review', True),
     (
      'staticfiles/help/ticket', True),
     (
      'staticfiles/help/vcs', True),
     (
      'staticfiles/help/zwiki', True)]
    [ _upgradefile(defenv, appenv, file, overwrite=overwrite) for (file, overwrite) in files
    ]
    srcfile = join(defenv, 'staticfiles/p_homepage')
    dstfile = join(appenv, 'staticfiles/p_homepage')
    oldfile = join(appenv, 'staticfiles/p_frontpage')
    if isfile(oldfile):
        os.remove(oldfile)
    if not isfile(dstfile):
        sh.copy(srcfile, dstfile)
    if isfile(oldfile):
        raise Exception('oldfile, %s is not removed' % oldfile)
    if not isfile(dstfile):
        raise Exception('%s is not copied' % dstfile)
    print 'Pulled staticfiles/p_homepage'