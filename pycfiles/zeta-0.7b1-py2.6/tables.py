# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/model/tables.py
# Compiled at: 2010-06-12 02:51:03
"""Contains Python Class objects mappable to database tables. 

This module should contain only class definitions for Object Mapper, and all
the class definitions must be added to __all__, so that it is possible to
gather all the Class object with an `import *` """
from datetime import datetime
from sqlalchemy.orm import relation, validates, reconstructor
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import Integer, String, Unicode, Binary, PickleType, DateTime, TIMESTAMP
from zeta.model import meta
from zeta.model.meta import *
import zeta.lib.helpers as h
from zeta.lib.constants import *
from zeta.lib.error import *
__all__ = [
 'System', 'StaticWiki', 'PermissionName', 'PermissionGroup',
 'UserRelation_Type', 'User', 'UserInfo', 'UserRelation',
 'Tag', 'Attachment', 'License', 'Vote',
 'ProjectTeam_Type', 'Project', 'ProjectInfo', 'MailingList', 'IRCChannel',
 'PrjComponent', 'Milestone', 'Version', 'ProjectPerm', 'ProjectTeam_Perm',
 'ProjectTeam',
 'TicketStatus', 'TicketType', 'TicketSeverity', 'Ticket', 'TicketStatusHistory',
 'TicketComment', 'TicketFilter', 'TicketReference',
 'ReviewComment_Nature', 'ReviewComment_Action', 'Review',
 'ReviewSet', 'ReviewComment',
 'VcsType', 'Vcs', 'VcsMount',
 'WikiType', 'Wiki', 'WikiTable_Map', 'WikiComment', 'wikipage_factory',
 'Timeline', 'UserInvitation', 'Survey']

class System(object):
    """Class object to model system table."""

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __repr__(self):
        return "<System Entry('%s','%s')>" % (self.field, self.value)

    idlabel = property(lambda self: self.field)


class StaticWiki(object):
    """Class object to model staticwiki table."""

    def __init__(self, path, text):
        self.path = path
        self.text = text
        self.translate = h.hitch(self, StaticWiki, h.translate, cacheattr='text')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, StaticWiki, h.translate, cacheattr='text')

    def __repr__(self):
        return "<StaticWiki Entry('%s')>" % self.path

    idlabel = property(lambda self: self.path)


class PermissionName(object):
    """Class Object to model permission_name table.
    
    perm_name, permission name should all be in UPPER case. If not, it will be
               converted to upper case before storing into the database.
    """

    def __init__(self, perm_name):
        self.perm_name = perm_name

    def __repr__(self):
        return "<PermissionName('%s')>" % self.perm_name

    idlabel = property(lambda self: self.perm_name)


class PermissionGroup(object):
    """Class Object to model permission_group table.
    
    perm_group, permission group name should all be in lower case. If not, it
                will be converted to lower case before storing it. The data 
                base will not.
    """

    def __init__(self, perm_group):
        self.perm_group = perm_group

    def __repr__(self):
        return "<PermissionGroup('%s','%s')>" % (self.perm_group, self.perm_names)

    idlabel = property(lambda self: self.perm_group)


class UserRelation_Type(object):
    """Class object to model userrelation_type table.
    
    userrel_type Type of relation between two different user.
    """

    def __init__(self, userrel_type):
        self.userrel_type = userrel_type

    def __repr__(self):
        return "<UserRelation_Type('%s')>" % self.userrel_type

    idlabel = property(lambda self: self.userrel_type)


class User(object):
    """Class object to model user table.

    username should be unique and lower case.
    emailid  should be valid.
    password is the digest password entered by user and processed by the
             browser.
    timezone the timezone user belong to.
    disabled only the site adminstrator can make it True.
    """

    def __init__(self, username, emailid, password, timezone, disabled=False):
        self.username = username
        self.emailid = emailid
        self.password = password
        self.timezone = timezone
        self.disabled = disabled

    def __repr__(self):
        return "<User('%s','%s','%s','%s','%s')>" % (self.username, self.emailid, self.password,
         self.timezone, self.disabled)

    idlabel = property(lambda self: self.username)


