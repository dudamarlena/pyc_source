# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/forms.py
# Compiled at: 2010-07-07 01:55:16
"""Form component that implements form request and submit visitor pattern.

VForm class implements the `form-visit` pattern.
Example,
    vf = Vform( compmgr )
    vf.process( request, c, **kwargs )
The pattern expects `formname` (whose value indicates the form name to be
processed) and `form` (which can be either `submit` or `request`)

When a new Form component needs to implemented, use the following example,

    class FormSomeform( Component ) :

        formname = < either a string or list of formnames >

        def requestform( self, request, c, **kwargs ) :
            ...

        def submitform( self, request, c, **kwargs ) :
            ...
"""
from __future__ import with_statement
import re
from pytz import all_timezones, timezone
import datetime as dt
from os.path import join
from sqlalchemy.orm import mapper, relation
from pylons import config
from pylons import tmpl_context as c
from pylons.controllers.util import abort
from authkit.authorize.pylons_adaptors import authorized, authorize
from authkit.permissions import no_authkit_users_in_environ
from zeta.ccore import Component, formcomponent
from zeta.model import meta
from zeta.model.schema import t_wikipage
from zeta.model.tables import User, Wiki, WikiType, WikiTable_Map, WikiComment, wikipage_factory
from zeta.lib.error import ZetaFormError
import zeta.lib.helpers as h
from zeta.lib.constants import *
from zeta.lib.captcha import Captcha, sessioncaptcha
from zeta.lib.mailclient import inviteuser
from zeta.comp.system import SystemComponent
from zeta.comp.tag import TagComponent
from zeta.comp.attach import AttachComponent
from zeta.comp.license import LicenseComponent
from zeta.comp.project import ProjectComponent
from zeta.comp.ticket import TicketComponent
from zeta.comp.review import ReviewComponent
from zeta.comp.vcs import VcsComponent
from zeta.comp.wiki import WikiComponent
from zeta.comp.timeline import TimelineComponent
gcache_formcomps = {}
compmgr = None
syscomp = None
tagcomp = None
attcomp = None
liccomp = None
projcomp = None
tckcomp = None
vcscomp = None
wikicomp = None
revcomp = None
tlcomp = None

def do_onetime(config):
    global attcomp
    global compmgr
    global liccomp
    global projcomp
    global revcomp
    global syscomp
    global tagcomp
    global tckcomp
    global tlcomp
    global vcscomp
    global wikicomp
    if compmgr == None:
        compmgr = config['compmgr']
        syscomp = SystemComponent(compmgr)
        tagcomp = TagComponent(compmgr)
        attcomp = AttachComponent(compmgr)
        liccomp = LicenseComponent(compmgr)
        projcomp = ProjectComponent(compmgr)
        tckcomp = TicketComponent(compmgr)
        vcscomp = VcsComponent(compmgr)
        wikicomp = WikiComponent(compmgr)
        revcomp = ReviewComponent(compmgr)
        tlcomp = TimelineComponent(compmgr)
    return


class VForm(Component):
    """Component implementing the Vistor pattern for forms. Any body who wants
    to do forms processing, can call,
        VForm( comp_manager ).process( visitor, **kwargs ).
    where, 
        visitor is the Form component implementing the,
            `request()` and `submit()` api.
        kwargs will be directly passed to the `request()` and `submit()` api."""

    def process(self, request, c, **kwargs):
        """Process the form"""
        global gcache_formcomps
        do_onetime(self.compmgr.config)
        form = request.params.get('form', '')
        formnames = request.params.getall('formname')
        visitors = []
        for formname in formnames:
            v = gcache_formcomps.get(formname, None)
            if not v:
                v = gcache_formcomps.setdefault(formname, formcomponent(formname)(self.compmgr))
            visitors.append(v)

        if form == 'request':
            [ v.requestform(request, c, **kwargs) for v in visitors ]
        elif form == 'submit':
            [ v.submitform(request, c, **kwargs) for v in visitors ]
        else:
            raise ZetaFormError('Unexpected visit for form processing !!')
        return


class SampleForm(Component):

    def requestform(self):
        pass

    def submitform(self):
        pass


def parse_tags(tagnames):
    """tagnames is a comma seperated string,
    return a list of tagnames"""
    return [ t for t in [ t.strip(' ') for t in tagnames.split(',') ] if t ]


class FormSystem(Component):
    """Form Component to create/delete system table entries"""
    formname = 'system'

    def requestform(self, request, c, **kwargs):
        """Populate context for system form"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / delete system entries"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        userrel_types = request.POST.get('userrel_types', None)
        userrel_types = userrel_types != None and set(h.parse_csv(userrel_types))
        projteamtypes = request.POST.get('projteamtypes', None)
        projteamtypes = projteamtypes != None and set(h.parse_csv(projteamtypes))
        tickettypes = request.POST.get('tickettypes', None)
        tickettypes = tickettypes != None and set(h.parse_csv(tickettypes))
        ticketstatus = request.POST.get('ticketstatus', None)
        ticketstatus = ticketstatus != None and set(h.parse_csv(ticketstatus))
        ticketseverity = request.POST.get('ticketseverity', None)
        ticketseverity = ticketseverity != None and set(h.parse_csv(ticketseverity))
        reviewnatures = request.POST.get('reviewnatures', None)
        reviewnatures = reviewnatures != None and set(h.parse_csv(reviewnatures))
        reviewactions = request.POST.get('reviewactions', None)
        reviewactions = reviewactions != None and set(h.parse_csv(reviewactions))
        wikitypes = request.POST.get('wikitypes', None)
        wikitypes = wikitypes != None and set(h.parse_csv(wikitypes))
        vcstypes = request.POST.get('vcstypes', None)
        vcstypes = vcstypes != None and set(h.parse_csv(vcstypes))
        ticketresolv = request.POST.get('ticketresolv', None)
        ticketresolv = ticketresolv != None and set(h.parse_csv(ticketresolv))
        specialtags = request.POST.get('specialtags', None)
        specialtags = specialtags != None and set(h.parse_csv(specialtags))
        def_wikitype = request.POST.get('def_wikitype', None)
        googlemaps = request.POST.get('googlemaps', None)
        strictauth = request.POST.get('strictauth', None)
        welcomestring = request.POST.get('welcomestring', None)
        userpanes = request.POST.get('userpanes', None)
        regrbyinvite = request.POST.get('regrbyinvite', None)
        invitebyall = request.POST.get('invitebyall', None)
        reltypes = set(userscomp.reltypes)
        teams = set(projcomp.teams)
        tcktypenames = set(tckcomp.tcktypenames)
        tckstatusnames = set(tckcomp.tckstatusnames)
        tckseveritynames = set(tckcomp.tckseveritynames)
        naturenames = set(revcomp.naturenames)
        actionnames = set(revcomp.actionnames)
        vcstypenames = set(vcscomp.vcstypenames)
        typenames = set(wikicomp.typenames)
        tagnames = set(tagcomp.tagnames)
        addrel_types = list(userrel_types.difference(reltypes))
        addteams = list(projteamtypes.difference(teams))
        addtickettypes = list(tickettypes.difference(tcktypenames))
        addticketstatus = list(ticketstatus.difference(tckstatusnames))
        addticketseverity = list(ticketseverity.difference(tckseveritynames))
        addreviewnatures = list(reviewnatures.difference(naturenames))
        addreviewactions = list(reviewactions.difference(actionnames))
        addwikitype = list(wikitypes.difference(typenames))
        addvcstypes = list(vcstypes.difference(vcstypenames))
        addspecialtags = list(specialtags.difference(tagnames))
        if user_id:
            addrel_types and userscomp.userreltype_create(addrel_types)
            addteams and projcomp.create_projteamtype(addteams)
            addtickettypes and tckcomp.create_tcktype(addtickettypes)
            addticketstatus and tckcomp.create_tckstatus(addticketstatus)
            addticketseverity and tckcomp.create_tckseverity(addticketseverity)
            addreviewnatures and revcomp.create_reviewnature(addreviewnatures)
            addreviewactions and revcomp.create_reviewaction(addreviewactions)
            addwikitype and wikicomp.create_wikitype(addwikitype)
            addvcstypes and vcscomp.create_vcstype(addvcstypes)
            addspecialtags and [ tagcomp.create_tag(t) for t in addspecialtags ]
        se = {}
        userrel_types and se.update({'userrel_types': (', ').join(userscomp.reltypes)})
        projteamtypes and se.update({'projteamtypes': (', ').join(projcomp.teams)})
        tickettypes and se.update({'tickettypes': (', ').join(tckcomp.tcktypenames)})
        ticketstatus and se.update({'ticketstatus': (', ').join(tckcomp.tckstatusnames)})
        ticketseverity and se.update({'ticketseverity': (', ').join(tckcomp.tckseveritynames)})
        reviewnatures and se.update({'reviewnatures': (', ').join(revcomp.naturenames)})
        reviewactions and se.update({'reviewactions': (', ').join(revcomp.actionnames)})
        vcstypes and se.update({'vcstypes': (', ').join(vcscomp.vcstypenames)})
        wikitypes and se.update({'wikitypes': (', ').join(wikicomp.typenames)})
        ticketresolv and se.update({'ticketresolv': (', ').join(ticketresolv)})
        specialtags and se.update({'specialtags': (', ').join(specialtags)})
        def_wikitype and se.update({'def_wikitype': def_wikitype})
        googlemaps and se.update({'googlemaps': googlemaps})
        strictauth and se.update({'strictauth': strictauth})
        welcomestring and se.update({'welcomestring': welcomestring})
        userpanes and se.update({'userpanes': (', ').join(set(h.parse_csv(userpanes)))})
        regrbyinvite and se.update({'regrbyinvite': regrbyinvite})
        invitebyall and se.update({'invitebyall': invitebyall})
        c.sysentries.update(se)
        syscomp.set_sysentry(c.sysentries, byuser=c.authuser)
        return


class FormSiteLogo(Component):
    """Form Component to upload site logo"""
    formname = [
     'sitelogo']

    def requestform(self, request, c, **kwargs):
        """Populate context for system form"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / delete system entries"""
        user_id = request.POST.get('user_id', None)
        sitelogo = request.POST.get('sitelogofile', '')
        envpath = self.compmgr.config.get('zeta.envpath')
        if c.sitelogo and sitelogo != '':
            open(join(envpath, 'public', c.sitelogo.lstrip(' /')), 'w').write(sitelogo.file.read())
        return


