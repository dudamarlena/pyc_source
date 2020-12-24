# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/controllers/xmlrpc.py
# Compiled at: 2010-07-10 08:17:47
"""Controller module to interface with client XMLRPC requests"""
from __future__ import with_statement
import logging, os, datetime as dt
from pylons import request, response
from pylons import config
from pylons import session
from pylons import tmpl_context as c
from pylons.controllers.util import abort
from pylons.controllers import XMLRPCController
from authkit.permissions import no_authkit_users_in_environ
from pytz import all_timezones, timezone
from zeta.ccore import Component
from zeta.config.routing import r_xmlrpc
from zeta.model import meta
from zeta.lib.error import *
from zeta.lib.base import BaseController, render
from zeta.lib.constants import *
from zeta.lib.view import viewcontext
import zeta.lib.helpers as h
from zeta.lib.error import ZetaFormError
from zeta.config.environment import beforecontrollers, aftercontrollers
from zeta.comp.system import SystemComponent
from zeta.comp.xinterface import XInterfaceComponent
from zeta.auth.perm import init_pms
log = logging.getLogger(__name__)
compmgr = None
syscomp = None
xicomp = None

def do_onetime():
    global compmgr
    global syscomp
    global xicomp
    if compmgr == None:
        compmgr = config['compmgr']
        syscomp = SystemComponent(compmgr)
        xicomp = XInterfaceComponent(compmgr)
    return


authzfail = {'rpcstatus': 'fail', 'message': 'Not authorized'}
authtfail = {'rpcstatus': 'fail', 'message': 'Not authenticated'}

def _result(rpcstatus, failmsg='', d={}):
    if rpcstatus:
        res = {'rpcstatus': 'ok'}
    else:
        res = {'rpcstatus': 'fail', 'message': failmsg}
    res.update(d)
    return res