class UserInfo(object):
    """Class object to model user_info table.
   
    firstname, middlename and lastname are mandatory, while,
    addressline1&2, city, pincode, state and country are optional.
    """

    def __init__(self, firstname=None, middlename=None, lastname=None, addressline1=None, addressline2=None, city=None, pincode=None, state=None, country=None, userpanes=None):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.addressline1 = addressline1
        self.addressline2 = addressline2
        self.city = city
        self.pincode = pincode
        self.state = state
        self.country = country
        if userpanes:
            self.userpanes = userpanes

    def __repr__(self):
        return "<UserInfo('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
         self.firstname, self.middlename, self.lastname,
         self.addressline1, self.addressline2, self.city,
         self.pincode, self.state, self.country)

    idlabel = property(lambda self: (', ').join([self.firstname,
     self.middlename,
     self.lastname]))


class UserRelation(object):
    """Class object to model user_relation table."""

    def __init__(self):
        pass

    def __repr__(self):
        return "<UserRelation>('%s','%s','%s')" % (self.userreltype, self.userfrom,
         self.userto)

    idlabel = property(lambda self: '%s, %s, %s' % (
     self.userreltype, self.userfrom,
     self.userto))


class Tag(object):
    """Class object to model tag table.

    tag, tagname 
    """

    def __init__(self, tagname):
        self.tagname = tagname

    def __repr__(self):
        return '%s' % self.tagname

    idlabel = property(lambda self: self.tagname)


class Attachment(object):
    """Class object to model attachment table.

    filename,       which can only be a filename and path relative to
                    environment path.
    summary,        an optional one line summary to explain the attachment.
    download_count, Number of times the attachment is downloaded.
    """

    def __init__(self, filename, download_count, summary=''):
        self.filename = filename
        self.download_count = download_count
        self.summary = summary

    def __repr__(self):
        return '%s' % self.filename

    idlabel = property(lambda self: self.filename)


class License(object):
    """Class object to model license table.

    licensename, a short name to identify the license
    summary,     a one line description of the license
    text,        a detailed specification of the license
    source,      who is the author of the license
    """

    def __init__(self, licensename, summary, text, source):
        self.licensename = licensename
        self.summary = summary
        self.text = text
        self.source = source
        self.translate = h.hitch(self, License, h.translate, cacheattr='text')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, License, h.translate, cacheattr='text')

    def __repr__(self):
        return "<License('%s,%s,%s,%s,%s')>" % (self.licensename, self.summary, self.text, self.source,
         self.created_on)

    idlabel = property(lambda self: self.licensename)


class Vote(object):
    """Class object to model vote table.

    votefor,    string specifying the voted for candidate
    medium,     string specifying how the vote was casted,
                allowable medium,
                    web, sms, phone"""

    def __init__(self, votedas='', medium='web'):
        self.votedas = votedas
        self.medium = medium

    def __repr__(self):
        return "<Vote('%s,%s')>" % (self.votedas, self.medium)


class ProjectTeam_Type(object):
    """Class object to model projectteam_type table.
    
    team_type Type of team the user belongs to, in a team.
    """

    def __init__(self, team_type):
        self.team_type = team_type

    def __repr__(self):
        return "<ProjectTeam_Type('%s')>" % self.team_type

    idlabel = property(lambda self: self.team_type)


class Project(object):
    """Class object to model project table.
    
    projectname, unique name for the project.
    summary,     one line summary of the project.
    admin_email, administrator email id.
    exposed,     if False, the project is not visible to non project members.
    disabled,   Make the project dormant.
    """

    def __init__(self, projectname, summary, admin_email, exposed=True, disabled=False):
        self.projectname = projectname
        self.summary = summary
        self.admin_email = admin_email
        self.exposed = exposed
        self.disabled = disabled

    def __repr__(self):
        return "<Project('%s,%s,%s,%s,%s')>" % (self.projectname, self.summary,
         self.admin_email, self.exposed, self.disabled)

    idlabel = property(lambda self: self.projectname)