class FormStaticWiki(Component):
    """Form Component to create/delete system table entries"""
    formname = [
     'editsw']

    def requestform(self, request, c, **kwargs):
        """Populate context for system form"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / delete system entries"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        pathurl = request.POST.get('pathurl', None)
        text = request.POST.get('text', None)
        h.validate_fields(request)
        pathurl and syscomp.set_staticwiki(pathurl, text, byuser=c.authuser)
        return


class FormPermissions(Component):
    """Form component to create and map permission groups"""

    def requestform(self, request, c, **kwargs):
        """Populate context for permission groups"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / Update / Delete entries in permission_group, permission_name
        and permission_maps tables"""
        pass


class FormPermgroup(FormPermissions):
    """Form Component to create permission group and permission names"""
    formname = [
     'createpg', 'updatepg', 'addpntopg', 'delpnfrompg']

    def submitform(self, request, c, **kwargs):
        """create perm_group and group perm_names under it"""
        userscomp = self.compmgr.config['userscomp']
        formname = request.params.get('formname', None)
        perm_group_id = request.POST.get('perm_group_id', None)
        perm_group = request.POST.get('perm_group', None)
        perm_names = request.POST.getall('perm_name')
        if formname in ('createpg', 'updatepg') and not perm_group:
            raise ZetaFormError('perm_group cannot be empty !!')
        elif formname in ('addpntopg', 'delpnfrompg') and not perm_names:
            raise ZetaFormError('perm_group cannot be empty !!')
        h.validate_fields(request)
        if formname == 'createpg':
            pg = userscomp.create_permgroup(perm_group)
            userscomp.add_permnames_togroup(pg, perm_names)
        elif formname == 'updatepg':
            pg = userscomp.get_permgroup(int(perm_group_id))
            if pg.perm_group != perm_group:
                userscomp.change_permgroup(pg, perm_group)
        elif formname == 'addpntopg':
            pg = userscomp.get_permgroup(int(perm_group_id))
            userscomp.add_permnames_togroup(pg, perm_names)
        elif formname == 'delpnfrompg':
            pg = userscomp.get_permgroup(int(perm_group_id))
            userscomp.remove_permnames_fromgroup(pg, perm_names)
        return


class FormDeletePermgroup(FormPermissions):
    """Form Component to delete permission group and permission names"""
    formname = 'delpg'

    def submitform(self, request, c, **kwargs):
        """delete perm_group"""
        userscomp = self.compmgr.config['userscomp']
        perm_groups = request.POST.getall('perm_group')
        perm_groups and userscomp.remove_permgroup(perm_groups)


class FormUsers(Component):
    """Form component to process user entries"""

    def requestform(self, request, c, **kwargs):
        """Populate context for users"""
        userscomp = self.compmgr.config['userscomp']
        c.all_timezones = all_timezones

    def submitform(self, request, c, **kwargs):
        """Create / Update / Delete user entries"""
        pass


class FormCreateUser(FormUsers):
    """Form Component to create user entries"""
    formname = [
     'createuser', 'updateuser']

    def requestform(self, request, c, **kwargs):
        """Populate context for users"""
        c.captcha = Captcha()

    def submitform(self, request, c, **kwargs):
        """create / update user entry"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        username = request.POST.get('username', None)
        emailid = request.POST.get('emailid', None)
        password = request.POST.get('password', None)
        confpass = request.POST.get('confpass', None)
        timezone = request.POST.get('timezone', None)
        firstname = request.POST.get('firstname', None)
        middlename = request.POST.get('middlename', '')
        lastname = request.POST.get('lastname', None)
        addressline1 = request.POST.get('addressline1', None)
        addressline2 = request.POST.get('addressline2', None)
        city = request.POST.get('city', None)
        pincode = request.POST.get('pincode', None)
        state = request.POST.get('state', None)
        country = request.POST.get('country', None)
        userpanes = request.POST.get('userpanes', None)
        captcha = request.POST.get('captcha', None)
        errmsg = ''
        errmsg += not username and 'username, ' or ''
        errmsg += not emailid and 'emailid, ' or ''
        errmsg += not user_id and (not password or password != confpass) and 'password, ' or ''
        errmsg += not timezone and 'timezone, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        user = (
         username, emailid, password, timezone)
        uinfo = (firstname, middlename, lastname, addressline1,
         addressline2, city, pincode, state, country, userpanes)
        if user_id:
            userscomp.user_create(user, uinfo, update=True)
        elif userscomp.user_exists(username):
            raise ZetaFormError('Username %s already exists' % username)
        elif captcha and sessioncaptcha().match(captcha.upper()):
            userscomp.user_create(user, uinfo)
            sessioncaptcha().destroy()
        elif kwargs.get('test', None):
            userscomp.user_create(user, uinfo)
        else:
            raise ZetaFormError('Captcha mismatch')
        return


class FormUpdatePassword(FormUsers):
    """Form Component to update user password"""
    formname = 'updtpass'

    def submitform(self, request, c, **kwargs):
        """create / update user entry"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        confpass = request.POST.get('confpass', None)
        if password != confpass:
            raise ZetaFormError('Mismatch in the re-entering the password !!')
        if user_id and password:
            user = userscomp.get_user(int(user_id))
            user = (user.username, user.emailid, password, user.timezone)
            userscomp.user_create(user, update=True)
        else:
            raise ZetaFormError('In-sufficient, detail user-id')
        return


class FormUserPhoto(FormUsers):
    """Form Component to update user photo attachment"""
    formname = [
     'userphoto', 'deluserphoto']

    def submitform(self, request, c, **kwargs):
        """update user photo"""
        userscomp = self.compmgr.config['userscomp']
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        attachfile = request.POST.get('attachfile', None)
        user = kwargs.get('user', None)
        if attachfile != None and user_id and user:
            photo = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
            userscomp.user_set_photo(int(user_id), photo)
        elif formname == 'deluserphoto' and user_id:
            userscomp.user_set_photo(int(user_id), photo=None)
        else:
            raise ZetaFormError('In-sufficient detail, user-id and attachfile')
        return


class FormUserIcon(FormUsers):
    """Form Component to update user icon attachment"""
    formname = [
     'usericon', 'delusericon']

    def submitform(self, request, c, **kwargs):
        """update user icon"""
        userscomp = self.compmgr.config['userscomp']
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        attachfile = request.POST.get('attachfile', None)
        user = kwargs.get('user', None)
        if attachfile != None and user_id and user:
            icon = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
            userscomp.user_set_icon(int(user_id), icon)
        elif formname == 'delusericon' and user_id:
            userscomp.user_set_icon(int(user_id), icon=None)
        else:
            raise ZetaFormError('In-sufficient detail, user-id and attachfile')
        return


class FormUserDisable(FormUsers):
    """Form Component to update user disable status"""
    formname = [
     'userdis', 'userenb']

    def submitform(self, request, c, **kwargs):
        """update user disable status"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        [ userscomp.user_disable(u) for u in request.POST.getall('disable_user')
        ]
        [ userscomp.user_disable(u, disable=False) for u in request.POST.getall('enable_user')
        ]
        return


class FormUserPermissions(FormUsers):
    """Form Component to update user permissions"""
    formname = [
     'adduserperms', 'deluserperms']

    def submitform(self, request, c, **kwargs):
        """update user permissions"""
        userscomp = self.compmgr.config['userscomp']
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        username = request.POST.get('username', None)
        perm_groups = request.POST.getall('perm_group')
        if user_id and username:
            if formname == 'deluserperms':
                userscomp.user_remove_permgroup(username, perm_groups)
            else:
                userscomp.user_add_permgroup(username, perm_groups)
        else:
            raise ZetaFormError('In-sufficient detail, user-id')
        return


