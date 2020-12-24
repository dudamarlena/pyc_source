# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/model/upgrade.py
# Compiled at: 2010-07-08 23:38:44
"""Functions to upgrade database from a previous version to current version.
The Database version is store in the 'system' table, while the current
database version supported by the application is available from the code.

"""
from __future__ import with_statement
import os
from os.path import join, isfile, dirname, splitext, basename
from hashlib import sha1
from pylons import config
from zeta.model.tables import *
from zeta.model import meta
from zeta.lib.error import *
from zeta.comp.system import SystemComponent
from zeta.comp.vcs import VcsComponent
g_user = 'admin'

def _sequence(dbver_db, dbver_app):
    """Sequence the upgradation from the current database version to the
    current database version supported by app"""
    versions = dbversion_keys
    index_db = versions.index(dbver_db)
    index_app = versions.index(dbver_app)
    if index_app < index_db:
        raise ZetaError("Application's DB version is less than or equal to Database version")
    elif index_app == index_db:
        print 'No upgrade required for database'
    return versions[index_db:index_app]


def upgradedb(dbver_db, dbver_app, defenv, appenv):
    """Upgrade the database from its current version to application compatible
    version"""
    for ver in _sequence(dbver_db, dbver_app):
        print 'Upgrading database from version %s ...' % ver
        dbversions[ver](defenv, appenv)


def upgradesw(file, path):
    """Helper function to push static wiki pages from File System to DB"""
    compmgr = config['compmgr']
    syscomp = SystemComponent(compmgr)
    print '  Pushing static-wiki page `%s` into Database ...' % path
    if isfile(file):
        syscomp.set_staticwiki(unicode(path), unicode(open(file).read()), byuser='admin')
    else:
        raise Exception('help/PasterAdmin file not found')


def rmsw(paths):
    """Remove static wiki pages identified by lists of `paths`"""
    compmgr = config['compmgr']
    syscomp = SystemComponent(compmgr)
    for path in paths:
        syscomp.remove_staticwiki(paths=path, byuser='admin')
        print '  removed static wiki, `%s`' % path


def upgradewithscripts(fromver, defenv, appenv):
    """Helper function detects sql scripts for each type of database and
    applies them to the current database.
    This way of upgrade is typically used for altering table schemas
    """
    scriptdir = join(dirname(__file__), 'upgradescripts')
    dbtype = meta.engine.name
    scripts = [ join(scriptdir, f) for f in os.listdir(scriptdir) if basename(f) == '%s.%s' % (fromver, dbtype)
              ]
    connection = meta.engine.connect()
    for script in scripts:
        print '  From script %s ...' % script
        stmts = open(script).read().split('\n\n')
        for stmt in stmts:
            print '  Executing statement \n  %s' % stmt
            connection.execute(stmt)

    connection.close()


def upgrade_0_7(defenv, appenv):
    """Upgrade Database version from 0.7 to 0.8"""
    userscomp = config['userscomp']
    print "Converting 'password' column values into message digest ..."
    users = userscomp.get_user()
    oldpass = dict([ (u.username, u.password) for u in users ])
    msession = meta.Session()
    with msession.begin(subtransactions=True):
        for u in users:
            u.password = sha1(u.password).hexdigest()

    newpass = dict([ (u.username, u.password) for u in userscomp.get_user() ])
    assert len(newpass) == len(oldpass)
    for u in oldpass:
        assert unicode(newpass[u]) == unicode(sha1(oldpass[u]).hexdigest())

    print 'Converted %s user passwords' % len(users)


def upgrade_0_8(defenv, appenv):
    """Upgrade Database version from 0.8 to 0.9"""
    compmgr = config['compmgr']
    syscomp = SystemComponent(compmgr)
    print 'Renaming static-wiki `p_frontpage` to `p_homepage` ...'
    sw = syscomp.get_staticwiki('p_frontpage')
    msession = meta.Session()
    with msession.begin(subtransactions=True):
        sw.path = 'p_homepage'
    paths = ['help/ColorValue',
     'help/PasterAdmin',
     'help/XmlRpcApi',
     'help/ZWExtensions',
     'help/ZWMacros',
     'help/ZWTemplateTags',
     'help/admin',
     'help/features',
     'help/pms',
     'help/review',
     'help/ticket',
     'help/vcs',
     'help/zwiki']
    [ upgradesw(join(defenv, 'staticfiles', path), path) for path in paths ]


def upgrade_0_9(defenv, appenv):
    """Upgrade database version from 0.9 to 1.0"""
    compmgr = config['compmgr']
    syscomp = SystemComponent(compmgr)
    print '  Adding `regrbyinvite` (default False) field to system table ...\n'
    entry = {'regrbyinvite': 'False'}
    syscomp.set_sysentry(entry, byuser=g_user)
    print '  Adding `invitebyall` (default False) field to system table ...\n'
    entry = {'invitebyall': 'False'}
    syscomp.set_sysentry(entry, byuser=g_user)
    print '  Adding `googlemaps` (default False) field to system table ...\n'
    entry = {'googlemaps': ''}
    syscomp.set_sysentry(entry, byuser=g_user)
    print '  Moving `strictauth` (%s) field to system table ...\n' % config['zeta.strictauth']
    entry = {'strictauth': unicode(config['zeta.strictauth'])}
    syscomp.set_sysentry(entry, byuser=g_user)
    upgradewithscripts('0_9', defenv, appenv)
    print '  Creating table for `userinvitation`\n'
    meta.metadata.create_all(bind=meta.engine, checkfirst=True)
    paths = [
     'help/pms',
     'help/vcs',
     'p_homepage']
    [ upgradesw(join(defenv, 'staticfiles', path), path) for path in paths ]


def upgrade_1_0(defenv, appenv):
    """Upgrade database version from 1.0 to 1.1"""
    import zeta.lib.helpers as h
    compmgr = config['compmgr']
    syscomp = SystemComponent(compmgr)
    vcscomp = VcsComponent(compmgr)
    print '  Creating table for `ticket_filters`, `reviewset`, `vcsmount`\n'
    meta.metadata.create_all(bind=meta.engine, checkfirst=True)
    print '  `googlemaps` should specify the generated key (No more boolean) ...\n'
    entry = {'googlemaps': ''}
    syscomp.set_sysentry(entry, byuser=g_user)
    print '  Changing permission name ZETA_ADMIN to SITE_ADMIN'
    userscomp = config['userscomp']
    userscomp.change_permname('ZETA_ADMIN', 'SITE_ADMIN', byuser='admin')
    vcstypes = syscomp.get_sysentry('vcstypes')
    vcstypes = h.parse_csv(vcstypes)
    if 'bzr' not in vcstypes:
        print '  Adding `bzr` vcstype to system table'
        vcstypes = (', ').join(vcstypes + ['bzr'])
        syscomp.set_sysentry({'vcstypes': vcstypes}, byuser='admin')
        print '  Adding `bzr` vcstype to vcs_type table'
        vcscomp.create_vcstype(['bzr'], byuser='admin')


dbversion_keys = [
 '0.7', '0.8', '0.9', '1.0', '1.1']
dbversions = {'0.7': upgrade_0_7, 
   '0.8': upgrade_0_8, 
   '0.9': upgrade_0_9, 
   '1.0': upgrade_1_0, 
   '1.1': None}