class ProjectInfo(object):
    """Class object to model project_info table.

    description, wiki markup describing the project.
    """

    def __init__(self, description):
        self.description = description
        self.translate = h.hitch(self, ProjectInfo, h.translate, cacheattr='description')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, ProjectInfo, h.translate, cacheattr='description')

    def __repr__(self):
        return "<ProjectInfo('%s')>" % self.description

    idlabel = property(lambda self: self.projectname)


class MailingList(object):
    """Class object to model mailinglist table.
    
    mailing_list, specifies the email-group id.
    """

    def __init__(self, mailing_list):
        self.mailing_list = mailing_list

    def __repr__(self):
        return "<MailingList('%s')>" % self.mailing_list

    idlabel = property(lambda self: self.mailing_list)


class IRCChannel(object):
    """Class object to model ircchannel table.

    ircchannel, specifies the irc-channel id.
    """

    def __init__(self, ircchannel):
        self.ircchannel = ircchannel

    def __repr__(self):
        return "<IRCChannel('%s')>" % self.ircchannel

    idlabel = property(lambda self: self.ircchannel)


class PrjComponent(object):
    """Class object to model component table.

    componentname,  project-wise unique name.
    comp_number,    project-wise unique number.
    """

    def __init__(self, componentname, comp_number, description):
        self.componentname = componentname
        self.comp_number = comp_number
        self.description = description
        self.translate = h.hitch(self, PrjComponent, h.translate, cacheattr='description')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, PrjComponent, h.translate, cacheattr='description')

    def __repr__(self):
        return "<PrjComponent('%s','%s','%s')>" % (self.componentname, self.comp_number,
         self.description)

    idlabel = property(lambda self: self.componentname)


class Milestone(object):
    """Class object to model milestone table.
    
    milestone_name, unique milestone name.
    mstn_number,    project-wise unique milestone number(id).
    description,    wiki markup describing the milestone.
    closing_remark, wiki markup to remark on closed milestones.
    completed,      Milestones can either be completed,
    cancelled,      or cancelled.
    due_date,       Duedate for completion.
    """

    def __init__(self, milestone_name, mstn_number, description, closing_remark='', completed=False, cancelled=False, due_date=None):
        self.milestone_name = milestone_name
        self.mstn_number = mstn_number
        self.description = description
        self.completed = completed
        self.cancelled = cancelled
        self.due_date = due_date
        if closing_remark:
            self.closing_remark = closing_remark
        self.translate = h.hitch(self, Milestone, h.translate, cacheattr='description')
        self.crtranslate = h.hitch(self, Milestone, h.translate, cacheattr='closing_remark')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, Milestone, h.translate, cacheattr='description')
        self.crtranslate = h.hitch(self, Milestone, h.translate, cacheattr='closing_remark')

    def __repr__(self):
        return "<Milestone('%s','%s','%s','%s','%s','%s','%s')>" % (self.milestone_name,
         self.mstn_number, self.description, self.closing_remark, self.completed,
         self.cancelled, self.due_date)

    idlabel = property(lambda self: self.milestone_name)


class Version(object):
    """Class object to model version table.

    version_name, unique version name.
    ver_number,   project-wise unique version number.
    description,  wiki markup describing the project version.
    """

    def __init__(self, version_name, ver_number, description):
        self.version_name = version_name
        self.ver_number = ver_number
        self.description = description
        self.translate = h.hitch(self, Version, h.translate, cacheattr='description')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, Version, h.translate, cacheattr='description')

    def __repr__(self):
        return "<Version('%s','%s','%s')>" % (self.version_name, self.ver_number, self.description)

    idlabel = property(lambda self: self.version_name)


