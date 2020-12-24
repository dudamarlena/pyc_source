# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/model/create.py
# Compiled at: 2010-06-12 02:48:47
"""Setup the Tables and populate them with initial values"""
from __future__ import with_statement
import os
from hashlib import sha1
from pylons import config
from zeta.model import meta
from zeta.model.tables import *
from zeta.lib.constants import *
__all__ = [
 'create_models', 'delete_models']
g_byuser = 'admin'

def _system_table(config, sysentries_cfg):
    """`entries` is a dictionary of 'field': 'value' which should be populated
    into the database."""
    from zeta.comp.system import SystemComponent
    compmgr = config['compmgr']
    syscomp = SystemComponent(compmgr)
    syscomp.set_sysentry(sysentries_cfg, byuser=g_byuser)


def _permissions(config, permissions):
    userscomp = config['userscomp']
    userscomp.create_apppermissions(permissions, byuser=g_byuser)


def _user_table(config):
    userscomp = config['userscomp']
    msession = meta.Session()
    with msession.begin(subtransactions=True):
        admin = User(unicode(config['zeta.siteadmin']), ADMIN_EMAIL, sha1(ADMIN_PASSWORD).hexdigest(), DEFAULT_TIMEZONE)
        admininfo = UserInfo(config['zeta.siteadmin'], config['zeta.siteadmin'], config['zeta.siteadmin'], None, None, None, None, None, None, None)
        admin.userinfo = admininfo
        msession.add(admin)
        anony = User('anonymous', ANONYMOUS_EMAIL, sha1(ANONYMOUS_PASSWORD).hexdigest(), DEFAULT_TIMEZONE)
        anonyinfo = UserInfo('anonymous', 'anonymous', 'anonymous', None, None, None, None, None, None)
        anony.userinfo = anonyinfo
        msession.add(anony)
    return


def _userrelation_types(config):
    userscomp = config['userscomp']
    userscomp.userreltype_create(config['zeta.userrel_types'], byuser=g_byuser)


def _projteam_types(config):
    from zeta.comp.project import ProjectComponent
    compmgr = config['compmgr']
    projcomp = ProjectComponent(compmgr)
    projcomp.create_projteamtype(config['zeta.projteamtypes'], byuser=g_byuser)


def _ticket_type(config):
    from zeta.comp.ticket import TicketComponent
    compmgr = config['compmgr']
    tckcomp = TicketComponent(compmgr)
    tckcomp.create_tcktype(config['zeta.tickettypes'], byuser=g_byuser)


def _ticket_status(config):
    from zeta.comp.ticket import TicketComponent
    compmgr = config['compmgr']
    tckcomp = TicketComponent(compmgr)
    tckcomp.create_tckstatus(config['zeta.ticketstatus'], byuser=g_byuser)


def _ticket_severity(config):
    from zeta.comp.ticket import TicketComponent
    compmgr = config['compmgr']
    tckcomp = TicketComponent(compmgr)
    tckcomp.create_tckseverity(config['zeta.ticketseverity'], byuser=g_byuser)


def _reviewcomment_nature(config):
    from zeta.comp.review import ReviewComponent
    compmgr = config['compmgr']
    revcomp = ReviewComponent(compmgr)
    revcomp.create_reviewnature(config['zeta.reviewnatures'], byuser=g_byuser)


def _reviewcomment_action(config):
    from zeta.comp.review import ReviewComponent
    compmgr = config['compmgr']
    revcomp = ReviewComponent(compmgr)
    revcomp.create_reviewaction(config['zeta.reviewactions'], byuser=g_byuser)


def _vcs_type(config):
    from zeta.comp.vcs import VcsComponent
    compmgr = config['compmgr']
    vcscomp = VcsComponent(compmgr)
    vcscomp.create_vcstype(config['zeta.vcstypes'], byuser=g_byuser)


def _wiki_type(config):
    from zeta.comp.wiki import WikiComponent
    compmgr = config['compmgr']
    wikicomp = WikiComponent(compmgr)
    wikicomp.create_wikitype(config['zeta.wikitypes'], byuser=g_byuser)


def _special_tags(config):
    from zeta.comp.tag import TagComponent
    compmgr = config['compmgr']
    tagcomp = TagComponent(compmgr)
    for tagname in config['zeta.specialtags']:
        tagcomp.create_tag(tagname, byuser=g_byuser)


def _staticwiki(config):
    from zeta.comp.system import SystemComponent
    compmgr = config['compmgr']
    rootdir = os.path.abspath(os.path.join(config['zeta.envpath'], DIR_STATICWIKI))
    syscomp = SystemComponent(compmgr)
    print '   Pushing static files from %s ... ' % rootdir
    (files, skipped) = syscomp.push_staticwiki(rootdir, byuser=g_byuser)
    for f in files:
        print '    ', f

    print '   Skipped files ... '
    for f in skipped:
        print '    ', f


def create_models(engine, config, tables=None, sysentries_cfg=None, permissions=None):
    """Create all the Tables."""
    meta.metadata.create_all(bind=engine, checkfirst=True, tables=tables)
    _user_table(config)
    if sysentries_cfg:
        _system_table(config, sysentries_cfg)
    if permissions:
        _permissions(config, permissions)
    _userrelation_types(config)
    _projteam_types(config)
    _ticket_status(config)
    _ticket_type(config)
    _ticket_severity(config)
    _reviewcomment_nature(config)
    _reviewcomment_action(config)
    _vcs_type(config)
    _wiki_type(config)
    _special_tags(config)
    _staticwiki(config)


def delete_models(engine, tables=None):
    meta.metadata.drop_all(bind=engine, tables=tables)
    meta.Session.close_all()