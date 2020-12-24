# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/helpers.py
# Compiled at: 2010-07-15 06:23:04
"""Helper functionsn,
Consists of functions to be used across the entire application, including
templates. This module is available as 'h'.

Import helpers as desired, or define your own, ie:
    from webhelpers.html.tags import checkbox, password
"""
import logging
from random import randint, choice
import os
from os.path import commonprefix, join
import sys, re, shutil
from difflib import SequenceMatcher
import datetime as dt
from urlparse import urlparse
from tempfile import mkstemp
import tempita, copy
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_for_filename, get_lexer_by_name
import pytz
from pytz import timezone
import simplejson as json
from routes import url_for
from pylons import request, response, session, tmpl_context as c
from pylons import config
from pylons import session
from pylons.controllers.util import redirect
from skimpyGimpy.skimpyAPI import Png
from pytz import all_timezones
from webhelpers.pylonslib import Flash as _Flash
from authkit.authorize.pylons_adaptors import authorize, authorized
from authkit.authorize import PermissionError, PermissionSetupError, NotAuthenticatedError, NotAuthorizedError
from webhelpers.feedgenerator import Rss201rev2Feed as FeedGen
from zwiki.zetawiki import parse_link
from zwiki.zwparser import ZWParser
from zeta.lib.constants import *
from zeta.lib.error import ZetaFormError
from zeta.lib.datefmt import *
from zeta.config.routing import *
from zeta.auth.perm import UserIn, ValidUser, HasPermname, SiteAdmin, ProjectAdmin

class Preview(object):
    pass


class ZetaWiki(object):
    """Zeta app object for zwiki"""

    def __init__(self):
        self.name = 'zeta'
        self.h = sys.modules['zeta.lib.helpers']
        self.c = c

    def _zcomp(self, name):
        from zeta.comp.attach import AttachComponent
        from zeta.comp.tag import TagComponent
        from zeta.comp.license import LicenseComponent
        from zeta.comp.project import ProjectComponent
        from zeta.comp.ticket import TicketComponent
        from zeta.comp.vcs import VcsComponent
        from zeta.comp.review import ReviewComponent
        compmgr = fromconfig('compmgr')
        comps = {'user': fromconfig('userscomp'), 
           'attachment': AttachComponent(compmgr), 
           'tag': TagComponent(compmgr), 
           'license': LicenseComponent(compmgr), 
           'project': ProjectComponent(compmgr), 
           'ticket': TicketComponent(compmgr), 
           'vcs': VcsComponent(compmgr), 
           'review': ReviewComponent(compmgr)}
        return comps[name]

    usercomp = property(lambda self: self._zcomp('user'))
    attcomp = property(lambda self: self._zcomp('attachment'))
    tagcomp = property(lambda self: self._zcomp('tag'))
    liccomp = property(lambda self: self._zcomp('license'))
    projcomp = property(lambda self: self._zcomp('project'))
    tckcomp = property(lambda self: self._zcomp('ticket'))
    vcscomp = property(lambda self: self._zcomp('vcs'))
    revcomp = property(lambda self: self._zcomp('review'))


log = logging.getLogger(__name__)
flash = _Flash()
zw_logparser = None

def custom_utcnow():
    import datetime
    nextdt = datetime.datetime(2005, 1, 1, 0, 0, 0, 0, timezone('UTC'))
    while 1:
        yield nextdt
        maxsec = int(fromconfig('maxsec', 1800))
        nextdt = nextdt + datetime.timedelta(0, randint(0, maxsec))


utc_generator = custom_utcnow()
utcnow = lambda : utc_generator.next()
utcnow = lambda : timezone('UTC').localize(dt.datetime.utcnow())

def redirect_to(*args, **kwargs):
    return redirect(url_for(*args, **kwargs))


def fromconfig(key, default=None):
    """Since `pylons.config` is initialized as late as possible, not able to
    figure out a way to get the config details. For now use
    `pylons.test.pylonsapp.config`"""
    val = config.get(key, default)
    if val == None:
        import zeta.config.environment as environment
        if environment.websetupconfig:
            val = environment.websetupconfig.get(key, default)
    if val == None:
        import pylons.test
        val = pylons.test.pylonsapp.config.get(key, default)
    return val