class ProjectPerm(object):
    """Class object to model project_perm table."""

    def __init__(self):
        pass

    def __repr__(self):
        return "<ProjectPerm>('%s','%s','%s')" % (
         self.project.projectname, self.user.username,
         self.permgroup.perm_group)

    idlabel = property(lambda self: 'for user %s, in %s, permission %s' % (
     self.user.username, self.project.projectname,
     self.permgroup.perm_group))


class ProjectTeam_Perm(object):
    """Class object to model projectteam_perm table."""

    def __init__(self):
        pass

    def __repr__(self):
        return "<ProjectTeam_Perm>('%s','%s','%s')" % (
         self.project.projectname, self.teamtype.team_type,
         self.permgroup.perm_group)

    idlabel = property(lambda self: 'for team "%s", in "%s", permission "%s"' % (
     self.teamtype.team_type,
     self.project.projectname,
     self.permgroup.perm_group))


class ProjectTeam(object):
    """Class object to model project_team table."""

    def __init__(self):
        pass

    def __repr__(self):
        return "<ProjectTeam>('%s','%s','%s')" % (
         self.project.projectname, self.teamtype.team_type,
         self.user.username)

    idlabel = property(lambda self: 'user "%s", to team "%s" in %s' % (
     self.user.username, self.teamtype.team_type,
     self.project.projectname))


class TicketStatus(object):
    """Class object to model ticket_status table.
    
    tck_statusname, must be one of the valid status names.
    """

    def __init__(self, tck_statusname):
        self.tck_statusname = tck_statusname

    def __repr__(self):
        return "<TicketStatus('%s')>" % self.tck_statusname

    idlabel = property(lambda self: self.tck_statusname)


class TicketType(object):
    """Class object to model ticket_type table.
    
    tck_typename, must be one of the valid type names.
    """

    def __init__(self, tck_typename):
        self.tck_typename = tck_typename

    def __repr__(self):
        return "<TicketType('%s')>" % self.tck_typename

    idlabel = property(lambda self: self.tck_typename)


class TicketSeverity(object):
    """Class object to model ticket_severity table.

    tck_severityname, must be one of the severity levels.
    """

    def __init__(self, tck_severityname):
        self.tck_severityname = tck_severityname

    def __repr__(self):
        return "<TicketSeverity('%s')>" % self.tck_severityname

    idlabel = property(lambda self: self.tck_severityname)


class Ticket(object):
    """Class object to model ticket table.

    ticket_number, unique ticket number for a given project.
    summary,       one line summary for the ticket.
    description,   Detailed description for the ticket as wiki-markup
    """

    def __init__(self, ticket_number, summary, description):
        self.ticket_number = ticket_number
        self.summary = summary
        self.description = description
        self.translate = h.hitch(self, Ticket, h.translate, cacheattr='description')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, Ticket, h.translate, cacheattr='description')

    def __repr__(self):
        return "<Ticket('%s','%s','%s')>" % (self.id, self.summary,
         self.description)

    idlabel = property(lambda self: 'ticket %s, (%s) ' % (
     self.id, self.summary))


class TicketStatusHistory(object):
    """Class object to model ticket_status_history table.
    
    due_date, should be a valid DateTime object.
    """

    def __init__(self, due_date=None):
        self.due_date = due_date

    def __repr__(self):
        return "<TicketStatusHistory('%s','%s','%s')>" % (
         self.status, self.due_date, self.owner)

    idlabel = property(lambda self: 'for ticket %s status %s owned by %s before %s ' % (
     self.ticket.id, self.status, self.owner,
     self.due_date))