class XmlrpcController(XMLRPCController):
    """Controller providing XMLRPC interface"""

    def __before__(self, environ=None):
        """Called before calling any actions under this controller"""
        do_onetime()
        c.username = request.params.get('username', None)
        c.password = request.params.get('password', None)
        environ = request.environ
        userscomp = environ['authkit.users']
        config['userscomp'] = userscomp
        if not config.has_key('c'):
            config['c'] = c
        c.sysentries = syscomp.get_sysentry()
        init_pms()
        user = userscomp.get_user(unicode(c.username))
        if user and user.password == c.password:
            c.authuser = user
            c.authusername = user.username
        else:
            c.authuser = None
            c.authusername = ''
        return

    def _marshalNone(self, val, default='None'):
        """`None` python data-type is not supported by XMLRPC, instead, it is
        marshalled as 'None' string"""
        if val == None:
            return default
        else:
            if isinstance(val, list):
                newlist = []
                [ newlist.append([v, default][(v == None)]) for v in val ]
                return newlist
            else:
                return val
            return

    def _demarshalNone(self, *args):
        """Interpret 'None' as None"""

        def translate(arg):
            if arg == 'None':
                return
            else:
                if isinstance(arg, list):
                    newlist = []
                    [ newlist.append([l, None][(l == 'None')]) for l in arg ]
                    return newlist
                else:
                    return arg
                return

        if len(args) == 1:
            return translate(args[0])
        if len(args) > 1:
            return [ translate(arg) for arg in args ]

    def _stripurl(self, url):
        """`url` to identify wiki pages and static wiki pages will have to be
        striped off `spaces`, `tabs`, and leading '/'"""
        return unicode(url.strip(' \t').lstrip('/'))

    def _permissions(self, user, authz):
        """Check for successful authentication and authorization"""
        if not user:
            res = authtfail
        elif not authz:
            res = authzfail
        else:
            res = {}
        return res

    def system(self):
        """
        === System()
        
        :Description ::
            Get the system table entries,

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus' : 'ok',
                  'entries'   : { key : value, .... }
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, True)
        (rc, entries, failmsg) = xicomp.system()
        return res or _result(True, d={'entries': entries})

    def myprojects(self):
        """
        === myprojects()
        :Description ::
            List of participating projects, by the requesting user,

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus'    : 'ok',
                  'projectnames' : [ <projectname>, <projectname>, .... ]
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, True)
        (rc, projnames, failmsg) = xicomp.myprojects(c.authuser)
        return res or _result(True, d={'projectnames': projnames})

    def projectdetails(self, projectname):
        """
        === projectdetails( projectname )
        
        :Description ::
            Project details like components, milestones, versions, teams for
            project, `projectname`,

        Positional arguments,
        |= projectname | name of the project for which the details are required

        :Return::
            On success,
                [<PRE
                { 'rpcstatus'    : 'ok',
                  'components'   : [ ( <compid>, <compname> ), ... ],
                  'milestones'   : [ ( <mstnid>, <milestonename> ), ... ],
                  'versions'     : [ ( <verid>, <versionname> ), ...   ],
                  'projectusers' : [ username, ... ],
                  
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, True)
        (rc, details, failmsg) = xicomp.projectdetails(unicode(projectname))
        return res or _result(True, d=details)

    def liststaticwikis(self):
        """
        === liststaticwikis()

        :Description ::
            List all the static wiki page names,

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus' : 'ok',
                  'paths'     : [ <path-url>, <path-url>, .... ]
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, True)
        (rc, paths, failmsg) = xicomp.list_sw()
        return res or _result(True, d={'paths': paths})

    def newstaticwiki(self, path, content):
        """
        === newstaticwiki( path, content )

        :Description ::
            Create a new static wiki page, under path-url `path`, published
            with `content`
        
        Positional arguments,
        |= path     | url-path, for the new static wiki page
        |= content  | wiki text to publish.

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('STATICWIKI_CREATE')))
        path = self._stripurl(path)
        (rc, sw, failmsg) = xicomp.create_sw(path, unicode(content))
        return res or _result(rc, failmsg=failmsg)

    def staticwiki(self, path):
        """
        === staticwiki( path )

        :Description ::
            Read a static wiki page from url `path`

        Positional arguments,
        |= path     | a valid and existing url-path

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus' : 'ok',
                  'path'      : <path-url>,
                  'text'      : <wiki-text>,
                  'texthtml'  : <html-text>,
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, True)
        path = self._stripurl(path)
        (rc, d, failmsg) = xicomp.read_sw(path)
        return res or _result(rc, d=d, failmsg=failmsg)

    def publishstaticwiki(self, path, content):
        """
        === publishstaticwiki( path, content )

        :Description ::
            Publish new content, (or updated content) onto a static wiki page,

        Positional arguments,
        |= path     | a valid and existing url-path
        |= content  | wiki text to publish

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('STATICWIKI_CREATE')))
        path = self._stripurl(path)
        (rc, sw, failmsg) = xicomp.update_sw(path, unicode(content))
        return res or _result(rc, failmsg=failmsg)

    def listwikipages(self, projectname):
        """
        === listwikipage( projectname )

        :Description ::
            List wiki pages under project, `projectname`,

        Positional arguments,
        |= projectname | a valid project-name

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus' : 'ok',
                  'wikipages' : [ <page-name>, <page-name>, .... ]
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('WIKI_VIEW')))
        (rc, wikipages, failmsg) = xicomp.list_wiki(unicode(projectname))
        return res or _result(True, d={'wikipages': sorted(wikipages)})

    def newwikipage(self, projectname, pagename, type, summary):
        """
        === newwikipage( projectname, type, summary )

        :Description ::
            Create a new wiki-page for project, `projectname`.

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | new wiki page-name under project,
        |= type        | type of wiki page, if False, default type will be used
        |= summary     | summary string, if False, will assume empty string

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('WIKI_CREATE')))
        (type, summary) = self._demarshalNone(type, summary)
        (rc, wiki, failmsg) = xicomp.create_wiki(unicode(projectname), wikiurl, type=unicode(type), summary=unicode(summary), byuser=c.authuser)
        return res or _result(rc, failmsg=failmsg)

    def wiki(self, projectname, pagename):
        """
        === wiki( projectname, pagename )

        :Description ::
            Read wiki-page `pagename`, for project, `projectname`,

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | valid and existing wiki page-name

        :Return ::
            On success,
                { 'rpcstatus' : 'ok',
                  'type'      : <wiki type string>
                  'summary'   : <wiki summary string>
                  'text'      : <wiki text string>
                }
            On failure,
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                }
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('WIKI_VIEW')))
        (rc, d, failmsg) = xicomp.read_wiki(unicode(projectname), wikiurl)
        for k in d:
            d[k] = self._marshalNone(d[k])

        return res or _result(rc, d=d, failmsg=failmsg)

    def publishwiki(self, projectname, pagename, content):
        """
        === publishwiki( projectname, pagename, content )
        
        :Description ::
            Publish new content, (or updated content) for wiki-page `pagename`,
            under project, `projectname`,

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | valid and existing wiki page-name
        |= content     | content to be published (as the next version).

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        author = c.authuser
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('WIKI_CREATE')))
        (rc, wiki, failmsg) = xicomp.update_wiki(unicode(projectname), wikiurl, unicode(content), author)
        return res or _result(rc, failmsg=failmsg)

    def configwiki(self, projectname, pagename, type, summary):
        """
        === configwiki( projectname, pagename, type, summary )
        
        :Description ::
            Config wiki-page, `pagename` under project, `projectname`,

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | valid and existing wiki page-name
        |= type        | type of wiki page, if False, will be skipped
        |= summary     | summary string, if False, will be skipped

        On success,
            [<PRE { 'rpcstatus'  : 'ok' } >]
        On failure,
            [<PRE
            { 'rpcstatus' : 'fail',
              'message'   : <msg string indicating reason for failure>
            } >]
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('WIKI_CREATE')))
        (type, summary) = self._demarshalNone(type, summary)
        (rc, wiki, failmsg) = xicomp.config_wiki(unicode(projectname), wikiurl, type, summary)
        return res or _result(rc, failmsg=failmsg)

    def commentonwiki(self, projectname, pagename, comment):
        """
        === commentonwiki( projectname, pagename, comment )

        :Description ::
            Comment on wiki-page, `pagename under project, `projectname`,

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | valid and existing wiki page-name
        |= comment     | comment as wiki text

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        commentor = c.authuser
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('WIKICOMMENT_CREATE')))
        (rc, wcmt, failmsg) = xicomp.comment_wiki(unicode(projectname), wikiurl, unicode(comment), commentor)
        return res or _result(rc, failmsg=failmsg)

    def tagwiki(self, projectname, pagename, addtags, deltags):
        """
        === tagwiki( projectname, pagename, addtags, deltags )
       
        :Description ::
            Add or delete tags from wiki-page `pagename`, under project
            `projectname`.

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | valid and existing wiki page-name
        |= addtags     | list of tagnames to add, if False, will be skipped
        |= deltags     | list of tagnames to delete, if False, will be skipped

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('WIKI_CREATE')))
        (addtags, deltags) = self._demarshalNone(addtags, deltags)
        addtags = addtags and [ unicode(t) for t in addtags ]
        deltags = deltags and [ unicode(t) for t in deltags ]
        (rc, wiki, failmsg) = xicomp.wiki_tags(unicode(projectname), wikiurl, addtags, deltags)
        return res or _result(rc, failmsg=failmsg)

    def votewiki(self, projectname, pagename, vote):
        """
        === votewiki( projectname, pagename, vote )
        
        :Description ::
            Upvote or Downvote wiki-page `pagename`, under project `projectname`

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | valid and existing wiki page-name
        |= vote        | either 'up' (up-vote page) or 'down' (down-vote page)

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus'  : 'fail',
                  'message' : <msg string indicating reason for failure>
                } >]
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        res = self._permissions(c.authuser, True)
        (rc, wiki, failmsg) = xicomp.wiki_vote(unicode(projectname), wikiurl, unicode(vote), c.authuser)
        return res or _result(rc, failmsg=failmsg)

    def wikifav(self, projectname, pagename, favorite):
        """
        === wikifav( projectname, pagename, favorite )

        :Description ::
            Add or remove wiki-page as favorite from `user`

        Positional arguments,
        |= projectname | a valid project-name
        |= pagename    | valid and existing wiki page-name
        |= favorite    | True (to add as favorite) or False (to remove from favorite)

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus'  : 'fail',
                  'message' : <msg string indicating reason for failure>
                } >]
        """
        wikiurl = unicode(h.url_forwiki(projectname, self._stripurl(pagename)))
        res = self._permissions(c.authuser, True)
        (rc, wiki, failmsg) = xicomp.wiki_fav(unicode(projectname), wikiurl, favorite, c.authuser)
        return res or _result(rc, failmsg=failmsg)

    def listtickets(self, projectname):
        """
        === listtickets( projectname )
        
        :Description ::
            List all tickets under project `projectname`,

        Positional arguments,
        |= projectname | a valid project-name

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus' : 'ok',
                  'tickets' : { <ticket-id> : [ <summary> ], ... }
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('TICKET_VIEW')))
        (rc, d, failmsg) = xicomp.list_ticket(unicode(projectname))
        return res or _result(rc, d=d, failmsg=failmsg)

    def newticket(self, projectname, summary, type, severity, description, components, milestones, versions, blocking, blockedby, parent):
        """
        === newticket( projectname, summary, type, severity, description,
        compenents, milestones, versions, blocking, blockedby, parent )
        
        :Description ::
            Create new ticket under project `projectname`

        Positional arguments,
        |= projectname | a valid project-name
        |= summary     | must be a valid summary string
        |= type        | must be a valid ticket type
        |= severity    | must be a valid ticket severity
        |= description | description string, if False, will be skipped
        |= components  | list of component ids, if False, will be skipped
        |= milestones  | list of milestone ids, if False, will be skipped
        |= versions    | list of version ids, if False, will be skipped
        |= blocking    | list of ticket ids blockedby this ticket, if False, will be skipped
        |= blockedby   | list of ticket ids blocking this ticket, if False, will be skipped
        |= parent      | parent ticket id

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus' : 'ok',
                  'id'        : <id>
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('TICKET_CREATE')))
        projectname = unicode(projectname)
        summary = unicode(summary)
        type = unicode(type)
        severity = unicode(severity)
        (description, components, milestones, versions, blocking, blockedby, parent) = self._demarshalNone(description, components, milestones, versions, blocking, blockedby, parent)
        (rc, d, failmsg) = xicomp.create_ticket(projectname, summary, type, severity, c.authuser, description=description, components=components, milestones=milestones, versions=versions, blocking=blocking, blockedby=blockedby, parent=parent)
        return res or _result(rc, d=d, failmsg=failmsg)

    def ticket(self, projectname, ticket):
        """
        === ticket( projectname, ticket )
        
        :Description ::
            Read ticket `ticket, under project `projectname`

        Positional arguments,
        |= projectname | a valid project-name
        |= ticket      | a valid ticket id

        :Return ::
            On success,
                [<PRE
                { 'rpcstatus'    : 'ok',
                  'id'        : <id>,
                  'summary'   : <summary string>,
                  'type'      : <type string>,
                  'severity'  : <severity string>,
                  'status'    : <status string>,
                  'due_date'  : <due_date in DD/MM/YYYY format>
                  'created_on': <created_in DD/MM/YYYY format>
                  'owner'     : <owner string>,
                  'promptuser': <promptuser string>,
                  'compid'    : <component-id>,
                  'compname'  : <componentname>,
                  'mstnid'    : <milestone-id>,
                  'mstnname'  : <milestone_name>,
                  'verid'     : <version-id>,
                  'vername'   : <version_name>,
                  'parent'    : <parent-ticketid>,
                  'description'      : <description string>,
                  'descriptionhtml'  : <description as html>,
                  'blockedby' : [ <ticket-id>, <ticket-id>, ... ],
                  'blocking'  : [ <ticket-id>, <ticket-id>, ... ],
                  'children'  : [ <ticket-id>, <ticket-id>, ... ]
                } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                }
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('TICKET_VIEW')))
        if not res:
            (rc, d, failmsg) = xicomp.read_ticket(unicode(projectname), ticket)
            if d:
                due_date = d.get('due_date', None)
                created_on = d.get('created_on', None)
                if due_date:
                    due_date = h.utc_2_usertz(due_date, c.authuser.timezone).strftime('%d/%m/%Y')
                if created_on:
                    created_on = h.utc_2_usertz(created_on, c.authuser.timezone).strftime('%d/%m/%Y')
                d['due_date'] = due_date
                d['created_on'] = created_on
            for k in d:
                d[k] = self._marshalNone(d[k])

        return res or _result(rc, d=d, failmsg=failmsg)

    def configticket(self, projectname, ticket, summary, type, severity, description, promptuser, components, milestones, versions, blocking, blockedby, parent, status, due_date):
        """
        === configticket( projectname, ticket, summary, type, severity,
        description, promptuser, components, versions, blocking, blockedby,
        parent, status, due_date )
        
        :Description ::
            Configure ticket, `ticket` under project, `projectname`

        Positional arguments,
        |= projectname | a valid project-name
        |= ticket      | a valid ticket id
        |= summary     | summary string, if False, will be skipped
        |= type        | valid ticket type, if False, will be skipped
        |= severity    | valid ticket severity, if False, will be skipped
        |= description | description string, if False, will be skipped
        |= components  | list of component ids, if False, will be skipped
        |= milestones  | list of milestone ids, if False, will be skipped
        |= versions    | list of version ids, if False, will be skipped
        |= blocking    | list of ticket ids blockedby this ticket, if False, will be skipped
        |= blockedby   | list of ticket ids blocking this ticket, if False, will be skipped
        |= parent      | parent ticket id
        |= status      | valid ticket status, if False, will be skipped
        |= due_date    | due_date in mm/dd/yyyy format

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('TICKET_CREATE')))
        if due_date and isinstance(due_date, (str, unicode)):
            due_date = h.duedate2dt(due_date, c.authuser.timezone)
        (summary, type, severity, description, promptuser, components, milestones, versions, blocking, blockedby, parent, status, due_date) = self._demarshalNone(summary, type, severity, description, promptuser, components, milestones, versions, blocking, blockedby, parent, status, due_date)
        (rc, t, failmsg) = xicomp.config_ticket(projectname, ticket, c.authuser, summary=summary, type=type, severity=severity, description=description, promptuser=promptuser, components=components, milestones=milestones, versions=versions, blocking=blocking, blockedby=blockedby, parent=parent, status=status, due_date=due_date)
        return res or _result(rc, failmsg=failmsg)

    def commentonticket(self, projectname, ticket, comment):
        """
        === commentonticket( projectname, ticket, comment )
        
        :Description ::
            Comment on `ticket` under project `projectname`

        Positional arguments,
        |= projectname | a valid project-name
        |= ticket      | a valid ticket id
        |= comment     | comment as wiki text

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        commentor = c.authuser
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('TICKET_COMMENT_CREATE')))
        (rc, tcmt, failmsg) = xicomp.comment_ticket(unicode(projectname), int(ticket), unicode(comment), commentor)
        return res or _result(rc, failmsg=failmsg)

    def tagticket(self, projectname, ticket, addtags, deltags):
        """
        === tagticket( projectname, ticket, addtags, deltags )
        
        :Description ::
            Add or delete tags from `ticket`,

        Positional arguments,
        |= projectname | a valid project-name
        |= ticket      | a valid ticket id
        |= addtags     | list of tagnames to add, if False, will be skipped
        |= deltags     | list of tagnames to delete, if False, will be skipped

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, h.authorized(h.HasPermname('TICKET_CREATE')))
        (addtags, deltags) = self._demarshalNone(addtags, deltags)
        addtags = addtags and [ unicode(t) for t in addtags ]
        deltags = deltags and [ unicode(t) for t in deltags ]
        (rc, t, failmsg) = xicomp.ticket_tags(unicode(projectname), ticket, addtags, deltags)
        return res or _result(rc, failmsg=failmsg)

    def voteticket(self, projectname, ticket, vote):
        """
        === voteticket( projectname, ticket, vote )
        
        :Description ::
            Upvote or Downvote a `ticket`

        Positional arguments,
        |= projectname | a valid project-name
        |= ticket      | a valid ticket id
        |= vote        | either 'up' (up-vote ticket) or 'down' (down-vote ticket)

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, True)
        (rc, t, failmsg) = xicomp.ticket_vote(unicode(projectname), ticket, unicode(vote), c.authuser)
        return res or _result(rc, failmsg=failmsg)

    def ticketfav(self, projectname, ticket, favorite):
        """
        === ticketfav( projectname, ticket, favorite )
        
        :Description :: 
            Add or remove ticket as favorite,

        :Return ::
            On success,
                [<PRE { 'rpcstatus'  : 'ok' } >]
            On failure,
                [<PRE
                { 'rpcstatus' : 'fail',
                  'message'   : <msg string indicating reason for failure>
                } >]
        """
        res = self._permissions(c.authuser, True)
        (rc, t, failmsg) = xicomp.ticket_fav(unicode(projectname), ticket, favorite, c.authuser)
        return res or _result(rc, failmsg=failmsg)

    def xmlrpc_fault(code, message):
        """Convenience method to return a Pylons response XMLRPC Fault"""
        print message

    def __after__(self):
        pass