class FormUserRelations(FormUsers):
    """Form Component to update user relations"""
    formname = [
     'adduserrels', 'approveuserrels', 'deluserrels']

    def submitform(self, request, c, **kwargs):
        """update user relations"""
        userscomp = self.compmgr.config['userscomp']
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        user_relation_ids = [ int(id) for id in request.POST.getall('user_relation_id')
                            ]
        if user_id:
            if formname == 'approveuserrels' and user_relation_ids:
                userscomp.user_approve_relation(user_relation_ids, approve=True)
            elif formname == 'deluserrels' and user_relation_ids:
                userscomp.user_remove_relation(user_relation_ids)
            else:
                userrel_type = request.POST.get('userrel_type', None)
                userfrom = request.POST.get('userfrom', None)
                tousers = request.POST.getall('userto')
                if userrel_type and userfrom and tousers:
                    [ userscomp.user_add_relation(userfrom, userto, userrel_type) for userto in tousers ]
                else:
                    errmsg = 'In-sufficient detail for creating user relation'
                    raise ZetaFormError(errmsg)
        else:
            raise ZetaFormError('In-sufficient detail, user_id')
        return


class FormInviteUser(FormUsers):
    """Form Component to invite user"""
    formname = 'inviteuser'

    def submitform(self, request, c, **kwargs):
        """invite user"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        emailid = request.POST.get('emailid', None)
        if user_id and emailid:
            user = userscomp.get_user(int(user_id))
            environ = request.environ
            digest = userscomp.inviteuser(user, emailid)
            fullurl = h.fullurl(environ['HTTP_HOST'], environ['SCRIPT_NAME'], h.url_foruserreg(digest))
            inviteuser(emailid, fullurl, user, c.sysentries['sitename'])
        return


class FormResetPass(FormUsers):
    """Form Component to reset user password"""
    formname = 'resetpass'

    def submitform(self, request, c, **kwargs):
        """Reset user password"""
        userscomp = self.compmgr.config['userscomp']
        emailid = kwargs.get('emailid', None)
        password = request.POST.get('password', None)
        confpass = request.POST.get('confpass', None)
        user = emailid and userscomp.userbyemailid(unicode(emailid))
        if user and password and password == confpass:
            user = (
             user.username, user.emailid, password, user.timezone)
            userscomp.user_create(user, update=True)
        else:
            raise ZetaFormError('Failed to match requirements')
        return


class FormLicense(Component):
    """Form component to process license"""

    def requestform(self, request, c, **kwargs):
        """Populate context for license"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / Update / Delete user entries"""
        pass


class FormCreateLicense(FormLicense):
    """Form component to create / update license entry"""
    formname = [
     'createlic', 'updatelic']

    def submitform(self, request, c, **kwargs):
        """create / update license entry"""
        user_id = request.POST.get('user_id', None)
        license_id = request.POST.get('license_id', None)
        license_id = license_id and int(license_id)
        licensename = request.POST.get('licensename', None)
        summary = request.POST.get('summary', None)
        text = request.POST.get('text', None)
        source = request.POST.get('source', None)
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        attachfiles = request.POST.getall('attachfile')
        user = kwargs.get('user', None)
        errmsg = ''
        errmsg += not licensename and 'licensename, ' or ''
        errmsg += not summary and 'summary, ' or ''
        errmsg += not text and 'text, ' or ''
        errmsg += not source and 'source, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        licensedet = [
         license_id, licensename, summary, text, source]
        if license_id:
            liccomp.create_license(licensedet, update=True)
        elif liccomp.license_exists(licensename):
            raise ZetaFormError('Licensename %s already exists' % licensename)
        else:
            l = liccomp.create_license(licensedet)
            if tagnames:
                liccomp.add_tags(l, tagnames)
            if user:
                for attachfile in attachfiles:
                    a = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
                    liccomp.add_attach(l, a)

        return


class FormRemoveLicense(FormLicense):
    """Form component to remove license entry"""
    formname = 'rmlic'

    def submitform(self, request, c, **kwargs):
        """remove license entry"""
        user_id = request.POST.get('user_id', None)
        id = kwargs.get('id', None)
        [ liccomp.remove_license(licensename) for licensename in request.POST.getall('licensename')
        ]
        if isinstance(id, (int, long)):
            liccomp.remove_license(id)
        return


class FormLicenseTags(FormLicense):
    """Form component to add / remove license tags"""
    formname = [
     'addlictags', 'dellictags']

    def submitform(self, request, c, **kwargs):
        """add / remove license tags"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        license_id = request.POST.get('license_id', None)
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        if license_id and formname == 'addlictags':
            license_id = int(license_id)
            liccomp.add_tags(license_id, tagnames)
        if license_id and formname == 'dellictags':
            license_id = int(license_id)
            liccomp.remove_tags(license_id, tagnames)
        return


class FormLicenseAttachs(FormLicense):
    """Form component to add / remove license attachments"""
    formname = [
     'addlicattachs', 'dellicattachs']

    def submitform(self, request, c, **kwargs):
        """add / remove license attachments"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        license_id = request.POST.get('license_id', None)
        user = kwargs.get('user', None)
        if license_id and formname == 'dellicattachs':
            [ liccomp.remove_attach(int(license_id), int(attach_id)) for attach_id in request.POST.getall('attach_id') ]
        elif license_id and formname == 'addlicattachs' and user:
            for attachfile in request.POST.getall('attachfile'):
                a = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
                liccomp.add_attach(int(license_id), a)

        return


class FormAttachs(Component):
    """Form component to process attachments"""

    def requestform(self, request, c, **kwargs):
        """Populate context for attachment"""
        pass

    def submitform(self, request, c, **kwargs):
        """create / update / delete attachment table entries"""
        pass


class FormAddAttachs(FormAttachs):
    """Form component to remove attachment"""
    formname = 'addattachs'

    def submitform(self, request, c, **kwargs):
        """add new attachment"""
        user_id = request.POST.get('user_id', None)
        summary = request.POST.get('summary', None)
        for attachfile in request.POST.getall('attachfile'):
            attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=int(user_id), summary=summary)

        return


class FormRemoveAttach(FormAttachs):
    """Form component to remove attachment"""
    formname = 'rmattachs'

    def submitform(self, request, c, **kwargs):
        """remove attachment"""
        user_id = request.POST.get('user_id', None)
        attach_ids = request.POST.getall('attach_id', [])
        [ attcomp.remove_attach(int(attach_id)) for attach_id in attach_ids ]
        return


class FormAttachsUpdate(FormAttachs):
    """Form component to update attachment summary and tags"""
    formname = [
     'attachssummary', 'attachstags']

    def submitform(self, request, c, **kwargs):
        """update attachment entry"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        attachment_id = request.POST.get('attachment_id', None)
        summary = request.POST.get('summary', '')
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        if user_id and attachment_id:
            if formname == 'attachssummary':
                attcomp.edit_summary(int(attachment_id), summary=summary)
            if formname == 'attachstags':
                attach = attcomp.get_attach(int(attachment_id), attrload=[
                 'tags'])
                currtags = set([ tag.tagname for tag in attach.tags ])
                rmtags = list(currtags.difference(tagnames))
                addtags = list(set(tagnames).difference(currtags))
                rmtags and attcomp.remove_tags(attach, tags=rmtags)
                addtags and attcomp.add_tags(attach, tags=addtags)
        return


class FormProjects(Component):
    """Form Component to process project fields"""

    def requestform(self, request, c, **kwargs):
        """Populate context for project"""
        pass

    def submitform(self, request, c, **kwargs):
        """create / update / delete project table entries"""
        pass


class FormCreateProject(FormProjects):
    """Form component to create / update project entry"""
    formname = [
     'createprj', 'updateprj']

    def submitform(self, request, c, **kwargs):
        """create / update project entry"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        projectname = request.POST.get('projectname', None)
        summary = request.POST.get('summary', None)
        admin_email = request.POST.get('admin_email', None)
        description = request.POST.get('description', None)
        licensename = request.POST.get('licensename', None)
        admin = request.POST.get('admin', None)
        errmsg = ''
        errmsg += not licensename and 'licensename, ' or ''
        errmsg += not summary and 'summary, ' or ''
        errmsg += not admin_email and 'admin_email, ' or ''
        errmsg += not description and 'description, ' or ''
        errmsg += not admin and 'admin, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        prjdetail = [None, projectname, summary, admin_email, licensename,
         admin]
        prjidetail = [description]
        if project_id:
            prjdetail[0] = int(project_id)
            projcomp.create_project(prjdetail, prjidetail, update=True)
        elif projcomp.project_exists(projectname):
            raise ZetaFormError('Projectname %s already exists' % projectname)
        else:
            p = projcomp.create_project(prjdetail, prjidetail)
            if p:
                w = wikicomp.create_wiki(unicode(h.url_forwiki(p.projectname, PROJHOMEPAGE)), type=c.sysentries.get('def_wikitype', None), creator=c.authuser)
                wikicomp.config_wiki(w, project=p)
                wikicomp.create_content(w.id, c.authuser, syscomp.get_staticwiki('p_homepage').text)
        return


