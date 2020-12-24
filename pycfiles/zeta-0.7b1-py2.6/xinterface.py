# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/xinterface.py
# Compiled at: 2010-03-19 11:20:12
"""Component providing eXternal Inteface access to the server"""
import sys
from sqlalchemy import insert, select
from pylons import config
from zeta.ccore import Component
from zeta.model.schema import t_staticwiki
from zeta.model import meta
import zeta.lib.helpers as h
from zeta.comp.system import SystemComponent
from zeta.comp.project import ProjectComponent
from zeta.comp.wiki import WikiComponent
from zeta.comp.ticket import TicketComponent
from zeta.comp.review import ReviewComponent

class XInterfaceComponent(Component):
    """Component to interface with external applications"""

    def system(self):
        """Get the system table entries"""
        syscomp = SystemComponent(self.compmgr)
        return (True, syscomp.get_sysentry(), '')

    def myprojects(self, user):
        """List of projects for `username`"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        projnames = sorted(h.myprojects(user))
        return (True, projnames or [], '')

    def projectdetails(self, projectname):
        """Obtain project details like,
            components, milestones, versions, teams"""
        projcomp = ProjectComponent(self.compmgr)
        (comps, mstns, vers, pusers) = projcomp.projectdetails(projectname)
        comps = [ (k, comps[k]) for k in comps ]
        mstns = [ (k, mstns[k]) for k in mstns ]
        vers = [ (k, vers[k]) for k in vers ]
        d = {'components': comps, 'milestones': mstns, 
           'versions': vers, 
           'projectusers': pusers}
        return (
         True, d, '')

    def list_sw(self):
        """List Static wiki pages"""
        q = select([t_staticwiki.c.path], bind=meta.engine)
        paths = sorted([ tup[0] for tup in q.execute().fetchall() ])
        return (True, paths, '')

    def create_sw(self, path, content='', byuser=None):
        """Create a new static wiki page"""
        syscomp = SystemComponent(self.compmgr)
        try:
            sw = syscomp.get_staticwiki(unicode(path))
            if sw:
                rc, failmsg = False, '%s, already exists' % path
            else:
                sw = syscomp.set_staticwiki(unicode(path), content, byuser=byuser)
                (rc, failmsg) = sw and (True, '') or (
                 False, 'Unable to create %s' % path)
        except:
            rc, sw, failmsg = False, None, 'Type : %s, Value : %s' % sys.exc_info()[:2]

        return (
         rc, sw, failmsg)

    def read_sw(self, path):
        """Read static wiki specified by path"""
        syscomp = SystemComponent(self.compmgr)
        sw = syscomp.get_staticwiki(path)
        d = sw and {'path': sw.path, 'text': sw.text, 
           'texthtml': sw.texthtml} or {}
        return (
         bool(d), d, 'StaticWiki %s not found' % path)

    def update_sw(self, path, content='', byuser=None):
        """Update static wiki page specified by `path`, with `content`"""
        syscomp = SystemComponent(self.compmgr)
        sw = syscomp.get_staticwiki(unicode(path))
        sw = sw and syscomp.set_staticwiki(unicode(path), unicode(content), byuser=byuser) or None
        return (bool(sw), sw, 'Unable to update static wiki %s' % path)

    def list_wiki(self, projectname):
        """List wiki urls for project `projectname`"""
        wikicomp = WikiComponent(self.compmgr)
        wikipages = [ h.wiki_parseurl(wu) for wu in wikicomp.wikiurls(projectname)
                    ]
        return (
         True, wikipages, '')

    def create_wiki(self, projectname, wikiurl, type=None, summary='', byuser=None):
        """Create a wiki page for the project `projectname`"""
        wikicomp = WikiComponent(self.compmgr)
        projcomp = ProjectComponent(self.compmgr)
        type = type and unicode(type) or unicode(c.sysentries['def_wikitype'])
        wiki = wikicomp.get_wiki(wikiurl)
        rc, wiki, failmsg = bool(wiki), wiki, 'wiki page, %s already exists' % wikiurl
        try:
            if not wiki:
                wiki = wikicomp.create_wiki(wikiurl, type, summary, creator=byuser)
                wiki and wikicomp.config_wiki(wiki, project=projectname, byuser=byuser)
                rc, wiki, failmsg = bool(wiki), wiki, 'Unable to create wiki page %s' % wikiurl
        except:
            rc, wiki, failmsg = False, None, 'Type : %s, Value : %s' % sys.exc_info()[:2]

        return (
         rc, wiki, failmsg)

    def read_wiki(self, projectname, wikiurl):
        """Read a wiki page for project `projectname`"""
        wikicomp = WikiComponent(self.compmgr)
        wiki = wikicomp.get_wiki(wikiurl)
        if wiki:
            wcnt = wikicomp.get_content(wiki)
            text = wcnt and wcnt.text or ''
            d = {'type': wiki.type.wiki_typename, 'summary': wiki.summary, 
               'text': text}
            rc, failmsg = True, ''
        else:
            rc, d, failmsg = False, {}, 'Unable to read wiki page, %s' % wikiurl
        return (
         rc, d, failmsg)

    def update_wiki(self, projectname, wikiurl, content, author):
        """Update a wiki page for project `projectname`"""
        wikicomp = WikiComponent(self.compmgr)
        wiki = wikicomp.get_wiki(wikiurl)
        try:
            if wiki:
                wpage = wikicomp.create_content(wiki, author, content)
                rc, wiki, failmsg = bool(wpage), wiki, 'Unable to update wiki page, %s' % wikiurl
            else:
                rc, wiki, failmsg = False, None, 'wiki page, %s does not exist' % wikiurl
        except:
            rc, wiki, failmsg = False, None, 'Type : %s, Value : %s' % sys.exc_info()[:2]

        return (rc, wiki, failmsg)

    def config_wiki(self, projectname, wikiurl, type=None, summary=None, byuser=None):
        """Config wiki page for project `projectname`"""
        wikicomp = WikiComponent(self.compmgr)
        wiki = wikicomp.get_wiki(wikiurl)
        if wiki:
            wikicomp.config_wiki(wiki, type=type, summary=summary, byuser=byuser)
            rc, wiki, failmsg = True, wiki, ''
        else:
            rc, wiki, failmsg = False, None, 'Invalid wiki page, %s' % wikiurl
        return (
         rc, wiki, failmsg)

    def comment_wiki(self, projectname, wikiurl, comment, commentor):
        """Comment on wiki page for project `projectname`"""
        wikicomp = WikiComponent(self.compmgr)
        wiki = wikicomp.get_wiki(wikiurl)
        if wiki and wiki.latest_version:
            wcmtdet = [
             None, commentor, wiki.latest_version, comment]
            wcmt = wikicomp.create_wikicomment(wiki, wcmtdet, byuser=commentor)
            rc, wcmt, failmsg = bool(wcmt), wcmt, 'Unable to create comment for wiki page %s' % wikiurl
        else:
            rc, wcmt, failmsg = False, None, 'Invalid wiki page, %s' % wikiurl
        return (
         rc, wcmt, failmsg)

    def wiki_tags(self, projectname, wikiurl, addtags=None, deltags=None, byuser=None):
        """Add or delete tags from wiki page"""
        wikicomp = WikiComponent(self.compmgr)
        wiki = wikicomp.get_wiki(wikiurl)
        if wiki:
            if addtags != None:
                wikicomp.add_tags(wiki, tags=addtags, byuser=byuser)
            if deltags != None:
                wikicomp.remove_tags(wiki, tags=deltags, byuser=byuser)
            rc, failmsg = True, ''
        else:
            rc, failmsg = True, 'Invalid wiki page, %s' % wikiurl
        return (
         rc, wiki, failmsg)

    def wiki_vote(self, projectname, wikiurl, vote, user):
        """Upvote or Downvote a wiki page"""
        wikicomp = WikiComponent(self.compmgr)
        wiki = wikicomp.get_wiki(wikiurl)
        if wiki:
            vote == 'up' and wikicomp.voteup(wiki, user) or vote == 'down' and wikicomp.votedown(wiki, user)
            rc, failmsg = True, ''
        else:
            rc, failmsg = False, 'Invalid wiki page, %s' % wikiurl
        return (
         rc, wiki, failmsg)

    def wiki_fav(self, projectname, wikiurl, favorite, user):
        """Add or remove wiki page as favorite"""
        wikicomp = WikiComponent(self.compmgr)
        wiki = wikicomp.get_wiki(wikiurl)
        if wiki and favorite == True:
            wikicomp.addfavorites(wiki, [user], byuser=user)
            rc, failmsg = True, ''
        elif wiki and favorite == False:
            wikicomp.delfavorites(wiki, [user], byuser=user)
            rc, failmsg = True, ''
        else:
            rc, failmsg = False, 'Invalid wiki page, %s' % wikiurl
        return (
         rc, wiki, failmsg)

    def list_ticket(self, projectname):
        """List all tickets under the project `projectname`"""
        tckcomp = TicketComponent(self.compmgr)
        tickets = dict([ (str(t[0]), t[1:]) for t in tckcomp.ticketsummary(projectname)
                       ])
        if tickets:
            rc, d, failmsg = True, {'tickets': tickets}, ''
        else:
            failmsg = 'Project %s does not have any tickets' % projectname
            rc, d = False, {}
        return (rc, d, failmsg)

    def create_ticket(self, projectname, summary, type, severity, owner, description='', components=None, milestones=None, versions=None, blocking=None, blockedby=None, parent=None):
        """Create a ticket for the project `projectname`"""
        tckcomp = TicketComponent(self.compmgr)
        projcomp = ProjectComponent(self.compmgr)
        project = projcomp.get_project(projectname)
        try:
            if project:
                tckdet = [None, summary, description, type, severity]
                tck = tckcomp.create_ticket(project, tckdet, owner=owner, byuser=owner)
                tckcomp.config_ticket(tck, components=components and [ int(id) for id in components if id ], milestones=milestones and [ int(id) for id in milestones if id ], versions=versions and [ int(id) for id in versions if id ], blocking=blocking and [ int(id) for id in blocking if id ], blockedby=blockedby and [ int(id) for id in blockedby if id ], parent=parent and int(parent), byuser=owner, append=False)
                rc, d, failmsg = True, {'id': tck.id}, ''
            else:
                rc, d, failmsg = False, {}, 'Invalid project, %s' % projectname
        except:
            rc, d, failmsg = False, {}, 'Type : %s, Value : %s' % sys.exc_info()[:2]

        return (
         rc, d, failmsg)

    def read_ticket(self, projectname, ticket):
        """Read a ticket for project `projectname`"""
        tckcomp = TicketComponent(self.compmgr)
        t = tckcomp.get_ticket(ticket)
        if t:
            d = tckcomp.ticketdetails(t)
            d.update(dict([ (k, '') for k in ['compid', 'compname', 'mstnid',
             'mstnname', 'verid', 'vername',
             'parent'] if d[k] == None
                          ]))
            d.update({'blockedby': tckcomp.blockersof(t), 
               'blocking': tckcomp.blockingfor(t), 
               'children': tckcomp.childrenfor(t)})
            rc, failmsg = True, ''
        else:
            rc, d, failmsg = False, {}, 'Invalid ticket, %s' % ticket
        return (
         rc, d, failmsg)

    def config_ticket(self, projectname, ticket, owner, summary=None, type=None, severity=None, description=None, promptuser=None, components=None, milestones=None, versions=None, blocking=None, blockedby=None, parent=None, status=None, due_date=None, byuser=None):
        """Config ticket"""
        tckcomp = TicketComponent(self.compmgr)
        t = tckcomp.get_ticket(ticket)
        projectname = unicode(projectname)
        try:
            if t:
                ts = tckcomp.get_ticket_status(t.tsh_id, attrload=['status'])
                tckcomp.config_ticket(t, type=type, severity=severity, promptuser=promptuser, components=components and [ int(id) for id in components if id ], milestones=milestones and [ int(id) for id in milestones if id ], versions=versions and [ int(id) for id in versions if id ], blocking=blocking and [ int(id) for id in blocking if id ], blockedby=blockedby and [ int(id) for id in blockedby if id ], parent=parent and int(parent), append=False, byuser=byuser)
                if summary != None or description != None:
                    tckdet = [
                     t.id, summary, description, t.type, t.severity]
                    tckcomp.create_ticket(projectname, tckdet, t.promptuser, update=True, byuser=byuser)
                if status == ts.status.tck_statusname and due_date != None or status == None and due_date != None:
                    tstatdet = [ts.id, ts.status, due_date]
                    tckcomp.create_ticket_status(t, tstatdet, owner, update=True, byuser=byuser)
                elif status:
                    tstatdet = [None, status, due_date]
                    tckcomp.create_ticket_status(t, tstatdet, owner, byuser=byuser)
                rc, failmsg = True, ''
            else:
                rc, failmsg = False, 'Invalid ticket %s' % t
        except:
            rc, failmsg = False, ' Type : %s, Value : %s' % sys.exc_info()[:2]

        return (rc, t, failmsg)

    def comment_ticket(self, projectname, ticket, comment, commentor):
        """Comment on ticket for project `projectname`"""
        tckcomp = TicketComponent(self.compmgr)
        t = tckcomp.get_ticket(ticket)
        try:
            if t:
                tcmtdet = [
                 None, comment, commentor]
                tcmt = tckcomp.create_ticket_comment(t, tcmtdet, byuser=commentor)
                rc, failmsg = bool(tcmt), 'Unable to create comment for ticket %s' % t.id
            else:
                rc, tcmt, failmsg = False, None, 'Invalid ticket, %s' % ticket
        except:
            rc, tcmt, failmsg = False, None, ' Type : %s, Value : %s' % sys.exc_info()[:2]

        return (rc, tcmt, failmsg)

    def ticket_tags(self, projectname, ticket, addtags=None, deltags=None, byuser=None):
        """Add or delete tags from ticket"""
        tckcomp = TicketComponent(self.compmgr)
        t = tckcomp.get_ticket(ticket)
        if t:
            if addtags != None:
                tckcomp.add_tags(t, tags=addtags, byuser=byuser)
            if deltags != None:
                tckcomp.remove_tags(t, tags=deltags, byuser=byuser)
            rc, failmsg = True, ''
        else:
            rc, failmsg = False, 'Invalid ticket, %s' % ticket
        return (rc, t, failmsg)

    def ticket_vote(self, projectname, ticket, vote, user):
        """Upvote or Downvote a ticket"""
        tckcomp = TicketComponent(self.compmgr)
        t = tckcomp.get_ticket(ticket)
        if t:
            vote == 'up' and tckcomp.voteup(t, user) or vote == 'down' and tckcomp.votedown(t, user)
            rc, failmsg = True, ''
        else:
            rc, failmsg = False, 'Invalid ticket, %s' % ticket
        return (rc, t, failmsg)

    def ticket_fav(self, projectname, ticket, favorite, user):
        """Add or remove ticket as favorite"""
        tckcomp = TicketComponent(self.compmgr)
        t = tckcomp.get_ticket(ticket)
        if t and favorite == True:
            tckcomp.addfavorites(t, [user], byuser=user)
            rc, failmsg = True, ''
        elif t and favorite == False:
            tckcomp.delfavorites(t, [user], byuser=user)
            rc, failmsg = True, ''
        else:
            rc, failmsg = False, 'Invalid ticket, %s' % ticket
        return (rc, t, failmsg)