url_foruserreg = lambda dgst: url_for(r_accounts, action='newaccount', digest=dgst, form='request', formname='createuser')
url_forresetp = lambda d, e: url_for(r_accounts, action='resetpass', digest=d, form='request', formname='resetpass', emailid=e)
url_foruser = lambda u: url_for(r_userhome, username=u)
url_forusericon = lambda u: url_for(r_attachment, id=u.iconfile and u.iconfile.id or '')
url_fortag = lambda t: url_for(r_tag, tagname=t)
url_forattach = lambda id: url_for(r_attachment, id=id)
url_forlicense = lambda id: url_for(r_licenseid, id=id)
url_forproject = lambda p: url_for(r_projecthome, projectname=p)
url_formstn = lambda p, id: url_for(r_projmstn, projectname=p, id=id)
url_forticket = lambda p, id: url_for(r_projticketid, projectname=p, id=id)
url_forvcs = lambda p, id: url_for(r_projvcsbrowse, projectname=p, id=id)
url_forreview = lambda p, id: url_for(r_projrevwid, projectname=p, id=id)
url_forrset = lambda p, id: url_for(r_projrevwset, projectname=p, id=id)
url_forwiki = lambda p, u: url_for(r_projwiki, projectname=p, url=u)
url_forswiki = lambda path: url_for(r_staticwiki, url=path)
url_fortcklist = lambda p, **kw: url_for(r_projtickets, projectname=p, **kw)
url_forutcklist = lambda u, **kw: url_for(r_usertickets, username=u, **kw)
url_formount = lambda p, id, u: url_for(r_projmount, projectname=p, id=id, murl=u)
url_forchmount = lambda p, id: url_for(r_projmounts, projectname=p, changeid=id)
scoopvalues = lambda objects, attribute: filter(None, [ getattr(o, attribute, None) for o in objects
             ])
filter_badargs = lambda item: not bool(item)
randomname = lambda len=8, chars='ABCDEGHKLMNOPRSTUVWXYZ1234567890': ('').join(choice(chars) for i in range(len))
str2bool = lambda s: s in ('True', 'true')

def captchafile():
    """Generate a captcha file and place it under /public/captcha/<captchafile>.png.
    where, the <captchafile> is generated as "captcha" + 12 random characters.

    Along with the file, a captcha word is randomly generated and,
    returned as
      ( '12 letter captcha value', '4 letter captcha word', captcha image file )
    """
    redo = True
    while redo:
        value = randomname(len=12)
        word = randomname(len=4)
        imgsrc = os.path.join('captcha', 'captcha_' + word + '_' + value + '.png')
        file = os.path.join(fromconfig('zeta.envpath'), 'public', imgsrc)
        if not os.path.isfile(file):
            generator = Png(word)
            result = generator.data(file)
            redo = False

    session['captchafile'] = file
    session['captchaword'] = word
    session.save()
    return (value, word, os.path.join('/', imgsrc))


def validate_captcha(word):
    """Validate whether the user entered captcha word matches the word userd
    for generating captcha."""
    rcmsg = ''
    if session.has_key('captchafile'):
        file = session['captchafile']
        os.remove(file)
        del session['captchafile']
        session.save()
        if session.has_key('captchaword'):
            sessword = session['captchaword']
            del session['captchaword']
            session.save()
            if sessword != word:
                rcmsg = 'Captcha Word does not match'
        else:
            rcmsg = 'Captcha Word not present in the session'
    else:
        rcmsg = 'Captcha file not in session'
    return rcmsg


def validate_fields(request):
    """Form field validation for Form Components
        `request` must contain a `POST` attribute which contains the fields as
        dictionary """
    timezone = request.POST.get('timezone', None)
    if timezone and timezone not in all_timezones:
        raise ZetaFormError('Unknown timezone')
    fields = [
     (
      1, LEN_NAME,
      [
       'perm_name', 'perm_group', 'userrel_type', 'username',
       'team_type', 'projectname', 'componentname', 'milestone_name',
       'version_name', 'tck_statusname', 'tck_typename',
       'tck_severityname', 'actionname', 'wiki_typename', 'author',
       'votedas', 'medium']),
     (
      0, LEN_256, ['userpanes']),
     (
      4, LEN_EMAILID,
      [
       'emailid', 'admin_email', 'mailing_list', 'ircchannel']),
     (
      1, LEN_TAGNAME, ['tagname']),
     (
      1, LEN_SUMMARY, ['summary']),
     (
      1, LEN_RESOURCEURL, ['filename', 'resource_url', 'wikiurl']),
     (
      1, LEN_LICENSENAME, ['licensename']),
     (
      1, LEN_DESCRIBE, ['text', 'description', 'closing_remark']),
     (
      1, LEN_LICENSESOURCE, ['source']),
     (
      3, LEN_1K, ['log'])]
    for (min, max, names) in fields:
        for name in names:
            values = request.POST.getall(name)
            invalids = [ value for value in values if value if not min <= len(value) <= max
                       ]
            if invalids:
                raise ZetaFormError('field `%s` is either too short or too long' % name)
            if values:
                if name == 'username' and not re.match(RE_UNAME, values[0]):
                    raise ZetaFormError("'username' must contain only alphanumeric " + "and underscore characters'")
                elif name == 'projectname' and not re.match(RE_PNAME, values[0]):
                    raise ZetaFormError("'projectname' must contain only alphanumeric, " + "underscore and '.' characters'")
                elif name == 'tagname' and not re.match(RE_TNAME, values[0]):
                    raise ZetaFormError("'tagname' must contain only alphanumeric, " + "underscore, '.' and '!' characters'")

    return


