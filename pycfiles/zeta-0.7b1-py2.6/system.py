# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/system.py
# Compiled at: 2010-07-09 09:25:01
"""Component to access data base and do data-crunching on system tables.
"""
from __future__ import with_statement
import os
from os.path import abspath, dirname, isdir
from sqlalchemy import *
from sqlalchemy.orm import *
from authkit.permissions import no_authkit_users_in_environ
from zeta.ccore import Component
from zeta.model import meta
from zeta.model.tables import System, StaticWiki
from zeta.lib.error import ZetaTagError
from zeta.lib.constants import LEN_TAGNAME
import zeta.lib.helpers as h, zeta.lib.cache as cache
from zeta.comp.timeline import TimelineComponent
from zeta.comp.xsearch import XSearchComponent
pjoin = os.path.join
sysentries = [
 'product_name', 'product_version', 'database_version',
 'timezone', 'unicode_encoding', 'sitename',
 'siteadmin', 'envpath',
 'userrel_types', 'projteamtypes', 'ticketstatus',
 'tickettypes', 'ticketseverity', 'reviewnatures',
 'reviewactions', 'vcstypes', 'wikitypes',
 'ticketresolv',
 'def_wikitype', 'specialtags', 'welcomestring',
 'userpanes', 'interzeta',
 'replogs', 'mailacc_offsets']

class SystemComponent(Component):
    """Component System"""

    @cache.cache('_sysentries', useargs=False)
    def _sysentries(self):
        msession = meta.Session()
        entries = dict([ (s.field, s.value) for s in msession.query(System).all()
                       ])
        return entries

    def get_sysentry(self, field=None, default=None):
        """Return the value for 'field' in the system table"""
        entries = self._sysentries()
        if field:
            return entries.get(field, default)
        return entries

    def set_sysentry(self, entries, byuser=None):
        """`entries` is a dictionary of 'field': 'value' which should be populated
        into the database."""
        tlcomp = TimelineComponent(self.compmgr)
        msession = meta.Session()
        skiplog = [
         'projteamtypes', 'tickettypes', 'ticketstatus',
         'ticketseverity', 'reviewnatures', 'reviewactions',
         'wikitypes', 'vcstypes', 'specialtags']
        with msession.begin(subtransactions=True):
            dbentries = dict(map(lambda e: (e.field, e), msession.query(System).all()))
            dbfields = dbentries.keys()
            loglines = []
            for (k, v) in entries.iteritems():
                if not isinstance(entries[k], (str, unicode)):
                    continue
                if k not in dbfields:
                    msession.add(System(k, v))
                    k not in skiplog and loglines.append('%s : %s' % (k, v))
                elif dbentries.get(k, None).value != v:
                    dbentries[k].value = v
                    k not in skiplog and loglines.append('%s : %s' % (k, v))

        loglines and tlcomp.log(byuser, 'system configuration,\n%s' % ('\n').join(loglines))
        cache.invalidate(self._sysentries)
        return

    def get_interzeta(self, name=None):
        """Get the host mapping for interzeta `name`"""
        msession = meta.Session()
        d = eval(self.get_sysentry('interzeta'))
        return name and d.get(name, '') or d

    def set_interzeta(self, maps, byuser=None):
        """set the 'host' mapping for interzeta `name`"""
        d = self.get_interzeta()
        d.update(maps)
        self.set_sysentry({'interzeta': unicode(repr(d))}, byuser=byuser)
        return maps

    def get_staticwiki(self, path=None, translate=False):
        """Get the static wiki page specified by 'path'
        Return StaticWiki"""
        msession = meta.Session()
        if path:
            sw = msession.query(StaticWiki).filter_by(path=path).first()
            translate and sw.translate(cache=True)
        else:
            sw = msession.query(StaticWiki).order_by(StaticWiki.path).all()
            translate and [ o.translate(cache=True) for o in sw ]
        return sw

    def set_staticwiki(self, path, text, byuser=None):
        """Set the static wiki page specified by 'path'"""
        tlcomp = TimelineComponent(self.compmgr)
        sw = self.get_staticwiki(path)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if sw:
                sw.text = unicode(text)
                sw.texthtml = sw.translate()
                log = 'updated static wiki page, %s' % path
                idxreplace = True
            else:
                sw = StaticWiki(unicode(path), unicode(text))
                sw.texthtml = sw.translate()
                msession.add(sw)
                log = 'created new static wiki page, %s' % path
                idxreplace = False
        srchcomp = XSearchComponent(self.compmgr)
        tlcomp.log(byuser, log)
        srchcomp.indexstaticwiki([sw], replace=idxreplace)
        return sw

    def remove_staticwiki(self, paths=None, byuser=None):
        """Remove the static wiki page identified by 'path'"""
        tlcomp = TimelineComponent(self.compmgr)
        if isinstance(paths, (str, unicode)):
            paths = [
             paths]
        swikis = self.get_staticwiki()
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if paths:
                [ msession.delete(sw) for sw in swikis if sw.path in paths ]
            else:
                [ msession.delete(sw) for sw in swikis ]
        tlcomp.log(byuser, 'deleted static wiki pages,\n%s' % (', ').join(paths))

    def pull_staticwiki(self, todir):
        """Pull static wiki pages from database and form a directory tree
        relative to 'todir'
        
        Return the list of files retrieved from the database and stored into
        the dir-tree."""
        files = []
        for sw in self.get_staticwiki():
            path = pjoin(todir, sw.path)
            if not isdir(dirname(path)):
                os.makedirs(dirname(path))
            open(path, 'w').write(sw.text)
            p = path.split(todir)[1]
            p = p[0] == os.sep and p[1:] or p
            files.append(p)

        return files

    def push_staticwiki(self, fromdir, byuser=None):
        """push static wiki pages into database by navigating the directory
        tree, 'fromdir'. Each file in the tree is considered a wiki page and
        the 'path' will be taken relative to 'fromdir'
        
        Return the list of files retrieved from the dir-tree and stored into
        the database."""
        swfiles = []
        skipped = []
        for (wpath, dirs, files) in os.walk(fromdir):
            for file in files:
                try:
                    path = unicode(pjoin(wpath.split(fromdir)[1], file))
                    path = path[0] == os.sep and path[1:] or path
                    text = unicode(open(pjoin(wpath, file)).read())
                except:
                    skipped.append(path)
                else:
                    self.set_staticwiki(path, text, byuser=byuser)
                    swfiles.append(path)

        return (
         swfiles, skipped)

    def upgradewiki(self, byuser=None):
        """Upgrade the database fields supporting wiki markup to the latest
        zwiki version"""
        tlcomp = TimelineComponent(self.compmgr)
        msession = meta.Session()
        staticwikis = self.get_staticwiki()
        with msession.begin(subtransactions=True):
            for sw in staticwikis:
                sw.texthtml = sw.translate()

        tlcomp.log(byuser, 'Upgraded static wiki pages')
        return len(staticwikis)

    def documentof(self, swiki, search='xapian'):
        """Make a document for 'staticwiki' entry to create a searchable index
            [ metadata, attributes, document ], where

            metadata   : { key, value } pairs to be associated with document
            attributes : searchable { key, value } pairs to be associated with
                         document
            document   : [ list , of, ... ] document string, with increasing
                         weightage
        """
        swiki = self.get_staticwiki(swiki.path)
        metadata = {'doctype': 'staticwiki', 'id': swiki.path}
        attributes = search == 'xapian' and [
         'XID:staticwiki_%s' % swiki.id,
         'XCLASS:site', 'XCLASS:staticwiki'] or []
        document = [
         swiki.text, swiki.path]
        return [
         metadata, attributes, document]