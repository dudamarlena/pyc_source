# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/view.py
# Compiled at: 2010-07-15 08:52:37
"""Module contains the library functions, classes required to build and
data crunch view objects, that can be used in the templates.
"""
from os.path import isfile
from pylons import request, response
from pylons import config
from pylons import tmpl_context as c
from pylons.controllers.util import abort
from zeta.config.routing import *
from zeta.config.environment import zetaversion, zetacreators, beforecontrollers
from zeta.lib.base import render
from zeta.lib.constants import LEN_NAME
import zeta.lib.helpers as h

class View(object):
    """Base class for all view object"""
    pass


anchor_types = [
 'link', 'pointer']

class Anchor(View):
    """Defines an anchor elements data"""

    def __init__(self, href=None, type='link', text=None, title=None, **kwargs):
        """Instantiate an anchor object with the following fields,
        href     url
        type     type of anchor, either `link` or `pointer`
        text     text to be displayed to user
        title    mouse-over help text.
        **kwargs additional parameters that will be added to the object
        """
        self.href = href
        self.text = text
        self.title = title
        self.type = type
        [ self.__dict__.setdefault(k, kwargs[k]) for k in kwargs ]


def _defaultcontext():
    c.title = config['zeta.sitename']
    c.sitename = config['zeta.sitename']
    c.siteadmin = config['zeta.siteadmin']
    c.welcomestring = c.sysentries.get('welcomestring', '')
    h.url_site = '/'
    c.zetalink = 'http://discoverzeta.com'
    c.zetalogo = config['zeta.zetalogo']
    c.zetaversion = zetaversion
    c.zetacreators = zetacreators


def usertype():
    if h.authorized(h.ValidUser(strict='True')):
        type = c.authusername
    elif h.authorized(h.SiteAdmin()):
        type = 'siteadmin'
    else:
        type = 'anonyuser'
    return type


def make_metanavs():
    """Find the nature of user accessing the page and compose the Anchor
    arrays. And cache them"""
    h.url_createprj = h.url_for(h.r_projcreate, form='request', formname='createprj')
    h.url_projindex = h.url_for(h.r_projects)
    h.projectlinks = [ [p, h.url_forproject(p)] for p in c.myprojects ]
    h.url_usershome = h.url_for(h.r_usershome)
    h.url_inviteuser = h.url_for(h.r_usersinvite)
    h.url_mytickets = h.url_for(h.r_usertickets, username=c.authusername)
    h.quicklinks = [
     [
      'users', h.url_usershome],
     [
      'invite', h.url_inviteuser],
     [
      'mytickets', h.url_mytickets]]
    if c.authorized:
        h.quicklinks.append([
         'mypage', h.url_for(h.r_userhome, username=c.authusername)])
    metanavs = []
    if h.authorized(h.ValidUser(strict='True')):
        metanavs.append(Anchor(href=None, type='pointer', text='quick-links', title='Quick shortcut to useful links'))
        metanavs.extend([
         Anchor(href=None, type='pointer', text='myprojects', title='Goto projects'),
         Anchor(href=h.url_for(r_userpref, username=c.authusername, form='request'), text='preference', title='Your account preference'),
         Anchor(href=h.url_for(r_accounts, action='signout'), text='signout', title='Sign out')])
    else:
        metanavs.extend([
         Anchor(href=h.url_for(r_accounts, action='signin'), text='signin', title='Sign in if already registered'),
         Anchor(href=h.url_for(r_accounts, action='newaccount', form='request', formname='createuser'), text='register', title='New User ? Sign up')])
    if h.authorized(h.HasPermname('SITE_ADMIN')):
        metanavs.extend([
         Anchor(href=h.url_for(r_siteadmin, form='request'), text='site-admin', title='Site level administration')])
    metanavs.extend([
     Anchor(href=h.url_for(r_staticwiki, url='aboutus'), text='aboutus', title='About Us'),
     Anchor(href=h.url_for(r_staticwiki, url='help/'), text='help', title='Learn how to use ' + config['zeta.sitename'])])
    return metanavs


def make_mainnavs(projname, activetab=0):
    """Generate the mainnavigation panel for project, `projname`,
    with the active tab for the panel specifying by the offset activetab.

    Freshly constructed 'mainnavs' array of anchor objects, for a specific
    project can be cached harmlessly.
    """
    mainnavs = []
    mainnavs.extend([
     Anchor(href=h.url_for(r_projecthome, projectname=projname), text=projname, title=projname + 'Project home', tab='inactive'),
     Anchor(href=h.url_for(r_projwikis, projectname=projname), text='Wiki', title='Wiki Pages for ' + projname, tab='inactive'),
     Anchor(href=h.url_for(r_projtickets, projectname=projname), text='Tickets', title='Open Tickets and issues for ' + projname, tab='inactive'),
     Anchor(href=h.url_for(r_projvcs, projectname=projname), text='Source', title='Browse Source code for ' + projname, tab='inactive'),
     Anchor(href=h.url_for(r_projrevw, projectname=projname), text='Review', title='Manage project reviews ' + projname, tab='inactive')])
    if h.authorized(h.SiteAdmin()) or h.authorized(h.ProjectAdmin()):
        mainnavs.append(Anchor(href=h.url_for(r_projadmin, projectname=projname, form='request'), text='Admin', title='Adminstration for ' + projname, tab='inactive'))
    [ setattr(mainnavs[i], 'tab', 'inactive') for i in range(len(mainnavs)) ]
    mainnavs[activetab].tab = 'active'
    return mainnavs


def viewcontext(**kwargs):
    _defaultcontext()
    c.metanavs = make_metanavs()
    h.suburl_searchzeta = h.url_for(h.r_searchpage)


def viewuserpanes(**kwargs):
    """Compose the elements for userpanes"""
    if c.authuser and c.authuser.userinfo.userpanes == 'siteuserpanes':
        c.userpanes = list(h.parse_csv(c.sysentries.get('userpanes')))
    elif not c.authorized:
        c.userpanes = []
    else:
        c.userpanes = h.parse_csv(c.authuser.userinfo.userpanes)


def viewprojectpanel(projectname, activetab=0):
    c.mainnavs = make_mainnavs(projectname, activetab)


def render_signin():
    """This function will be called by AuthKit for user signin page"""
    beforecontrollers()
    viewcontext()
    h.url_forgotpass = h.url_for(h.r_accounts, action='forgotpass', form='request', formname='forgotpass')
    c.skipga = True
    claimeduser = request.POST.get('username', None)
    if claimeduser and getattr(c, 'signinflash', '') == '':
        c.signinflash = 'Enter a correct username,  password'
    userscomp = h.fromconfig('userscomp')
    claimeduser = claimeduser and userscomp.get_user(claimeduser)
    if claimeduser and claimeduser.disabled:
        c.signinflash = 'User disabled, contact site-administrator'
    html = render('/derived/accounts/signin.html').encode('utf-8')
    return html