def todojoreadstore(items, handler, id='', label=''):
    """Takes `list` or `dict` as `items` parameter,
        - iterates on each value or (key, value) pair
        - passes the value or (key, value) pair to the handler
        - Expects a `dict` object as output.
        - makes a list out of all the returned dict object and 
          Returns."""
    r = []
    if isinstance(items, list):
        r = filter(None, map(handler, items))
    elif isinstance(items, dict):
        r = filter(None, map(handler, items.keys(), items.values()))
    json_py = {}
    json_py.setdefault('items', r)
    id and json_py.setdefault('identifier', id)
    label and json_py.setdefault('label', label)
    return json.dumps(json_py)


def myprojects(authuser):
    """For the authenticated user, return the list of projects the user is
    associated"""
    from zeta.comp.project import ProjectComponent
    userscomp = fromconfig('userscomp')
    compmgr = fromconfig('compmgr')
    projcomp = ProjectComponent(compmgr)
    if authuser and authuser.username == 'admin':
        myprojects = sorted(projcomp.projectnames)
    elif authuser:
        myprojects = sorted(userscomp.projectnames(authuser.username))
    else:
        myprojects = []
    return myprojects


def nestedreplies(cmt, comments):
    """Recursive function to assemble the comments in threaded mode. This
    decides whether the comment is depth first mode or breadth first mode"""
    for rcmt in cmt.replies:
        comments.append(rcmt)
        nestedreplies(rcmt, comments)

    return comments


def hitch(obj, cls, function, *args, **kwargs):
    """Hitch a function with a different object and different set of
    arguments."""

    def fnhitched(self, *a, **kw):
        kwargs.update(kw)
        return function(self, *(args + a), **kwargs)

    return fnhitched.__get__(obj, cls)


def parse_csv(line):
    """Parse a line of comma seperated values, discarding duplicate values and
    empty values, while stripping away the leading and trailing white spaces
    for valid values"""
    vals = line and line.split(',') or []
    vals = filter(None, [ v.strip(' \t') for v in vals ])
    return vals


def url_for_mform(*args, **kwargs):
    """Generate urls requesting / submitting multiple forms,
    ( with multiple, formname=* query parameters )"""
    formurl = ''
    if 'formname' in kwargs:
        formname = kwargs.pop('formname')
        formurl = url_for(*args, **kwargs)
        formurl += '&' + ('&').join([ 'formname=' + fn for fn in formname ])
    return formurl


def wiki_parseurl(wikiurl):
    routes_map = fromconfig('routes.map')
    (d, robj) = routes_map.routematch(wikiurl)
    return d.get('url', '')


def wiki_parseurls(wikiurls):
    """`wikiurls` is a list-of-url (containing the path info part) for wiki
    pages. Parse them and extract the WikiPageName"""
    routes_map = fromconfig('routes.map')
    if isinstance(wikiurls, list):
        return filter(None, [ wiki_parseurl(wikiurl) for wikiurl in wikiurls ])
    else:
        if isinstance(wikiurls, (str, unicode)):
            return wiki_parseurl(wikiurls)
        return