class TicketComment(object):
    """Class object to model ticket_comment table.
    
    text, comment in wiki-markup 
    """

    def __init__(self, text):
        self.text = text
        self.translate = h.hitch(self, TicketComment, h.translate, cacheattr='text')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, TicketComment, h.translate, cacheattr='text')

    def __repr__(self):
        return "<TicketComment('%s','%s')>" % (self.text, self.commentby)

    idlabel = property(lambda self: 'comment "%s" for ticket %s' % (
     self.text, self.ticket.id))


class TicketFilter(object):
    """Class object to model ticket_filter table.

    name,         name of the filter
    filterbyjson, filter map in json format
    """

    def __init__(self, name, filterbyjson, user_id=None):
        self.name = name
        self.filterbyjson = filterbyjson
        if user_id and isinstance(user_id, (int, long)):
            self.user_id = user_id

    def __repr__(self):
        return "<TicketFilter('%s')>" % self.name


class TicketReference(object):
    """Class object to model ticket_reference table.
    
    resource_url, valid resource realm and id.
    """

    def __init__(self, resource_url):
        self.resource_url = resource_url

    def __repr__(self):
        return "<TicketReference('%s')>" % self.resource_url


class ReviewComment_Nature(object):
    """Class object to model reviewcomment_nature table.

    naturename, one of the valid comment 'nature'."""

    def __init__(self, naturename):
        self.naturename = naturename

    def __repr__(self):
        return '%s' % self.naturename

    idlabel = property(lambda self: self.naturename)


class ReviewComment_Action(object):
    """Class object to model reviewcomment_action table.

    actionname, one of the valid action that can be taken on a review comment.
    """

    def __init__(self, actionname):
        self.actionname = actionname

    def __repr__(self):
        return '%s' % self.actionname

    idlabel = property(lambda self: self.actionname)


