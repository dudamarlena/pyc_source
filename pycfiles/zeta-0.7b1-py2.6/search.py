# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/controllers/search.py
# Compiled at: 2010-04-18 07:01:31
"""Controller module to manage site search."""
from __future__ import with_statement
import logging, os, xapian as xap
from pylons import request, response
from pylons import config
from pylons import session
from pylons import tmpl_context as c
from pylons.controllers.util import abort
from authkit.permissions import no_authkit_users_in_environ
from zeta.ccore import Component
from zeta.config.routing import r_searchpage, r_home
from zeta.model import meta
from zeta.lib.error import *
from zeta.lib.base import BaseController, render
from zeta.lib.constants import *
from zeta.lib.view import viewcontext
import zeta.lib.helpers as h
from zeta.lib.error import ZetaFormError
from zeta.config.environment import beforecontrollers, aftercontrollers
from zeta.comp.xsearch import XSearchComponent
from zeta.comp.attach import AttachComponent
from zeta.comp.license import LicenseComponent
from zeta.comp.system import SystemComponent
from zeta.comp.project import ProjectComponent
from zeta.comp.ticket import TicketComponent
from zeta.comp.review import ReviewComponent
from zeta.comp.wiki import WikiComponent
log = logging.getLogger(__name__)
ITEMSINPAGE = 10
compmgr = None
srchcomp = None
attcomp = None
liccomp = None
syscomp = None
projcomp = None
tckcomp = None
revcomp = None
wikicomp = None

def do_onetime():
    global attcomp
    global compmgr
    global liccomp
    global projcomp
    global revcomp
    global srchcomp
    global syscomp
    global tckcomp
    global wikicomp
    if compmgr == None:
        compmgr = config['compmgr']
        srchcomp = XSearchComponent(compmgr)
        attcomp = AttachComponent(compmgr)
        liccomp = LicenseComponent(compmgr)
        syscomp = SystemComponent(compmgr)
        projcomp = ProjectComponent(compmgr)
        tckcomp = TicketComponent(compmgr)
        revcomp = ReviewComponent(compmgr)
        wikicomp = WikiComponent(compmgr)
    return


def sr_userurl(id):
    userscomp = config['userscomp']
    user = userscomp.get_user(id)
    return h.url_foruser(user.username)


def sr_attachurl(id):
    attach = attcomp.get_attach(id)
    return h.url_forattach(attach.id)


def sr_licenseurl(id):
    license = liccomp.get_license(id)
    return h.url_forlicense(id)


def sr_swikiurl(path):
    swiki = syscomp.get_staticwiki(unicode(path))
    return h.url_forswiki(path)


def sr_projecturl(id):
    project = projcomp.get_project(id)
    return h.url_forproject(project.projectname)


def sr_ticketurl(projectname, id):
    ticket = tckcomp.get_ticket(id)
    return h.url_forticket(projectname, ticket.id)


def sr_reviewurl(projectname, id):
    review = revcomp.get_review(id)
    return h.url_forreview(projectname, review.id)


def sr_wikiurl(projectname, id):
    wiki = wikicomp.get_wiki(id)
    return wiki.wikiurl


urlconstructor = {'user': sr_userurl, 
   'attach': sr_attachurl, 
   'license': sr_licenseurl, 
   'staticwiki': sr_swikiurl, 
   'project': sr_projecturl, 
   'ticket': sr_ticketurl, 
   'review': sr_reviewurl, 
   'wiki': sr_wikiurl}

class SearchController(BaseController):
    """Controller for faceted search using Xapian"""

    def __before__(self, environ):
        beforecontrollers(environ=environ)
        do_onetime()
        c.querystring = request.params.get('querystring', '')
        c.frommatch = int(request.params.get('frommatch', 0))
        c.all = request.params.get('all', '')
        projectface = request.params.get('project', '')
        if projectface:
            c.allfaces = srchcomp.projectfaces.copy()
        else:
            c.allfaces = srchcomp.searchfaces.copy()

        def filterfaces(attr):
            val = request.params.get(attr, None)
            return val and (attr, val) or ('', '')

        c.faces = dict(map(filterfaces, c.allfaces.keys()))
        c.faces.pop('', None)
        if not c.faces or c.all:
            c.faces = {'all': '1'}
            projectface and c.faces.update([('project', projectface)])
        return

    @h.authorize(h.HasPermname('SEARCH_VIEW'))
    def index(self, environ):
        """Search"""
        viewcontext()
        q = c.querystring
        prefixes = []
        for face in c.faces.keys():
            if face == 'all':
                break
            elif face == 'project':
                prefixes.append((xap.Query.OP_AND, 'XPROJECT%s' % c.faces['project'].lower()))
            elif face:
                prefixes.append((xap.Query.OP_OR, 'XCLASS%s' % face))

        matches = srchcomp.query(q, prefixes, c.frommatch)
        c.matches = []
        c.total = c.frommatch + len(matches)
        rem = True
        count = 0
        for m in matches:
            if count >= ITEMSINPAGE:
                break
            count += 1
            (text, url) = srchcomp.urlfor_match(m, urlconstructor)
            c.matches.append({'percent': m.percent, 
               'rank': m.rank, 
               'weight': m.weight, 
               'data': m.document.get_data(), 
               'url': url, 
               'text': text})
        else:
            rem = False

        kwargs = {}
        kwargs.update(c.faces)
        c.querystring and kwargs.update({'querystring': c.querystring})
        h.suburl_search = h.url_for(h.r_searchpage, **kwargs)
        h.suburl_searchprev = c.frommatch and h.url_for(h.r_searchpage, frommatch=(c.frommatch - ITEMSINPAGE), **kwargs) or ''
        h.suburl_searchnext = rem and h.url_for(h.r_searchpage, frommatch=(c.frommatch + ITEMSINPAGE), **kwargs) or ''
        c.terms = srchcomp.queryterms(q)
        c.title = 'Search'
        c.allfaces.pop('project')
        return render('/derived/search/searchpage.html')

    def __after__(self):
        aftercontrollers()