def url_forzetalink(c, **kwargs):
    """Based on the kwargs, generate the url,
    Note : It is a costly affair to fetch the entry from database and compute
    the url, so, we try to compute them from `kwargs` as much as possible.
    Refer `timeline`"""
    from zeta.comp.attach import AttachComponent
    from zeta.comp.tag import TagComponent
    from zeta.comp.license import LicenseComponent
    from zeta.comp.project import ProjectComponent
    from zeta.comp.ticket import TicketComponent
    from zeta.comp.vcs import VcsComponent
    from zeta.comp.review import ReviewComponent
    compmgr = fromconfig('compmgr')
    userscomp = fromconfig('userscomp')
    tckreslv = fromconfig('zeta.ticketresolv')
    attcomp = AttachComponent(compmgr)
    tagcomp = TagComponent(compmgr)
    liccomp = LicenseComponent(compmgr)
    projcomp = ProjectComponent(compmgr)
    tckcomp = TicketComponent(compmgr)
    vcscomp = VcsComponent(compmgr)
    revcomp = ReviewComponent(compmgr)
    url = ''
    title = ''
    text = ''
    style = ''
    linkfor = kwargs.keys()
    if 'user' in linkfor:
        u = userscomp.get_user(kwargs['user'])
        if u:
            url = url_for(r_userhome, username=u.username)
            title = u.username
            text = u.username
    elif 'attachment' in linkfor:
        att = attcomp.get_attach(kwargs['attachment'])
        if att:
            url = url_for(r_attachdownl, id=att.id)
            title = att.filename
            text = att.filename
    elif 'tag' in linkfor:
        g = tagcomp.get_tag(kwargs['tag'])
        if g:
            url = url_for(r_tag, tagname=g.tagname)
            title = g.tagname
            text = g.tagname
    elif 'license' in linkfor:
        lic = liccomp.get_license(kwargs['license'])
        if lic:
            url = url_for(r_licenseid, id=lic.id)
            title = lic.licensename
            text = lic.licensename
    elif 'milestone' in linkfor:
        m = projcomp.get_milestone(kwargs['milestone'])
        if m:
            url = url_for(r_projmstn, projectname=m.project.projectname, id=m.id)
            title = m.milestone_name
            style = 'text-decoration : line-through;' if m.completed else 'color:red; text-decoration : line-through;' if (m.cancelled) else ''
            text = m.milestone_name
    elif 'ticket' in linkfor:
        t = tckcomp.get_ticket(kwargs['ticket'])
        if t:
            (_id, status) = tckcomp.currticketstatus(t)
            url = url_for(r_projticketid, projectname=t.project.projectname, id=t.id)
            title = t.summary
            style = 'text-decoration : line-through;' if status in tckreslv else ''
    elif 'source' in linkfor and 'revision' in linkfor:
        v = vcscomp.get_vcs(kwargs['source'])
        revno = kwargs['revision']
        if v:
            url = url_for(r_projvcsrev, projectname=v.project.projectname, id=v.id, revno=str(revno))
            title = '%s (revision %s)' % (v.name, revno)
            text = '%s:r%s' % (v.name, revno)
    elif 'source' in linkfor:
        v = vcscomp.get_vcs(kwargs['source'])
        if v:
            url = url_for(r_projvcsbrowse, projectname=v.project.projectname, id=v.id)
            title = v.name
            text = v.name
    elif 'wiki' in linkfor:
        page = kwargs['wiki']
        p = kwargs.get('project', None)
        p = p and projcomp.get_project(p)
        try:
            p = p or c and getattr(c, 'project', None) or None
        except:
            pass
        else:
            url = page if page[0] == '/' else url_forwiki(p.projectname, page) if p else page
            title = url
            text = page
    elif 'review' in linkfor:
        r = revcomp.get_review(kwargs['review'])
        if r:
            url = url_for(r_projrevwid, projectname=r.project.projectname, id=r.id)
            title = r.resource_url
            text = 'review%s' % r.id
    elif 'project' in linkfor:
        p = projcomp.get_project(kwargs['project'])
        if p:
            url = url_for(r_projecthome, projectname=p.projectname)
            title = p.projectname
            text = p.projectname
    return (
     url, text, title, style)


def translate(self, cacheattr='text', redirect=True, cache=False):
    """Translate the wiki in `cacheattr` into html"""
    envpath = fromconfig('zeta.envpath')
    htmlattr = cacheattr + 'html'
    self.zwparser = ZWParser(app=ZetaWiki(), lextab='lextab', yacctab='yacctab', outputdir=join(envpath, 'data'), yacc_optimize=True)
    self.tu = self.zwparser.parse(getattr(self, cacheattr))
    html = self.tu.tohtml()
    if cache == True or self.zwparser.dynamictext == False:
        setattr(self, htmlattr, html)
    return unicode(html)


def interzeta_map(name):
    """Retrieve the interzeta mapping for 'name'"""
    from zeta.comp.system import SystemComponent
    syscomp = SystemComponent(fromconfig('compmgr'))
    return syscomp.get_interzeta(name)


def autoreference(text, tagnames=[]):
    """In the passed text, search and identify valid tagnames and create
    reference for them"""
    from zeta.comp.tag import TagComponent
    compmgr = fromconfig('compmgr')
    tagcomp = TagComponent(compmgr)
    tagnames = tagnames or tagcomp.tagnames
    patt = '\\b(' + ('|').join(tagnames) + ')\\b'
    reps = ' [< <a href="/tag/\\1">\\1</a> >] '
    text = re.sub(patt, reps, text)
    return text


tmpl_content = '\n<blockquote class="fntsmall fggray" style="margin-top: 2px; margin-bottom: 3px;">\n    <pre>%s</pre>\n</blockquote>'

def log2html(logmsg):
    """Convert the log message into html"""
    global zw_logparser
    s = logmsg.split('::')
    desc = s.pop(0)
    reference = s.pop(0).strip()
    if not zw_logparser:
        zw_logparser = ZWParser(app=ZetaWiki(), lextab='lextab', yacctab='yacctab', outputdir=join(fromconfig('zeta.envpath'), 'data'))
    (href, title, text, _left) = parse_link(zw_logparser, reference)
    if href:
        item = '<a href="%s" title="%s">%s</a>' % (href, title, text)
    else:
        item = text
    summary = '<span class="logsumm" style="color: green">%s %s</span>' % (
     desc, item)
    cont = ('').join(s).strip(' \t')
    content = cont and tmpl_content % cont or ''
    return (
     summary, content)