class FormProjectLicense(FormProjects):
    """Form component to update / remove project license"""
    formname = 'prjlic'

    def submitform(self, request, c, **kwargs):
        """update / remove project license"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        licensename = request.POST.get('licensename', None)
        if not licensename:
            raise ZetaFormError('Check licensename !!')
        if project_id:
            projcomp.config_project(int(project_id), license=licensename)
        return


class FormProjectAdmin(FormProjects):
    """Form component to update project admin"""
    formname = 'prjadmin'

    def submitform(self, request, c, **kwargs):
        """update project admin"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        adminname = request.POST.get('adminname', None)
        if not adminname:
            raise ZetaFormError('Check adminname !!')
        if project_id:
            projcomp.config_project(int(project_id), admin=adminname)
        return


class FormProjectFavorite(FormProjects):
    """Form component to add or remove a project being a user's favourite"""
    formname = 'projfav'

    def submitform(self, request, c, **kwargs):
        """add / remove project favourite"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        addfavuser = request.POST.get('addfavuser', None)
        delfavuser = request.POST.get('delfavuser', None)
        if addfavuser and project_id:
            projcomp.addfavorites(int(project_id), addfavuser)
        elif delfavuser and project_id:
            projcomp.delfavorites(int(project_id), delfavuser)
        return


class FormProjectDisable(FormProjects):
    """Form component to update project disable status"""
    formname = [
     'prjdis', 'prjenb']

    def submitform(self, request, c, **kwargs):
        """update project disable status"""
        user_id = request.POST.get('user_id', None)
        [ projcomp.config_project(projectname, disable=True) for projectname in request.POST.getall('disable_project')
        ]
        [ projcomp.config_project(projectname, disable=False) for projectname in request.POST.getall('enable_project')
        ]
        return


class FormProjectExpose(FormProjects):
    """Form component to update project expose status"""
    formname = [
     'prjexp', 'prjprv']

    def submitform(self, request, c, **kwargs):
        """update project expose status"""
        projcomp = ProjectComponent(self.compmgr)
        user_id = request.POST.get('user_id', None)
        expprojects = request.POST.getall('expose_project')
        prvprojects = request.POST.getall('private_project')
        [ projcomp.config_project(projectname, expose=True) for projectname in expprojects
        ]
        [ projcomp.config_project(projectname, expose=False) for projectname in prvprojects
        ]
        return


class FormProjectLogo(FormProjects):
    """Form component to update / remove project logo"""
    formname = [
     'addprjlogo', 'delprjlogo']

    def submitform(self, request, c, **kwargs):
        """update / remove project logo"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        attachfile = request.POST.get('attachfile', None)
        user = kwargs.get('user', None)
        if attachfile != None and project_id and user:
            logo = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
            projcomp.config_project(int(project_id), logo=logo)
        elif formname == 'delprjlogo' and project_id:
            projcomp.config_project(int(project_id), logo=None)
        else:
            raise ZetaFormError('In-sufficient detail, project-id and attachfile')
        return


class FormProjectIcon(FormProjects):
    """Form component to update / remove project icon"""
    formname = [
     'addprjicon', 'delprjicon']

    def submitform(self, request, c, **kwargs):
        """update / remove project icon"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        attachfile = request.POST.get('attachfile', None)
        user = kwargs.get('user', None)
        if attachfile != None and project_id and user:
            icon = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
            projcomp.config_project(int(project_id), icon=icon)
        elif formname == 'delprjicon' and project_id:
            projcomp.config_project(int(project_id), icon=None)
        else:
            raise ZetaFormError('In-sufficient detail, project-id and attachfile')
        return


class FormProjectMailinglist(FormProjects):
    """Form component to add / remove project mailinglist"""
    formname = 'prjml'

    def submitform(self, request, c, **kwargs):
        """add / remove project mailinglist"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        mailinglists = request.POST.get('mailinglists', '') and request.POST.get('mailinglists', '').split(',')
        mailinglists = [ m for m in [ m.strip(' ') for m in mailinglists ] if m ]
        appendml = kwargs.get('appendml', False)
        if filter(lambda ml: bool(ml), mailinglists):
            projcomp.set_mailinglists(int(project_id), mailinglists, append=appendml)
        else:
            projcomp.set_mailinglists(int(project_id), mailinglists=None)
        return


class FormProjectIRCchannels(FormProjects):
    """Form component to add / remove project IRCChannels"""
    formname = 'prjirc'

    def submitform(self, request, c, **kwargs):
        """add / remove project IRCChannels"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ircchannels = request.POST.get('ircchannels', '') and request.POST.get('ircchannels', '').split(',')
        ircchannels = [ i for i in [ i.strip(' ') for i in ircchannels ] if i ]
        appendirc = kwargs.get('appendirc', False)
        if filter(lambda irc: bool(irc), ircchannels):
            projcomp.set_ircchannels(int(project_id), ircchannels, append=appendirc)
        else:
            projcomp.set_ircchannels(int(project_id), ircchannels=None)
        return


class FormProjectCreateComponent(FormProjects):
    """Form component to create / update project components"""
    formname = [
     'createpcomp', 'updatepcomp']

    def submitform(self, request, c, **kwargs):
        """create / update project components"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        component_id = request.POST.get('component_id', None)
        componentname = request.POST.get('componentname', None)
        description = request.POST.get('description', None)
        owner = request.POST.get('owner', None)
        errmsg = ''
        errmsg += not componentname and 'componentname, ' or ''
        errmsg += not description and 'description, ' or ''
        errmsg += not owner and 'owner, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        compdetail = [
         None, componentname, description, owner]
        if component_id:
            compdetail[0] = int(component_id)
            projcomp.create_component(int(project_id), compdetail, update=True)
        else:
            c = projcomp.create_component(int(project_id), compdetail)
        return


class FormProjectComponentOwner(FormProjects):
    """Form component to update / remove component owner"""
    formname = 'pcompowner'

    def submitform(self, request, c, **kwargs):
        """update /remove component owner"""
        projcomp = ProjectComponent(self.compmgr)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        component_id = request.POST.get('component_id', None)
        owner = request.POST.get('owner', None)
        comp = projcomp.get_component(int(component_id))
        if comp and owner:
            compdetail = [
             comp.id, comp.componentname, comp.description,
             owner]
            projcomp.create_component(int(project_id), compdetail, update=True)
        return


class FormProjectRemoveComponent(FormProjects):
    """Form component to remove project components"""
    formname = 'rmpcomp'

    def submitform(self, request, c, **kwargs):
        """remove project components"""
        projcomp = ProjectComponent(self.compmgr)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        component_ids = request.POST.getall('component_id')
        [ projcomp.remove_component(int(project_id), int(component_id)) for component_id in component_ids
        ]
        return


class FormProjectCreateMilestone(FormProjects):
    """Form component to create / update project milestones"""
    formname = [
     'createmstn', 'updatemstn']

    def submitform(self, request, c, **kwargs):
        """create / update project milestones,
        due_date is expect in UTC."""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        milestone_id = request.POST.get('milestone_id', None)
        milestone_name = request.POST.get('milestone_name', None)
        description = request.POST.get('description', None)
        due_date = request.POST.get('due_date', None)
        errmsg = ''
        errmsg += not milestone_name and 'milestone_name, ' or ''
        errmsg += not description and 'description, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        if due_date:
            usertz = timezone(userscomp.get_user(int(user_id)).timezone)
            due_date = h.usertz_2_utc(dt.datetime.strptime(due_date, '%Y-%m-%d'), usertz)
        mstndetail = [
         None, milestone_name, description, due_date]
        if milestone_id:
            mstndetail[0] = int(milestone_id)
            projcomp.create_milestone(int(project_id), mstndetail, update=True)
        else:
            m = projcomp.create_milestone(int(project_id), mstndetail)
        return


class FormProjectMilestoneDuedate(FormProjects):
    """Form component to update milestone due_date
        due_date is expect in UTC."""
    formname = 'mstnduedate'

    def submitform(self, request, c, **kwargs):
        """update milestone duedate"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        milestone_id = request.POST.get('milestone_id', None)
        due_date = request.POST.get('due_date', None)
        m = projcomp.get_milestone(int(milestone_id))
        if due_date:
            usertz = timezone(userscomp.get_user(int(user_id)).timezone)
            due_date = h.usertz_2_utc(dt.datetime.strptime(due_date, '%Y-%m-%d'), usertz)
        if m and due_date:
            mstndetail = [
             m.id, m.milestone_name, m.description, due_date]
            projcomp.create_milestone(int(project_id), mstndetail, update=True)
        return


class FormProjectCloseMilestone(FormProjects):
    """Form component to close milestone"""
    formname = 'mstnclose'

    def submitform(self, request, c, **kwargs):
        """close milestone"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        milestone_id = request.POST.get('milestone_id', None)
        closing_remark = request.POST.get('closing_remark', None)
        status = request.POST.get('status', None)
        errmsg = ''
        errmsg += status and not closing_remark and 'closing_remark, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        m = projcomp.get_milestone(int(milestone_id))
        if closing_remark and m and status:
            projcomp.close_milestone(m, closing_remark, status)
        return