class ReviewSet(object):
    """Class object to model reviewset table.

    name, reviewset name
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '%s' % self.name

    idlabel = property(lambda self: self.name)


class Review(object):
    """Class object to model review table.

    review_number, unique sequence of number for a ticket.
    closed,        True if all the review comments are acted upon and approved
                   by moderator
    """

    def __init__(self, resource_url, version, review_number, closed=False):
        self.review_number = review_number
        self.resource_url = resource_url
        self.version = version
        self.closed = closed

    def __repr__(self):
        return "for '%s' version '%s' status %s" % (
         self.resource_url, self.version,
         self.closed and 'closed' or 'open')

    idlabel = property(lambda self: 'for %s version %s status %s' % (
     self.resource_url, self.version,
     self.closed and 'closed' or 'open'))


class ReviewComment(object):
    """Class object to model review_comment table.
    
    position, based on the review material, position identifies the portion to
              which the review comment is applicable.
    text,     plain text to describe the review comment.
    approved, Can be done only by the moderator.
    """

    def __init__(self, position, text, approved=False):
        self.position = position
        self.text = text
        self.approved = approved
        self.translate = h.hitch(self, ReviewComment, h.translate, cacheattr='text')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, ReviewComment, h.translate, cacheattr='text')

    def __repr__(self):
        return "<ReviewComment('%s','%s','%s')>" % (self.position, self.text, self.approved)

    idlabel = property(lambda self: self.text)


class VcsType(object):
    """Class object to model vcs_type table.
    
    vcs_typename, must be one of the valid vcs type names.
    """

    def __init__(self, vcs_typename):
        self.vcs_typename = vcs_typename

    def __repr__(self):
        return "<VcsType('%s')>" % self.vcs_typename

    idlabel = property(lambda self: self.vcs_typename)


class VcsMount(object):
    """Class object to model vcsmount table."""

    def __init__(self, name, repospath, content='html'):
        self.name = name
        self.repospath = repospath
        self.content = content

    def __repr__(self):
        return "<VcsMount('%s','%s')>" % (self.name, self.repospath)

    idlabel = property(lambda self: self.name)


class Vcs(object):
    """Class object to model vcs table."""

    def __init__(self, name, rooturl, loginname='', password=''):
        self.name = name
        self.rooturl = rooturl
        self.loginname = loginname
        self.password = password

    def __repr__(self):
        return "<Vcs('%s','%s')>" % (self.name, self.rooturl)

    idlabel = property(lambda self: self.name)


class WikiType(object):
    """Class object to model wiki_type table.
    
    wiki_typename, must be one of the valid wiki type names.
    """

    def __init__(self, wiki_typename):
        self.wiki_typename = wiki_typename

    def __repr__(self):
        return "<WikiType('%s')>" % self.wiki_typename

    idlabel = property(lambda self: self.wiki_typename)


class Wiki(object):
    """Class object to model wiki table.
    
    wikiurl,        Entire path, query and fragment sting in the URI.
    latest_version, Id in WikiPage pointing to the latest version of the page.
    """

    def __init__(self, wikiurl, summary, latest_version):
        self.wikiurl = wikiurl
        self.summary = summary
        self.latest_version = latest_version

    def __repr__(self):
        return "<Wiki('%s','%s','%s')>" % (self.wikiurl, self.summary,
         self.latest_version)

    idlabel = property(lambda self: self.wikiurl)


class WikiTable_Map(object):
    """Class object to model wikitable_map table.
    
    table_pagenum,  Name of the table name in the database.
    """

    def __init__(self, table_pagenum):
        self.table_pagenum = table_pagenum

    def __repr__(self):
        return "<WikiTable_Map('%s')>" % self.table_name


class WikiComment(object):
    """Class object to model wiki_comment table.
    
    version_id, Id in WikiPage pointing to which the comment is added.
    text,       wiki text markup
    """

    def __init__(self, version_id, text):
        self.version_id = version_id
        self.text = text
        self.translate = h.hitch(self, WikiComment, h.translate, cacheattr='text')

    @reconstructor
    def _init_on_load(self):
        self.translate = h.hitch(self, WikiComment, h.translate, cacheattr='text')

    def __repr__(self):
        return "<WikiComment('%s','%s')>" % (self.version_id, self.text)

    idlabel = property(lambda self: 'comment "%s" for wiki page %s' % (
     self.text, self.wiki.wikiurl))


def wikipage_factory(table_pagenum):
    """
    Create a WikiPage class and make the class name as 'name'.
    Return the created class.
    """

    class WikiPage(object):
        """Class object to model wikipage[0-N] table.
        
        text,   wiki text markup
        author, wiki text author
        """

        def __init__(self, text, author=''):
            self.text = text
            self.author = author
            self.translate = h.hitch(self, self.__class__, h.translate, cacheattr='text')

        @reconstructor
        def _init_on_load(self):
            self.translate = h.hitch(self, self.__class__, h.translate, cacheattr='text')

        def __repr__(self):
            return "<WikiPage[0-N]('%s','%s')>" % (self.text, self.author)

    WikiPage.__name__ = 'WikiPage' + str(table_pagenum)
    return meta.wikipage_factory.setdefault(table_pagenum, WikiPage)


class Timeline(object):
    """Class object to model `timeline` table"""

    def __init__(self, log, userhtml='', itemhtml=''):
        self.log = log
        self.userhtml = userhtml
        self.itemhtml = itemhtml

    def __repr__(self):
        return "<Timeline('%s')>" % self.log


class UserInvitation(object):
    """Class object to model `userinvitation` table"""

    def __init__(self, emailid, digest):
        self.emailid = emailid
        self.digest = digest

    def __repr__(self):
        return "<UserInvitation('%s')>" % self.emailid


class Survey(object):
    """Class object to model `survey` table
    """

    def __init__(self, name, start_time, question='', options='', end_time=None, anonymous=False):
        self.name = name
        self.start_time = start_time
        self.question = question
        self.options = options
        self.end_time = end_time
        self.anonymous = anonymous

    def __repr__(self):
        return "<Survey('%s,%s')>" % (self.name, self.start_time)

    idlabel = property(lambda self: self.name)