re_text = re.compile('<a[^>]*>([^<]*)</a>')
re_href = re.compile('href="([^"]*)"')

def log2feed(log):
    """Convert the log message into html feed"""
    user = re_text.findall(log.userhtml)[0]
    itemsfound = re_text.findall(log.itemhtml)
    item = itemsfound and itemsfound[(-1)] or '-'
    summary = 'By %s, in, %s' % (user, item)
    linkfound = re_href.findall(log.itemhtml)
    link = linkfound and linkfound[(-1)] or '-'
    content = log.log
    return (summary, link, content)


def logfor(attributes):
    """Construct the log message based on attributes, which are of the
    form,
        [ ( name, old, new ),
          ...
        ]"""
    lines = []
    for (name, old, new) in attributes:
        if old == new:
            continue
        if name:
            lines.append('%s : %s' % (name, new))
        else:
            lines.append(new)

    return ('\n').join(lines)


def timeslice(logs):
    """Given the list of logs, slice them into groups based on day"""
    slices = {}
    now = dt.datetime.utcnow()
    [ slices.setdefault(log.created_on.strftime('%a, %b %d %Y'), []).append(log) for log in logs
    ]
    return slices


def tline_controller(c, routename, routeargs, assc_tables, fromoff, logid, dir, modelobj=None):
    from zeta.comp.timeline import TimelineComponent
    tlcomp = TimelineComponent(fromconfig('compmgr'))
    c.alllogs = tlcomp.fetchlogs(assc_tables, modelobj, limit=TLCOUNT + 2, id=logid, direction=dir)
    c.logs = c.alllogs[:100]
    c.links = ['', '', '']
    if fromoff > TLCOUNT:
        c.links[0] = url_for(routename, fromoff=1, **routeargs)
        c.links[1] = url_for(routename, logid=c.logs[0].id, dir='newer', fromoff=(fromoff - TLCOUNT), **routeargs)
    if len(c.alllogs) >= TLCOUNT:
        c.links[2] = url_for(routename, logid=c.logs[(-1)].id, dir='older', fromoff=(fromoff + TLCOUNT), **routeargs)
    c.fromoff = fromoff
    c.tooff = fromoff + len(c.logs)


def olderby(days):
    """Returns in human readable form of, how older days are"""
    weeks = days / 7.0
    months = days / 30.0
    years = days / 365.0
    if years > 3:
        show = '%.2f year%s' % (years, ['', 's'][bool(years - 1)])
    elif months > 6:
        show = '%.2f month%s' % (months, ['', 's'][bool(months - 1)])
    elif weeks > 15:
        show = '%.2f week%s' % (weeks, ['', 's'][bool(weeks - 1)])
    else:
        show = '%.2f day%s' % (days, ['', 's'][bool(days - 1)])
    return show


delimiters = ' \t.?:;='

def shortblock(text, offset, around=100):
    """Shorten the text around the offset"""
    l = len(text)
    begin = offset - around > 0 and offset - around or 0
    end = offset + around < l and offset + around or l
    text = text[begin:end]
    begins = filter(lambda x: x != -1, [ text.find(delim) for delim in delimiters ])
    begin = begins and min(begins) or 0
    ends = filter(lambda x: x != -1, [ text.rfind(delim) for delim in delimiters ])
    end = ends and max(ends) or -1
    return text[begin:end].strip(delimiters)


def localizeterms(text, terms):
    """Localize text around the terms"""
    text = text.lower()
    occurances = [ text.find(term) for term in terms ]
    firstblock = occurances and shortblock(text, min(occurances), around=100) or ''
    occurances = [ text.rfind(term) for term in terms if text.rfind(term) not in occurances
                 ]
    lastblock = occurances and shortblock(text, max(occurances), around=100) or ''
    firstblock = firstblock.replace('<', ' ').replace('>', ' ')
    lastblock = lastblock.replace('<', ' ').replace('>', ' ')
    for term in terms:
        firstblock = firstblock.replace(term, '<b>%s</b>' % term)
        lastblock = lastblock.replace(term, '<b>%s</b>' % term)

    text = firstblock + (firstblock and '...' or '') + lastblock + (lastblock and '...' or '')
    return text


re_xmlauth = re.compile('//([^:@]+:[^@]+)@.+')