class FormProjectRemoveMilestone(FormProjects):
    """Form component to remove project milestones"""
    formname = 'rmmstn'

    def submitform(self, request, c, **kwargs):
        """remove project milestones"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        milestone_ids = request.POST.getall('milestone_id')
        [ projcomp.remove_milestone(int(project_id), int(milestone_id)) for milestone_id in milestone_ids
        ]
        return


class FormProjectCreateVersion(FormProjects):
    """Form component to create / update project versions"""
    formname = [
     'createver', 'updatever']

    def submitform(self, request, c, **kwargs):
        """create / update project versions"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        version_id = request.POST.get('version_id', None)
        version_name = request.POST.get('version_name', None)
        description = request.POST.get('description', None)
        errmsg = ''
        errmsg += not version_name and 'version_name, ' or ''
        errmsg += not description and 'description, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        verdetail = [
         None, version_name, description]
        if version_id and project_id:
            verdetail[0] = int(version_id)
            projcomp.create_version(int(project_id), verdetail, update=True)
        elif project_id:
            v = projcomp.create_version(int(project_id), verdetail)
        return


class FormProjectRemoveVersion(FormProjects):
    """Form component to remove project versions"""
    formname = 'rmver'

    def submitform(self, request, c, **kwargs):
        """remove project versions"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        version_ids = request.POST.getall('version_id')
        [ projcomp.remove_version(int(project_id), int(version_id)) for version_id in version_ids
        ]
        return


class FormProjectTags(FormProjects):
    """Form component to add / remove project tags"""
    formname = [
     'addprjtags', 'delprjtags']

    def submitform(self, request, c, **kwargs):
        """add / remove project tags"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        component_id = request.POST.get('component_id', None)
        milestone_id = request.POST.get('milestone_id', None)
        version_id = request.POST.get('version_id', None)
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        entity = component_id and 'component' or milestone_id and 'milestone' or version_id and 'version' or None
        id = component_id and int(component_id) or milestone_id and int(milestone_id) or version_id and int(version_id) or int(project_id)
        if project_id and id and formname == 'addprjtags':
            obj = entity == 'component' and projcomp.get_component(id) or entity == 'milestone' and projcomp.get_milestone(id) or entity == 'version' and projcomp.get_version(id) or projcomp.get_project(id)
            projcomp.add_tags(int(project_id), entity, id, tagnames)
        if project_id and id and formname == 'delprjtags':
            obj = entity == 'component' and projcomp.get_component(id) or entity == 'milestone' and projcomp.get_milestone(id) or entity == 'version' and projcomp.get_version(id) or projcomp.get_project(id)
            projcomp.remove_tags(int(project_id), entity, id, tagnames)
        return


class FormProjectAttachs(FormProjects):
    """Form component to add / remove project attachments"""
    formname = [
     'addprjattachs', 'delprjattachs']

    def submitform(self, request, c, **kwargs):
        """add / remove project attachments"""
        attcomp = AttachComponent(self.compmgr)
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        user = kwargs.get('user', None)
        if project_id and formname == 'delprjattachs':
            [ projcomp.remove_attach(int(project_id), int(attach_id)) for attach_id in request.POST.getall('attach_id') ]
        elif project_id and formname == 'addprjattachs' and user:
            for attachfile in request.POST.getall('attachfile'):
                a = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
                projcomp.add_attach(int(project_id), a)

        return


class FormProjectTeam(FormProjects):
    """Form component to add / remove project-teams"""
    formname = ['addprjteam', 'delprjteam']

    def submitform(self, request, c, **kwargs):
        """add / remove project-teams"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        if formname == 'delprjteam':
            project_team_ids = [ int(id) for id in request.POST.getall('project_team_id') ]
            projcomp.remove_project_users(project_team_ids)
        else:
            team_type = request.POST.get('team_type', None)
            projectusers = request.POST.getall('projuser')
            projcomp.add_project_user(int(project_id), team_type, projectusers)
        return


class FormProjectTeamPermissions(FormProjects):
    """Form component to add /remove project-team permissions"""
    formname = [
     'addteamperms', 'delteamperms']

    def submitform(self, request, c, **kwargs):
        """add / remove project-team permissions"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        if formname == 'delteamperms':
            projectteam_perm_ids = [ int(id) for id in request.POST.getall('projectteam_perm_id') ]
            projcomp.remove_projectteam_perm(projectteam_perm_ids)
        else:
            team_type = request.POST.get('team_type', None)
            perm_groups = request.POST.getall('perm_group')
            projcomp.add_projectteam_perm(int(project_id), team_type, perm_groups)
        return


class FormProjectPermission(FormProjects):
    """Form component to add /remove project-user permissions"""
    formname = [
     'addprjperms', 'delprjperms']

    def submitform(self, request, c, **kwargs):
        """add / remove project-user permissions"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        if formname == 'delprjperms':
            project_perm_ids = [ int(id) for id in request.POST.getall('project_perm_id') ]
            projcomp.remove_project_permission(project_perm_ids)
        else:
            projuser = request.POST.get('projuser', None)
            perm_groups = request.POST.getall('perm_group')
            [ projcomp.add_project_permission(int(project_id), projuser, perm_group) for perm_group in perm_groups
            ]
        return


class FormTickets(Component):
    """Form component to create / update / delete ticket tables"""

    def requestform(self, request, c, **kwargs):
        """Populate context for ticket forms"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / Update / Delete entries in ticket tables"""
        pass


class FormCreateTicket(FormTickets):
    """Form component to create / update tickets"""
    formname = 'createtck'

    def submitform(self, request, c, **kwargs):
        """create / update ticket table"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        summary = request.POST.get('summary', None)
        description = request.POST.get('description', None)
        tck_typename = request.POST.get('tck_typename', None)
        tck_severityname = request.POST.get('tck_severityname', None)
        promptuser = request.POST.get('promptuser', None)
        component_ids = request.POST.getall('component_id')
        component_ids = component_ids or None
        milestone_ids = request.POST.getall('milestone_id')
        milestone_ids = milestone_ids or None
        version_ids = request.POST.getall('version_id')
        version_ids = version_ids or None
        parent_id = request.POST.get('parent_id', None)
        blocking_ids = request.POST.get('blocking_ids', '') and request.POST.get('blocking_ids', '').split(',')
        blocking_ids = [ id for id in [ id.strip(' ') for id in blocking_ids ] if id ]
        blockedby_ids = request.POST.get('blockedby_ids', '') and request.POST.get('blockedby_ids', '').split(',')
        blockedby_ids = [ id for id in [ id.strip(' ') for id in blockedby_ids ] if id ]
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        append = kwargs.get('append', False)
        errmsg = ''
        errmsg += not summary and 'summary, ' or ''
        errmsg += not tck_typename and 'tck_typename, ' or ''
        errmsg += not tck_severityname and 'tck_severityname, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        tckdetail = [
         None, summary, description, tck_typename,
         tck_severityname]
        promptuser = promptuser or int(user_id)
        if ticket_id:
            ticket_id = int(ticket_id)
            tckdetail[0] = ticket_id
            tckcomp.create_ticket(int(project_id), tckdetail, promptuser, update=True)
        else:
            owner = int(user_id)
            t = tckcomp.create_ticket(int(project_id), tckdetail, promptuser, owner, index=False)
            ticket_id = t.id
            if tagnames:
                tckcomp.add_tags(t, tagnames)
        tckcomp.config_ticket(ticket_id, parent=parent_id and int(parent_id) or None, components=component_ids and [ int(id) for id in component_ids if id ], milestones=milestone_ids and [ int(id) for id in milestone_ids if id ], versions=version_ids and [ int(id) for id in version_ids if id ], blocking=[ int(id) for id in blocking_ids if id ], blockedby=[ int(id) for id in blockedby_ids if id ], append=append)
        return


class FormTicketConfig(FormTickets):
    """Form component to update ticket config"""
    formname = [
     'configtck', 'tcktype', 'tckseverity', 'tckpromptuser',
     'tckcomponent', 'tckmilestone', 'tckversion', 'tckparent',
     'tckblockedby', 'tckblocking', 'tcksummary', 'tckdescription']

    def submitform(self, request, c, **kwargs):
        """update ticket config"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        tck_typename = request.POST.get('tck_typename', None)
        tck_severityname = request.POST.get('tck_severityname', None)
        promptuser = request.POST.get('promptuser', None)
        component_ids = request.POST.getall('component_id')
        milestone_ids = request.POST.getall('milestone_id')
        version_ids = request.POST.getall('version_id')
        parent_id = request.POST.get('parent_id', None)
        blocking_ids = request.POST.get('blocking_ids', None)
        blockedby_ids = request.POST.get('blockedby_ids', None)
        summary = request.POST.get('summary', None)
        description = request.POST.get('description', None)
        append = kwargs.get('append', False)
        tck_typename = tck_typename or None
        tck_severityname = tck_severityname or None
        promptuser = promptuser or None
        component_ids = component_ids or None
        milestone_ids = milestone_ids or None
        version_ids = version_ids or None
        try:
            if isinstance(blocking_ids, (str, unicode)):
                ids = blocking_ids.split(',')
                blocking_ids = [ int(id) for id in [ id.strip(' ') for id in ids ] if id ]
        except:
            blocking_ids = None

        try:
            if isinstance(blockedby_ids, (str, unicode)):
                ids = blockedby_ids.split(',')
                blockedby_ids = [ int(id) for id in [ id.strip(' ') for id in ids ] if id ]
        except:
            blockedby_ids = None

        try:
            parent_id = parent_id and int(parent_id)
        except:
            parent_id = None

        if ticket_id:
            tckcomp.config_ticket(int(ticket_id), type=tck_typename, severity=tck_severityname, promptuser=promptuser, parent=parent_id, components=component_ids and [ int(id) for id in component_ids if id ], milestones=milestone_ids and [ int(id) for id in milestone_ids if id ], versions=version_ids and [ int(id) for id in version_ids if id ], blocking=blocking_ids, blockedby=blockedby_ids, append=append)
        if project_id and ticket_id and (summary != None or description != None):
            t = tckcomp.get_ticket(int(ticket_id))
            summary = summary or t.summary
            ticket_id = int(ticket_id)
            project_id = int(project_id)
            tckdetail = [t.id, summary, description, t.type, t.severity]
            tckcomp.create_ticket(project_id, tckdetail, t.promptuser, update=True)
        return