def auth_xmlrpc(url):
    """Parse the url, extract the username and password (in hash digest) and
    authenticate.
    Use this function if the username and password is available as,
        http://username:password@..../....."""
    userscomp = fromconfig('userscomp')
    authinfo = re_xmlauth.findall(url)
    (user, password) = authinfo and authinfo[0].split(':') or (None, None)
    if not user:
        return
    else:
        user = userscomp.get_user(user)
        if user.password == password:
            return user
        return


class Html2Doc(object):
    """Translate the html content to a different document format"""

    def __init__(self, html, format='text'):
        self.html = html
        self.format = format
        (self.srcfd, self.srcfile) = mkstemp()
        (self.dstfd, self.dstfile) = mkstemp()
        open(self.srcfile, 'wb').write(html)

    def totext(self):
        os.system('html2text -o %s %s > /dev/null 2>&1' % (
         self.dstfile, self.srcfile))
        return open(self.dstfile, 'rb').read()

    def tops(self):
        os.system('htmldoc --webpage -t ps3 -f %s %s > /dev/null 2>&1' % (
         self.dstfile, self.srcfile))
        return open(self.dstfile, 'rb').read()

    def topdf(self):
        os.system('htmldoc --webpage -t pdf14 -f %s %s > /dev/null 2>&1' % (
         self.dstfile, self.srcfile))
        return open(self.dstfile, 'rb').read()

    def convert(self):
        if self.format == 'text':
            return self.totext()
        if self.format == 'ps':
            return self.tops()
        if self.format == 'pdf':
            return self.topdf()

    def __del__(self):
        os.remove(self.srcfile)
        os.remove(self.dstfile)


def useraddress(uinfo):
    """Convert the user address fields into a single string and return back
    the string"""
    fulladdress = (', ').join(filter(None, [ getattr(uinfo, attr, '') or '' for attr in [
     'addressline1', 'addressline2',
     'city', 'state', 'country']
                                           ]))
    return fulladdress


def user2canonical(user):
    """For `user` object, return a canonical string that is either composed of
    FirstName, MiddleName, LastName or if not preset, just username"""
    if isinstance(user, (str, unicode)):
        cname = user
    else:
        uinfo = user.userinfo
        if uinfo.firstname or uinfo.middlename or uinfo.lastname:
            cname = (' ').join([uinfo.firstname, uinfo.middlename, uinfo.lastname])
        else:
            cname = user.username
    return cname


def fullurl(host, script, path):
    """Construct full http url"""
    return 'http://%s%s%s' % (host, script, path)


def gmapkey(sysentries):
    """Get a valid key if present in system-entries"""
    key = c.sysentries.get('googlemaps', '')
    if key in ('False', 'false') or len(key) < 16:
        return ''
    else:
        return key


gcache_filters = None

def compile_tckfilters(tckfilters):
    """Compile ticket filters into JavaScript convinient way, `filters` should
    be a python object in the following format,

        [ ( <filtername>,

            # list of OR filters, where any of the AND filters should match.

            [ # list of AND filters, where every field should match its filter
              # criteria

              [ ( <field1>, <filter-string> ), 
                ( <field2>, <filter-string> ), 
                ...
              ],
            ],
            ...
          ),
          ...
        ]
    """
    global gcache_filters
    substitute = lambda tmpl: tmpl.substitute(_t_authusername=c.authusername)
    dotemplate = lambda term: '_t_' in term and substitute(tempita.Template(term)) or term
    if gcache_filters == None:
        gcache_filters = [ (filtername, [ [ (field, re.compile(dotemplate(term))) for (field, term) in andlist ] for andlist in orlist ]) for (filtername, orlist) in tckfilters
                         ]
    return gcache_filters


def checksuburl(url, baseurl):
    """Check wether `baseurl` looks like a parent for `url`, used for parsing static
    wiki urls """
    parts = url.split(baseurl, 1)
    if len(parts) == 1:
        rc = [
         False, '']
    elif parts[0] == '':
        rc = [
         True, url]
    else:
        rc = [
         False, '']
    return rc


def duedate2dt(due_date, tz='UTC'):
    """Convert `due_date` from string into Datetime object"""

    def _tryformat(tzone, due_date, format):
        """Try to convert the due_date with `format` string"""
        try:
            usertz = timezone(tzone)
            due_date = usertz_2_utc(dt.datetime.strptime(due_date, format), usertz)
            return due_date
        except:
            return False

    formats = ['%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y']
    for fmt in formats:
        dd = _tryformat(tz, due_date, fmt)
        if dd:
            due_date = dd
            break
    else:
        due_date = None

    return due_date


def tckcolorcode(tdet, tckccodes):
    """`tdet` is expected as a dictionary of,
            { tck_typename: type, tck_statusname: status,
              tck_severityname: severity }
    will be matched agains `tckccodes` to retrive the configured color code"""
    color = tckccodes[0][2]
    for rule in tckccodes[1:]:
        if tdet[rule[0]] == rule[1]:
            color = rule[2]
            break

    return color


def escape_htmlchars(text):
    """If the text is not supposed to have html characters, escape them"""
    text = re.compile('&', re.MULTILINE | re.UNICODE).sub('&amp;', text)
    text = re.compile('"', re.MULTILINE | re.UNICODE).sub('&quot;', text)
    text = re.compile('<', re.MULTILINE | re.UNICODE).sub('&lt;', text)
    text = re.compile('>', re.MULTILINE | re.UNICODE).sub('&gt;', text)
    return text


gcache_tckproj = {}

def maptckproj(tid=None):
    """Map a ticket to its project and return the projectname. This function
    maintains a in-module cache and is based on the assumption that a ticket
    will always be part of the same project"""
    global gcache_tckproj
    if tid not in gcache_tckproj:
        from zeta.comp.ticket import TicketComponent
        compmgr = fromconfig('compmgr')
        tckcomp = TicketComponent(compmgr)
        tcks = tckcomp.ticketdeps()
        gcache_tckproj = dict([ (k, tcks[k][0]) for k in tcks ])
    return gcache_tckproj[tid]


def urlpathcrumbs(pathinfo, host, script):
    """Decompose url and generate path crumbs for it"""
    routes_map = config['routes.map']
    urlpath = ''
    hrefs = []
    robjs = []
    notsw = False
    for part in pathinfo.split('/'):
        if part == '':
            continue
        urlpath = ('/').join([urlpath, part])
        (d, robj) = routes_map.routematch(urlpath)
        if robjs and robjs[(-1)].name == 'staticwiki':
            (_part, _link) = hrefs[(-1)]
            hrefs[-1] = (_part, _link + '/')
        robjs.append(robj)
        if robj and robj.name == 'staticwiki' and notsw:
            continue
        if robj and notsw == False:
            notsw = robj.name != 'staticwiki'
        if robj:
            link = 'http://%s%s%s' % (host, script, urlpath)
            hrefs.append((part, link))

    return hrefs


def guessrep(url):
    """Based on the rooturl format guess repository access"""
    from zeta.comp.vcs import VcsComponent
    import zeta.lib.vcsadaptor as va
    compmgr = fromconfig('compmgr')
    vcscomp = VcsComponent(compmgr)
    vrep = None
    if url[:7] == 'file://' or url[:7] == 'http://' or url[:7] == 'https://':
        for vcs in vcscomp.get_vcs():
            if commonprefix([url, vcs.rooturl]) != vcs.rooturl:
                continue
            try:
                vrep = va.open_repository(vcs)
            except:
                continue
            else:
                break

    return vrep


def attachassc2link(item, aa, ua, la, pa, ta, ra, wa):
    attachassc = getattr(aa, 'attachassc', {})
    userid2name = getattr(ua, 'id2name', {})
    licid2name = getattr(la, 'id2name', {})
    projid2name = getattr(pa, 'id2name', {})
    tdets = getattr(ta, 'tdets', {})
    rdets = getattr(ra, 'rdets', {})
    wikiid2url = getattr(wa, 'id2url', {})
    wdets = getattr(wa, 'wdets', {})
    text = ''
    if item[0] == 'user':
        name = userid2name.get(item[1], '')
        href = name and url_foruser(name) or ''
        text = href and name or ''
    elif item[0] == 'license':
        text = licid2name.get(item[1], '')
        href = text and url_forlicense(item[1]) or ''
    elif item[0] == 'project':
        text = projid2name.get(item[1], '')
        href = text and url_forproject(text) or ''
    elif item[0] == 'ticket':
        text = str(item[1])
        tdet = tdets.get(item[1], [])
        href = text and tdet and url_forticket(tdet[0], item[1]) or ''
    elif item[0] == 'review':
        text = str(item[1])
        rdet = rdets.get(item[1], [])
        href = text and rdet and url_forreview(rdet[0], item[1]) or ''
    elif item[0] == 'wiki':
        wdet = wdets.get(item[1], [])
        text = wdet and wdet[1] or ''
        href = text and wdet and url_forwiki(wdet[0], text) or ''
    if href:
        return (text, href)
    return ('', '')


def tlineplot(logs):
    """Compute timeline plot data for logs, superimposed on site timeline plot"""
    logs.reverse()
    if logs:
        maxdays = (logs[(-1)].created_on - logs[0].created_on).days
        datatline = [ [] for i in range(maxdays + 1) ]
        [ datatline[(l.created_on - logs[0].created_on).days].append([l.id, l.userhtml, l.itemhtml, l.created_on.ctime()]) for l in logs
        ]
    else:
        datatline = []
    if logs:
        startdt = [
         str(logs[0].created_on.year),
         str(logs[0].created_on.month - 1),
         str(logs[0].created_on.day)]
    else:
        startdt = [
         '2000', '0', '1']
    return (
     datatline, startdt)