class FormTicketFavorite(FormTickets):
    """Form component to add or remove a ticket being a user's favourite"""
    formname = 'tckfav'

    def submitform(self, request, c, **kwargs):
        """add / remove ticket favourite"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        addfavuser = request.POST.get('addfavuser', None)
        delfavuser = request.POST.get('delfavuser', None)
        if addfavuser and ticket_id:
            tckcomp.addfavorites(int(ticket_id), addfavuser)
        if delfavuser and ticket_id:
            tckcomp.delfavorites(int(ticket_id), delfavuser)
        return


class FormTicketVote(FormTickets):
    """Form component to vote for/against ticket"""
    formname = 'votetck'

    def submitform(self, request, c, **kwargs):
        """vote ticket"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        votedas = request.POST.get('votedas', None)
        if votedas == 'up':
            tckcomp.voteup(int(ticket_id), int(user_id))
        elif votedas == 'down':
            tckcomp.votedown(int(ticket_id), int(user_id))
        return


class FormCreateTicketStatus(FormTickets):
    """Form component to create / update ticket status"""
    formname = 'createtstat'

    def submitform(self, request, c, **kwargs):
        """create / update ticket status"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        ticket_status_id = request.POST.get('ticket_status_id', None)
        tck_statusname = request.POST.get('tck_statusname', None)
        due_date = request.POST.get('due_date', None)
        owner = request.POST.get('owner', None)
        errmsg = ''
        errmsg += not tck_statusname and 'tck_statusname, ' or ''
        errmsg += not owner and 'owner, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        if due_date:
            usertz = timezone(userscomp.get_user(int(user_id)).timezone)
            due_date = h.usertz_2_utc(dt.datetime.strptime(due_date, '%Y-%m-%d'), usertz)
        tckstatdetail = [
         None, tck_statusname, due_date]
        ticket_id = int(ticket_id)
        if ticket_id:
            owner = int(owner)
            t = tckcomp.get_ticket(ticket_id)
            ts = tckcomp.get_ticket_status(t.tsh_id, attrload=['status'])
            if ticket_status_id:
                tckstatdetail[0] = int(ticket_status_id)
                tckcomp.create_ticket_status(ticket_id, tckstatdetail, owner, update=True)
            elif ts.status.tck_statusname == tck_statusname and due_date != None:
                tckstatdetail[0] = ts.id
                tckcomp.create_ticket_status(ticket_id, tckstatdetail, owner, update=True)
            elif tck_statusname:
                ts = tckcomp.create_ticket_status(ticket_id, tckstatdetail, owner)
        return


class FormTicketStatusConfig(FormTickets):
    """Form component to update ticket-status config"""
    formname = ['configtstat', 'tststatus', 'tstduedate']

    def submitform(self, request, c, **kwargs):
        """update ticket-status config"""
        userscomp = self.compmgr.config['userscomp']
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        ticket_status_id = request.POST.get('ticket_status_id', None)
        tck_statusname = request.POST.get('tck_statusname', None)
        due_date = request.POST.get('due_date', None)
        owner = request.POST.get('owner', None)
        tck_statusname = tck_statusname or None
        owner = owner and int(owner)
        if due_date:
            usertz = timezone(userscomp.get_user(int(user_id)).timezone)
            due_date = h.usertz_2_utc(dt.datetime.strptime(due_date, '%Y-%m-%d'), usertz)
        if ticket_id and ticket_status_id:
            ts = tckcomp.get_ticket_status(int(ticket_status_id))
            tckstatdetail = [ts.id, tck_statusname or ts.status, due_date]
            tckcomp.create_ticket_status(int(ticket_id), tckstatdetail, owner or ts.owner, update=True)
        return


class FormCreateTicketComment(FormTickets):
    """Form component to create / update ticket-comment"""
    formname = [
     'createtcmt', 'replytcmt', 'updatetcmt']

    def submitform(self, request, c, **kwargs):
        """create / update ticket-comment"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        ticket_comment_id = request.POST.get('ticket_comment_id', None)
        text = request.POST.get('text', None)
        commentby = request.POST.get('commentby', None)
        replytocomment_id = request.POST.get('replytocomment_id', None)
        errmsg = ''
        errmsg += not text and 'text, ' or ''
        errmsg += not commentby and 'commentby, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        tckcomment = [
         None, text, commentby]
        if ticket_id and ticket_comment_id:
            ticket_comment_id = int(ticket_comment_id)
            tckcomment[0] = ticket_comment_id
            tckcomp.create_ticket_comment(int(ticket_id), tckcomment, update=True)
        elif ticket_id:
            tc = tckcomp.create_ticket_comment(int(ticket_id), tckcomment)
            ticket_comment_id = tc.id
        replytocomment_id = replytocomment_id and int(replytocomment_id)
        if ticket_comment_id and replytocomment_id:
            tckcomp.comment_reply(ticket_comment_id, replytocomment_id)
        return


class FormTicketFilter(FormTickets):
    """Form component to add /remove ticket filters"""
    formname = [
     'addtckfilter', 'deltckfilter']

    def submitform(self, request, c, **kwargs):
        """add / remove ticket filters"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        name = request.POST.get('name', None)
        filterbyjson = request.POST.get('filterbyjson', None)
        tf_id = request.POST.get('tf_id', None)
        userid = int(user_id)
        if name and filterbyjson and formname == 'addtckfilter':
            tckcomp.create_ticketfilter(name=name, filterbyjson=filterbyjson, foruser=userid, byuser=userid)
        if formname == 'deltckfilter':
            tckcomp.del_ticketfilter(tfs=[int(tf_id)], byuser=userid)
        return


class FormTicketTags(FormTickets):
    """Form component to add / remove tags"""
    formname = [
     'addtcktags', 'deltcktags']

    def submitform(self, request, c, **kwargs):
        """add / remove ticket tags"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        if ticket_id and formname == 'addtcktags':
            t = tckcomp.get_ticket(int(ticket_id))
            tckcomp.add_tags(t, tagnames)
        if ticket_id and formname == 'deltcktags':
            t = tckcomp.get_ticket(int(ticket_id))
            tckcomp.remove_tags(t, tagnames)
        return


class FormTicketAttachs(FormTickets):
    """Form component to add / remove attachments"""
    formname = [
     'addtckattachs', 'deltckattachs']

    def submitform(self, request, c, **kwargs):
        """add / remove ticket attachments"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        ticket_id = request.POST.get('ticket_id', None)
        user = kwargs.get('user', None)
        if ticket_id and formname == 'deltckattachs':
            [ tckcomp.remove_attach(int(ticket_id), int(attach_id)) for attach_id in request.POST.getall('attach_id') ]
        elif ticket_id and formname == 'addtckattachs' and user:
            for attachfile in request.POST.getall('attachfile'):
                a = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
                tckcomp.add_attach(int(ticket_id), a)

        return


class FormReviews(Component):
    """Form component to create / update / delete review tables"""

    def requestform(self, request, c, **kwargs):
        """Populate context for review forms"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / Update / Delete entries in review tables"""
        pass