def computechartwidth(xcount, threshold, defwidth):
    if xcount > threshold:
        return int(xcount / float(threshold) * defwidth)
    return defwidth


def chartify_mstn(mstntickets):
    """Convert milestone ticket information into chartable data"""
    bystatus = {}
    bytypes = {}
    byseverity = {}
    byowner = {}
    resolved = 0
    unresolved = 0
    for (ttype, tsev, tst, towner) in mstntickets:
        if ttype:
            bytypes[ttype] = bytypes.setdefault(ttype, 0) + 1
        if tsev:
            byseverity[tsev] = byseverity.setdefault(tsev, 0) + 1
        if tst:
            bystatus[tst] = bystatus.setdefault(tst, 0) + 1
            if tst in config['zeta.ticketresolv']:
                resolved += 1
            else:
                unresolved += 1
        if towner:
            byowner[towner] = byowner.setdefault(towner, 0) + 1

    mstnresolved = [
     resolved, unresolved]
    return (bystatus, bytypes, byseverity, byowner, mstnresolved)


def computecount(data, fn):
    """Apply function `fn` on each item of the iterable `data` which will
    return a key value, the number of times each key value is returned will be
    counted and returned as a map of,
        { key : count-of-key,
          ...
        }"""
    d = {}
    [ d.setdefault(fn(x), []).append(1) for x in data ]
    d = dict([ (k, sum(v)) for (k, v) in d.iteritems() ])
    return d


def date2jsdate(date, default=None):
    """From Datetime object extract paramters to convert it to JavaScript
    Date() object"""
    if date:
        fromdate = [
         str(date.year), str(date.month - 1), str(date.day)]
    else:
        fromdate = default
    return fromdate


def fix2repospath(path, roots=[]):
    """When relative path to repository is expected, sometimes, path can be
    absolute, fix it relative to one of the `roots`"""
    relpath = path
    for r in roots:
        if commonprefix([path, r]) != r:
            continue
        relpath = path.split(r)[1]

    return relpath


udiffprfx = [
 '===', '---', '+++']

def udifftolno(udiff):
    """Find the lines (numbered from 1) in that are different, based on
    unified diff text `udiff`"""

    def parserange(rngstr):
        (frm, to) = rngstr.split(',')
        i = int(frm[1:])
        j = i + int(to)
        return (frm[0], i, j)

    stripheader = lambda lines: [ l for l in lines if l not in udiffprfx ]
    splitrange = lambda hdr: hdr.strip('@ ').split(' ')
    parsehdr = lambda hdr: hdr and [ parserange(x) for x in splitrange(hdr) ]
    diffpri = []
    diffsec = []
    pricnt = seccnt = 0
    x = None
    for l in stripheader(udiff.splitlines()):
        patt = re.search('^@@ \\-[0-9]*,[0-9]* \\+[0-9]*,[0-9]* @@$', l)
        if patt:
            pricnt = seccnt = 0
            x = parsehdr(patt.group())
        elif x:
            if l[0] == '-':
                diffsec.append(x[0][1] + seccnt)
                seccnt += 1
            elif l[0] == '+':
                diffpri.append(x[1][1] + pricnt)
                pricnt += 1
            else:
                pricnt += 1
                seccnt += 1

    return [
     diffpri, diffsec]


def wikidifflno(flines, tlines):
    """Find the lines (numbered from 1) in that are different, based on
    unified diff text `udiff`"""
    m = SequenceMatcher(None, flines, tlines)
    diffpri = []
    diffsec = []
    for cluster in m.get_grouped_opcodes():
        for tup in cluster:
            if tup[0] in ('delete', 'insert', 'replace'):
                len = tup[2] - tup[1]
                diffsec.extend([ tup[1] + ln + 1 for ln in range(0, len) ])
                diffpri.extend([ tup[3] + ln + 1 for ln in range(0, len) ])

    return [
     diffpri, diffsec]


def syntaxhl(text, lexbyfile='', lexname='', linenos=False):
    """Use pygments to high-light syntax"""
    try:
        if lexbyfile:
            lexer = get_lexer_for_filename(lexbyfile)
        elif lexname:
            lexer = get_lexer_by_name(lexname)
        else:
            lexer = get_lexer_by_name('text')
    except:
        lexer = get_lexer_by_name('text')

    try:
        text = highlight(text, lexer, HtmlFormatter(linenos=linenos))
    except:
        text = '<pre></pre>'

    return text


def printdict(d):
    from pprint import pprint
    pprint(d)


def printobj(obj):
    from pprint import pprint
    pprint(dict([ (a, getattr(obj, a)) for a in dir(obj) if '__' not in a ]))