class FormReviewSet(FormReviews):
    """Form component to create / update review set"""
    formname = [
     'createrset', 'updaterset', 'addtorset', 'delfromrset']

    def submitform(self, request, c, **kwargs):
        """create / update review sets. Add / remove review in review set"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        review_id = request.POST.getall('review_id')
        rset_id = request.POST.get('rset_id', None)
        name = request.POST.get('name', None)
        if formname in ('createrset', 'updaterset'):
            if name and rset_id:
                rset = revcomp.get_reviewset(int(rset_id))
                rset and revcomp.update_reviewset(rset, name)
            elif name and project_id:
                proj = projcomp.get_project(int(project_id))
                proj and revcomp.create_reviewset(proj, name)
        elif formname == 'addtorset' and review_id and rset_id:
            review = revcomp.get_review(int(review_id[0]))
            rset = revcomp.get_reviewset(int(rset_id))
            revcomp.add_reviewtoset(rset, review)
        elif formname == 'delfromrset' and review_id and rset_id:
            review = revcomp.get_review(int(review_id[0]))
            rset = revcomp.get_reviewset(int(rset_id))
            review.reviewset == rset and revcomp.remove_reviewfromset(review)
        return


class FormCreateReview(FormReviews):
    """Form component to create / update review"""
    formname = [
     'createrev', 'configrev', 'revwauthor', 'revwmoderator']

    def submitform(self, request, c, **kwargs):
        """create / update review"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        review_ids = request.POST.getall('review_id')
        resource_urls = request.POST.getall('resource_url')
        version = request.POST.get('version', None)
        version = version and int(version)
        author = request.POST.get('author', None)
        moderator = request.POST.get('moderator', None)
        participants = request.POST.getall('participant')
        rset_id = request.POST.get('rset_id')
        append = kwargs.get('append', True)
        if formname == 'createrev':
            errmsg = ''
            errmsg += not resource_urls and 'resource_url, ' or ''
            errmsg += not version and 'version, ' or ''
            errmsg += not author and 'author, ' or ''
            errmsg += not moderator and 'moderator, ' or ''
            if errmsg:
                errmsg = 'Check ' + errmsg + '!!'
                raise ZetaFormError(errmsg)
            h.validate_fields(request)
        rset = rset_id and revcomp.get_reviewset(int(rset_id))
        if project_id and len(review_ids) == 1 and len(resource_urls) == 1:
            revdetail = [
             int(review_ids[0]), resource_urls[0], version, author,
             moderator]
            r = revcomp.create_review(int(project_id), revdetail, update=True)
            participants and revcomp.set_participants(int(review_ids[0]), participants, append=append)
            r and rset and revcomp.add_reviewtoset(rset, r)
        elif project_id and review_ids:
            for rid in review_ids:
                revdetail = [
                 int(rid), None, version, author, moderator]
                r = revcomp.create_review(int(project_id), revdetail, update=True)
                participants and revcomp.set_participants(int(rid), participants, append=append)
                r and rset and revcomp.add_reviewtoset(rset, r)

        elif project_id and resource_urls:
            for rurl in resource_urls:
                revdetail = [
                 None, rurl, version, author, moderator]
                r = revcomp.create_review(int(project_id), revdetail)
                participants and revcomp.set_participants(r, participants, append=append)
                r and rset and revcomp.add_reviewtoset(rset, r)

        return


class FormReviewParticipants(FormReviews):
    """Form component to update review"""
    formname = ['addparts', 'delparts']

    def submitform(self, request, c, **kwargs):
        """update review"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        review_id = request.POST.get('review_id', None)
        participants = request.POST.getall('participant')
        append = kwargs.get('append', True)
        if review_id and participants:
            if formname == 'addparts':
                revcomp.set_participants(int(review_id), participants, append=append)
            elif formname == 'delparts':
                revcomp.set_participants(int(review_id), participants, remove=True)
        return


class FormCloseReview(FormReviews):
    """Form component to close review"""
    formname = 'closerev'

    def submitform(self, request, c, **kwargs):
        """close review"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        review_id = request.POST.get('review_id', None)
        command = request.POST.get('command')
        if command == 'open':
            close = False
            rc = revcomp.close_review(int(review_id), close=close)
        elif command == 'close':
            close = True
            rc = revcomp.close_review(int(review_id), close=close)
        else:
            raise ZetaFormError("Unknow 'closerev' command")
        if rc != close:
            raise ZetaFormError('Cannot close review, check whether ' + 'all review comments are approved')
        return


class FormCreateReviewComment(FormReviews):
    """Form component to create / update review"""
    formname = [
     'creatercmt', 'replyrcmt']

    def submitform(self, request, c, **kwargs):
        """create / update review"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        review_id = request.POST.get('review_id', None)
        review_comment_id = request.POST.get('review_comment_id', None)
        position = request.POST.get('position', None)
        text = request.POST.get('text', None)
        nature = request.POST.get('reviewnature', None)
        commentby = request.POST.get('commentby', None)
        replytocomment_id = request.POST.get('replytocomment_id', None)
        errmsg = ''
        errmsg += not text and 'text, ' or ''
        errmsg += not commentby and 'commentby, ' or ''
        errmsg += formname == 'creatercmt' and not position and 'position, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        revcomment = [
         None, position, text, commentby, nature, None]
        if review_id and review_comment_id:
            revcomment[0] = int(review_comment_id)
            revcomp.create_reviewcomment(int(review_id), revcomment, update=True)
        elif review_id:
            rc = revcomp.create_reviewcomment(int(review_id), revcomment)
            review_comment_id = rc.id
        replytocomment_id = replytocomment_id and int(replytocomment_id)
        if review_comment_id and replytocomment_id:
            revcomp.comment_reply(review_comment_id, replytocomment_id)
        return


class FormProcessReviewComment(FormReviews):
    """Form component to approve review comment"""
    formname = 'processrcmt'

    def submitform(self, request, c, **kwargs):
        """process (action/approve) review comment"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        review_id = request.POST.get('review_id', None)
        review_comment_id = request.POST.get('review_comment_id', None)
        approve = request.POST.get('approve', None)
        reviewnature = request.POST.get('reviewnature', None)
        reviewaction = request.POST.get('reviewaction', None)
        if approve != None:
            if approve == 'true':
                approve = True
            elif approve == 'false':
                approve = False
            else:
                approve = None
        if review_comment_id:
            revcomp.process_reviewcomment(int(review_comment_id), reviewnature=reviewnature, reviewaction=reviewaction, approve=approve)
        return


class FormReviewFavorite(FormReviews):
    """Form component to add or remove a review being a user's favourite"""
    formname = 'revwfav'

    def submitform(self, request, c, **kwargs):
        """add / remove review favourite"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        review_id = request.POST.get('review_id', None)
        addfavuser = request.POST.get('addfavuser', None)
        delfavuser = request.POST.get('delfavuser', None)
        if addfavuser and review_id:
            revcomp.addfavorites(int(review_id), addfavuser)
        if delfavuser and review_id:
            revcomp.delfavorites(int(review_id), delfavuser)
        return


class FormReviewTags(FormReviews):
    """Form component to add / remove Review tags"""
    formname = [
     'addrevtags', 'delrevtags']

    def submitform(self, request, c, **kwargs):
        """add / remove review tags"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        review_id = request.POST.get('review_id', None)
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        if review_id and formname == 'addrevtags':
            revcomp.add_tags(int(review_id), tagnames)
        if review_id and formname == 'delrevtags':
            revcomp.remove_tags(int(review_id), tagnames)
        return


class FormReviewAttachs(FormReviews):
    """Form component to add / remove review attachments"""
    formname = [
     'addrevattachs', 'delrevattachs']

    def submitform(self, request, c, **kwargs):
        """add / remove review attachments"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        review_id = request.POST.get('review_id', None)
        user = kwargs.get('user', None)
        if review_id and formname == 'delrevattachs':
            [ revcomp.remove_attach(int(review_id), int(attach_id)) for attach_id in request.POST.getall('attach_id') ]
        elif review_id and formname == 'addrevattachs' and user:
            for attachfile in request.POST.getall('attachfile'):
                a = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
                revcomp.add_attach(int(review_id), a)

        return


class FormVcs(Component):
    """Form component to create / update / delete vcs tables"""

    def requestform(self, request, c, **kwargs):
        """Populate context for vcs forms"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / Update / Delete entries in vcs tables"""
        pass


class FormCreateVcs(FormVcs):
    """Form component to create / update / delete vcs"""
    formname = 'createvcs'

    def submitform(self, request, c, **kwargs):
        """create vcs"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        vcs_typename = request.POST.get('vcs_typename', None)
        name = request.POST.get('name', None)
        rooturl = request.POST.get('rooturl', None)
        loginname = request.POST.get('loginname', None)
        password = request.POST.get('password', None)
        errmsg = ''
        errmsg += not name and 'repository name, ' or ''
        errmsg += not vcs_typename and 'repository type, ' or ''
        errmsg += not rooturl and 'root url, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        if project_id:
            vcsdetail = (
             vcs_typename, name, rooturl, loginname, password)
            v = vcscomp.create_vcs(int(project_id), vcsdetail, byuser=int(user_id))
        else:
            raise ZetaFormError('Project not defined')
        return


class FormConfigVcs(FormVcs):
    """Form component to configure existing vcs entry"""
    formname = 'configvcs'

    def submitform(self, request, c, **kwargs):
        """config vcs"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        vcs_id = request.POST.get('vcs_id', None)
        vcs_typename = request.POST.get('vcs_typename', None)
        name = request.POST.get('name', None)
        rooturl = request.POST.get('rooturl', None)
        loginname = request.POST.get('loginname', None)
        password = request.POST.get('password', None)
        if vcs_id:
            vcscomp.config_vcs(int(vcs_id), name=name, type=vcs_typename, rooturl=rooturl, loginname=loginname, password=password, byuser=int(user_id))
        return


class FormDeleteVcs(FormVcs):
    """Form component to delete vcs"""
    formname = [
     'deletevcs']

    def submitform(self, request, c, **kwargs):
        """delete vcs"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        vcs_id = request.POST.get('vcs_id', None)
        if project_id and vcs_id:
            vcscomp.delete_vcs(int(vcs_id))
        return


class FormCreateVcsmount(FormVcs):
    """Form component to create a repository mount"""
    formname = [
     'createmount']

    def submitform(self, request, c, **kwargs):
        """Create repository mount"""
        user_id = request.POST.get('user_id', None)
        vcs_id = request.POST.get('vcs_id', None)
        name = request.POST.get('name', None)
        repospath = request.POST.get('repospath', None)
        content = request.POST.get('content', None)
        errmsg = ''
        errmsg += not vcs_id and 'vcs_id, ' or ''
        errmsg += not name and 'name, ' or ''
        errmsg += not repospath and 'repospath, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        vcs_id = int(vcs_id)
        if user_id and vcs_id and name and repospath:
            if content:
                m = vcscomp.create_mount(vcs_id, name, repospath, content)
            else:
                m = vcscomp.create_mount(vcs_id, name, repospath)
        return


class FormUpdateVcsmount(FormVcs):
    """Form component to update repository mount"""
    formname = ['updatemount']

    def submitform(self, request, c, **kwargs):
        """Update repository mount"""
        user_id = request.POST.get('user_id', None)
        mount_id = request.POST.get('mount_id', None)
        name = request.POST.get('name', None)
        repospath = request.POST.get('repospath', None)
        content = request.POST.get('content', None)
        m = mount_id and vcscomp.get_mount(int(mount_id))
        kwargs = {}
        name and kwargs.setdefault('name', name)
        repospath and kwargs.setdefault('repospath', repospath)
        content and kwargs.setdefault('content', content)
        m and vcscomp.update_mount(m, **kwargs)
        return


class FormDeleteVcsmount(FormVcs):
    """Form component to delete repository mount"""
    formname = [
     'deletemount']

    def submitform(self, request, c, **kwargs):
        """Delete repository mount"""
        user_id = request.POST.get('user_id', None)
        mount_id = request.POST.get('mount_id', None)
        mount_id and vcscomp.delete_mount(int(mount_id))
        return


class FormWikis(Component):
    """Form component to create / update / delete wiki tables"""

    def requestform(self, request, c, **kwargs):
        """Populate context for wiki forms"""
        pass

    def submitform(self, request, c, **kwargs):
        """Create / Update / Delete entries in wiki tables"""
        pass


class FormCreateWiki(FormWikis):
    """Form component to create wiki"""
    formname = 'createwiki'

    def submitform(self, request, c, **kwargs):
        """create wiki"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wikiurl = request.POST.get('wikiurl', None)
        wiki_typename = request.POST.get('wiki_typename', None)
        creator = request.POST.get('creator', None)
        errmsg = ''
        errmsg += not wikiurl and 'wikiurl, ' or ''
        errmsg += not wiki_typename and 'wiki_typename, ' or ''
        errmsg += not creator and 'creator, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        if wikicomp.get_wiki(wikiurl):
            raise ZetaFormError('wiki page with url `%s` already exists !!')
        w = wikicomp.create_wiki(wikiurl, wiki_typename, creator=creator)
        project_id and wikicomp.config_wiki(w, project=int(project_id))
        return


class FormConfigWiki(FormWikis):
    """Form component to configure a wiki page"""
    formname = [
     'configwiki', 'wikitype', 'wikisummary']

    def submitform(self, request, c, **kwargs):
        """configure a wiki page"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        wiki_typename = request.POST.get('wiki_typename', None)
        summary = request.POST.get('summary', None)
        append = kwargs.get('append', False)
        wiki_id = int(wiki_id)
        wiki_typename and wikicomp.config_wiki(wiki_id, type=wiki_typename)
        summary and wikicomp.config_wiki(wiki_id, summary=summary)
        project_id and wikicomp.config_wiki(wiki_id, project=int(project_id))
        return


class FormWikiFavorite(FormWikis):
    """Form component to add or remove a wiki being a user's favourite"""
    formname = 'wikifav'

    def submitform(self, request, c, **kwargs):
        """add / remove wiki favourite"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        addfavuser = request.POST.get('addfavuser', None)
        delfavuser = request.POST.get('delfavuser', None)
        if addfavuser and wiki_id:
            wikicomp.addfavorites(int(wiki_id), addfavuser)
        if delfavuser and wiki_id:
            wikicomp.delfavorites(int(wiki_id), delfavuser)
        return


class FormWikiVote(FormWikis):
    """Form component to vote for/against wiki"""
    formname = 'votewiki'

    def submitform(self, request, c, **kwargs):
        """vote wiki"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        votedas = request.POST.get('votedas', None)
        if votedas == 'up':
            wikicomp.voteup(int(wiki_id), int(user_id))
        elif votedas == 'down':
            wikicomp.votedown(int(wiki_id), int(user_id))
        return


class FormWikiContent(FormWikis):
    """Form component to create / update wiki page content"""
    formname = 'wikicont'

    def submitform(self, request, c, **kwargs):
        """create / update wiki page content"""
        user_id = request.POST.get('user_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        text = request.POST.get('text', None)
        author = request.POST.get('author', None)
        version_id = request.POST.get('version_id', None)
        errmsg = ''
        errmsg += not text and 'text, ' or ''
        errmsg += not author and 'author, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        version_id = version_id and int(version_id)
        if wiki_id:
            wikicomp.create_content(int(wiki_id), author, text, version_id)
        return


class FormRemoveWikiContent(FormWikis):
    """Form component to remove a wiki page version"""
    formname = 'rmwikicont'

    def submitform(self, request, c, **kwargs):
        """remove a wiki page content"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        version_id = request.POST.get('version_id', None)
        errmsg = ''
        errmsg += not version_id and 'version_id, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        if wiki_id:
            wikicomp.remove_content(int(wiki_id), int(version_id))
        return


class FormWikiRedirect(FormWikis):
    """Form component to redirect wiki page"""
    formname = 'wikiredir'

    def submitform(self, request, c, **kwargs):
        """redirect wiki page"""
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        wiki_target = request.POST.get('wiki_target', None)
        if wiki_id and wiki_target:
            wikicomp.wiki_redirect(int(wiki_id), int(wiki_target))
        return


class FormCreateWikiComment(FormWikis):
    """Form component to create / update wiki-comment"""
    formname = [
     'createwcmt', 'updatewcmt', 'replywcmt']

    def submitform(self, request, c, **kwargs):
        """create / update wiki-comment"""
        user_id = request.POST.get('user_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        wiki_comment_id = request.POST.get('wiki_comment_id', None)
        version_id = request.POST.get('version_id', None)
        text = request.POST.get('text', None)
        commentby = request.POST.get('commentby', None)
        replytocomment_id = request.POST.get('replytocomment_id', None)
        errmsg = ''
        errmsg += not text and 'text, ' or ''
        errmsg += not commentby and 'commentby, ' or ''
        errmsg += not version_id and 'version_id, ' or ''
        if errmsg:
            errmsg = 'Check ' + errmsg + '!!'
            raise ZetaFormError(errmsg)
        h.validate_fields(request)
        wcmtdetail = [
         None, commentby, int(version_id), text]
        if wiki_id and wiki_comment_id:
            wiki_comment_id = int(wiki_comment_id)
            wcmtdetail[0] = wiki_comment_id
            wikicomp.create_wikicomment(int(wiki_id), wcmtdetail, update=True)
        elif wiki_id:
            wc = wikicomp.create_wikicomment(int(wiki_id), wcmtdetail)
            wiki_comment_id = wc.id
        replytocomment_id = replytocomment_id and int(replytocomment_id)
        if wiki_comment_id and replytocomment_id:
            wikicomp.comment_reply(wiki_comment_id, replytocomment_id)
        return


class FormWikiTags(FormWikis):
    """Form component to add / remove wiki tags"""
    formname = [
     'addwikitags', 'delwikitags']

    def submitform(self, request, c, **kwargs):
        """add / remove wiki tags"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        tagnames = list(set(h.parse_csv(request.POST.get('tags', ''))))
        if wiki_id and formname == 'addwikitags':
            w = wikicomp.get_wiki(int(wiki_id))
            wikicomp.add_tags(w, tagnames)
        if wiki_id and formname == 'delwikitags':
            w = wikicomp.get_wiki(int(wiki_id))
            wikicomp.remove_tags(w, tagnames)
        return


class FormWikiAttachs(FormWikis):
    """Form component to add / remove wiki attachments"""
    formname = [
     'addwikiattachs', 'delwikiattachs']

    def submitform(self, request, c, **kwargs):
        """add / remove wiki attachments"""
        formname = request.params.get('formname', None)
        user_id = request.POST.get('user_id', None)
        project_id = request.POST.get('project_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        user = kwargs.get('user', None)
        if wiki_id and formname == 'delwikiattachs':
            [ wikicomp.remove_attach(int(wiki_id), int(attach_id)) for attach_id in request.POST.getall('attach_id') ]
        elif wiki_id and formname == 'addwikiattachs' and user:
            for attachfile in request.POST.getall('attachfile'):
                a = attcomp.create_attach(attachfile.filename, fdfile=attachfile.file, uploader=user)
                wikicomp.add_attach(int(wiki_id), a)

        return


class FormWikiDiff(FormWikis):
    """Form component to generate the difference between wiki versions.
    This component does not commit anything to the database."""
    formname = 'wikidiff'

    def submitform(self, request, c, **kwargs):
        """Generate the difference between wiki versions"""
        user_id = request.POST.get('user_id', None)
        wiki_id = request.POST.get('wiki_id', None)
        oldver = request.POST.get('oldver', None)
        newver = request.POST.get('newver', None)
        c.oldver = oldver and int(oldver)
        c.newver = newver and int(newver)
        return