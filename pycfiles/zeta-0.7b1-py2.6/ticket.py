# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/ticket.py
# Compiled at: 2010-06-13 10:12:30
"""Component to access data base and do data-crunching on ticket tables.
"""
from __future__ import with_statement
import os, re
from sqlalchemy import *
from sqlalchemy.orm import *
from authkit.permissions import no_authkit_users_in_environ
from zeta.ccore import Component
import zeta.lib.helpers as h
from zeta.model import meta
from zeta.model.schema import *
from zeta.model.tables import Ticket, TicketType, TicketStatus, TicketSeverity, TicketStatusHistory, TicketFilter, TicketComment, TicketReference, Project, User
from zeta.comp.tag import TagComponent
from zeta.comp.attach import AttachComponent
from zeta.comp.project import ProjectComponent
from zeta.comp.timeline import TimelineComponent
from zeta.comp.vote import VoteComponent
from zeta.comp.xsearch import XSearchComponent

class TicketComponent(Component):
    """Component Ticket."""

    def get_tcktype(self, ticket_type=None):
        """Get TicketType instance for the type identified by,
        ticket_type, which can be,
            `id` or `tck_typename` or `TicketType` instance.

        Return,     
            TicketType instance.
            A list of TicketType instances."""
        msession = meta.Session()
        if isinstance(ticket_type, (int, long)):
            ticket_type = msession.query(TicketType).filter_by(id=ticket_type).first()
        elif isinstance(ticket_type, (str, unicode)):
            ticket_type = msession.query(TicketType).filter_by(tck_typename=ticket_type).first()
        elif ticket_type == None:
            ticket_type = msession.query(TicketType).all()
        elif isinstance(ticket_type, TicketType):
            pass
        else:
            ticket_type = None
        return ticket_type

    def get_tckstatus(self, ticket_status=None):
        """Get TicketStatus instance for the status identified by,
        ticket_status, which can be,
            `id` or `tck_statusname` or `TicketStatus` instance.

        Return,     
            TicketStatus instance.
            A list of TicketStatus instances."""
        msession = meta.Session()
        if isinstance(ticket_status, (int, long)):
            ticket_status = msession.query(TicketStatus).filter_by(id=ticket_status).first()
        elif isinstance(ticket_status, (str, unicode)):
            ticket_status = msession.query(TicketStatus).filter_by(tck_statusname=ticket_status).first()
        elif ticket_status == None:
            ticket_status = msession.query(TicketStatus).all()
        elif isinstance(ticket_status, TicketStatus):
            pass
        else:
            ticket_status = None
        return ticket_status

    def get_tckseverity(self, ticket_severity=None):
        """Get TicketSeverity instance for the severity identified by,
        ticket_severity, which can be,
            `id` or `tck_severityname` or `TicketSeverity` instance.

        Return,     
            TicketSeverity instance.
            A list of TicketSeverity instances."""
        msession = meta.Session()
        if isinstance(ticket_severity, (int, long)):
            ticket_severity = msession.query(TicketSeverity).filter_by(id=ticket_severity).first()
        elif isinstance(ticket_severity, (str, unicode)):
            ticket_severity = msession.query(TicketSeverity).filter_by(tck_severityname=ticket_severity).first()
        elif ticket_severity == None:
            ticket_severity = msession.query(TicketSeverity).all()
        elif isinstance(ticket_severity, TicketSeverity):
            pass
        else:
            ticket_status = None
        return ticket_severity

    def create_tcktype(self, tck_typenames, byuser=None):
        """Create tck_typename  entries for the tck_typenames specified by,
        `tck_typenames`
            which can be, a string specifying the tck_typename name or a list of
            such strings"""
        tlcomp = TimelineComponent(self.compmgr)
        if isinstance(tck_typenames, (str, unicode)):
            tck_typenames = [
             tck_typenames]
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ msession.add(TicketType(unicode(t))) for t in tck_typenames if t ]
        tlcomp.log(byuser, 'added ticket types, `%s`' % (', ').join(tck_typenames))

    def create_tckstatus(self, tck_statusnames, byuser=None):
        """Create tck_statusname  entries for the tck_statusames specified by,
        `tck_statusnames`
            which can be, a string specifying the tck_statusname name or a list of
            such strings"""
        tlcomp = TimelineComponent(self.compmgr)
        if isinstance(tck_statusnames, (str, unicode)):
            tck_statusnames = [
             tck_statusnames]
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ msession.add(TicketStatus(unicode(tst))) for tst in tck_statusnames if tst ]
        tlcomp.log(byuser, 'added ticket status, `%s`' % (', ').join(tck_statusnames))

    def create_tckseverity(self, tck_severitynames, byuser=None):
        """Create tck_severityname  entries for the tck_severitynames specified
        by, `tck_severitynames`
            which can be, a string specifying the tck_severityname name or a
            list of such strings"""
        tlcomp = TimelineComponent(self.compmgr)
        if isinstance(tck_severitynames, (str, unicode)):
            tck_severitynames = [
             tck_severitynames]
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ msession.add(TicketSeverity(unicode(tsv))) for tsv in tck_severitynames if tsv ]
        tlcomp.log(byuser, 'added ticket severity, `%s`' % (', ').join(tck_severitynames))

    def create_ticket(self, project, tckdetail, promptuser=None, owner=None, update=False, byuser=None, index=True):
        """Create a new ticket based on,
        `project` can be,
            `id` or `projectname` or `Project` instance
        `tckdetail` which is a tuple of,
            ( ticket_id or ticket_number, summary, description, type, severity )
            severity can be `id` or `tck_severityname`
        `promptuser` can be,
            `id` or `username` or `User` instance.
        `owner` can be,
            `id` or `username` or `User` instance.
            where owner is primarily intended for initially creating a ticket.
        if update=True,
            An existing ticket entry identified by tckdetail[0] will be
            updated.
            `ticket_id` is `id` or `Ticket` instance.
        Once Ticket entry is created, ticket status had to be set as `new` in
        ticket_status_history. If the ticket is just updated, ticket status is
        not touched.
        if index=True,
            then search index the ticket, else don't

        Return,
            Ticket instance."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        prjcomp = ProjectComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        log = ''
        tckdetail = list(tckdetail)
        project = prjcomp.get_project(project)
        ticket = update and self.get_ticket(tckdetail[0], attrload=[
         'type', 'severity', 'promptuser']) or None
        tck_status = self.get_tckstatus('new')
        tck_type = tckdetail[3] and self.get_tcktype(tckdetail[3])
        tck_severity = tckdetail[4] and self.get_tckseverity(tckdetail[4])
        promptuser = promptuser and userscomp.get_user(promptuser)
        owner = owner and userscomp.get_user(owner)
        tckdetail[1] = tckdetail[1] and tckdetail[1].replace('\n', ' ').replace('\r', ' ')
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if update and ticket or ticket:
                loglines = [
                 (
                  'type', ticket.type.tck_typename,
                  getattr(tck_type, 'tck_typename', '')),
                 (
                  'severity', ticket.severity.tck_severityname,
                  getattr(tck_severity, 'tck_severityname', '')),
                 (
                  'promptuser', getattr(ticket.promptuser, 'username', ''),
                  getattr(promptuser, 'username', ''))]
                tck_type and loglines.append(('type', ticket.type.tck_typename,
                 tck_type.tck_typename))
                tck_severity and loglines.append(('severity', ticket.severity.tck_severityname,
                 tck_severity.tck_severityname))
                promptuser and loglines.append(('promptuser', ticket.promptuser.username,
                 promptuser.username))
                tckdetail[1] and loglines.append(('summary', ticket.summary, tckdetail[1]))
                tckdetail[2] != None and loglines.append(('', ticket.description, tckdetail[2]))
                log = h.logfor(loglines)
                if log:
                    log = 'Updated ticket information,\n%s' % log
                tckdetail[1] and setattr(ticket, 'summary', tckdetail[1])
                if tckdetail[2] != None:
                    ticket.description = tckdetail[2]
                    ticket.descriptionhtml = ticket.translate()
                promptuser and setattr(ticket, 'promptuser', promptuser)
                tck_type and setattr(ticket, 'type', tck_type)
                tck_severity and setattr(ticket, 'severity', tck_severity)
                idxreplace = True
            else:
                lasttck = prjcomp._last_entry(project.tickets, 'ticket_number')
                nexttcknum = lasttck and lasttck.ticket_number + 1 or 1
                if not tckdetail[2]:
                    tckdetail[2] = ''
                ticket = Ticket(nexttcknum, tckdetail[1], tckdetail[2])
                ticket.descriptionhtml = ticket.translate()
                promptuser and setattr(ticket, 'promptuser', promptuser)
                tck_type and setattr(ticket, 'type', tck_type)
                tck_severity and setattr(ticket, 'severity', tck_severity)
                project.tickets.append(ticket)
                msession.add(ticket)
                msession.flush()
                loglines = [
                 'created project ticket,',
                 'summary : %s' % ticket.summary,
                 '%s' % ticket.description]
                log = ('\n').join(loglines)
                ticketst = TicketStatusHistory()
                ticketst.owner = owner
                ticketst.status = tck_status
                ticketst.ticket = ticket
                ticket.statushistory.append(ticketst)
                msession.add(ticketst)
                msession.flush()
                ticket.tsh_id = ticketst.id
                idxreplace = True
        log and tlcomp.log(byuser, log, ticket=ticket)
        if index:
            srchcomp = XSearchComponent(self.compmgr)
            srchcomp.indexticket([ticket], replace=idxreplace)
        return ticket

    def config_ticket(self, ticket, components=None, milestones=None, versions=None, blockedby=None, blocking=None, parent=None, type=None, severity=None, promptuser=None, append=True, byuser=None, index=True):
        """For the ticket identified by,
        `ticket` which can be,
            `id` or `ticket_number` or `Ticket` instance

        Add the lists of `components`, `milestones`, `versions`, `blockedby`,
        `blocking`, to the ticket.
        Add the elements `parent`, `type`, `severity` and `promptuser` to the
        ticket.
        if append=True (applicable only for uselist=True schema)
            add the entries in the association tables else replace the
            existing entries with the listed ones.
        if index=True,
            then search index the ticket, else don't
        """
        config = self.compmgr.config
        prjcomp = ProjectComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        userscomp = config['userscomp']
        listattrs = [
         'components', 'milestones', 'versions', 'blockedby',
         'blocking']
        attrs = ['promptuser', 'parent', 'type', 'severity']
        localvars = locals()
        logattrs = listattrs[3:] + attrs
        loglines = []
        [ loglines.append('%s : %s' % (a, localvars[a])) for a in logattrs if localvars[a] != None
        ]
        ticket = self.get_ticket(ticket)
        components = components and filter(None, [ prjcomp.get_component(c) for c in components if c
                                                 ])
        milestones = milestones and filter(None, [ prjcomp.get_milestone(m) for m in milestones if m
                                                 ])
        versions = versions and filter(None, [ prjcomp.get_version(v) for v in versions if v
                                             ])
        blockedby = blockedby and filter(None, [ self.get_ticket(t) for t in blockedby if t
                                               ])
        blocking = blocking and filter(None, [ self.get_ticket(t) for t in blocking if t
                                             ])
        blockedby = blockedby and list(set(blockedby))
        blocking = blocking and list(set(blocking))
        (components or components == []) and loglines.append('components : %s' % (components and components[0].componentname or 'Null'))
        (milestones or milestones == []) and loglines.append('milestones : %s' % (milestones and milestones[0].milestone_name or 'Null'))
        (versions or versions == []) and loglines.append('versions : %s' % (versions and versions[0].version_name or 'Null'))
        log = ('\n').join(loglines)
        if log:
            log = 'changed attributes,\n%s' % log
        parent = parent and self.get_ticket(parent)
        type = type and self.get_tcktype(type)
        severity = severity and self.get_tckseverity(severity)
        promptuser = promptuser and userscomp.get_user(promptuser)
        msession = meta.Session()
        localvars = locals()
        with msession.begin(subtransactions=True):
            for attr in listattrs:
                if localvars[attr] != None:
                    if append:
                        getattr(ticket, attr).extend(localvars[attr])
                    else:
                        setattr(ticket, attr, localvars[attr])

            if promptuser:
                setattr(ticket, 'promptuser', promptuser)
            elif promptuser != None:
                setattr(ticket, 'promptuser', None)
            if parent:
                setattr(ticket, 'parent', parent)
            elif parent != None:
                setattr(ticket, 'parent', None)
            type and setattr(ticket, 'type', type)
            severity and setattr(ticket, 'severity', severity)
        log and tlcomp.log(byuser, log, ticket=ticket)
        if index:
            srchcomp = XSearchComponent(self.compmgr)
            srchcomp.indexticket([ticket], replace=True)
        return

    def addfavorites(self, ticket, favusers, byuser=None):
        """Add the ticket as favorite for users identified by
        `favusers`, which can be (also can be an array of)
            `id` or `username` or `User` instance.
        to `ticket` which can be,
            `id` or `Ticket` instance"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        if not isinstance(favusers, list):
            favusers = [
             favusers]
        favusers = [ userscomp.get_user(u) for u in favusers ]
        ticket = self.get_ticket(ticket, attrload=['project'])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ ticket.favoriteof.append(u) for u in favusers ]
        tlcomp.log(byuser, 'added ticket as favorite', ticket=ticket)

    def delfavorites(self, ticket, favusers, byuser=None):
        """Delete the ticket as favorite for users identified by
        `favusers`, which can be (also can be an array of)
            `id` or `username` or `User` instance.
        to `ticket` which can be,
            `id` or `Ticket` instance"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        if not isinstance(favusers, list):
            favusers = [
             favusers]
        favusers = [ userscomp.get_user(u) for u in favusers ]
        ticket = self.get_ticket(ticket, attrload=['project'])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ ticket.favoriteof.remove(u) for u in favusers if u in ticket.favoriteof ]
        tlcomp.log(byuser, 'removed ticket from favorite', ticket=ticket)

    def create_ticket_status(self, ticket, tckstatdetail, owner, update=False, byuser=None, index=True):
        """Create an entry for the ticket status based on,
        `ticket` can be,
            `id` or `ticket_number` or `Ticket` instance
        `tckstatdetail`, which is a tuple of,
            ( id, status, due_date )
            status can be `id` or `tck_statusname`
        `owner` can be 
            `id` or `username` or `User` instance.
        if update=True,
            The latest ticket status entry will be updated, but the status field
            will not be used.
            `id` can be `id` or TicketStatusHistory instance.
        if index==True,
            then search index the ticket, else dont

        Return,
            TicketStatusHistory instance."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        log = ''
        ticketst = update and self.get_ticket_status(tckstatdetail[0], attrload=[
         'status']) or None
        ticket = self.get_ticket(ticket, attrload=['project'])
        owner = userscomp.get_user(owner)
        tck_status = self.get_tckstatus(tckstatdetail[1])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if update and ticketst or ticketst:
                loglines = [
                 (
                  'status', ticketst.status.tck_statusname,
                  getattr(tck_status, 'tck_statusname', '')),
                 (
                  'due-date', ticketst.due_date, tckstatdetail[2])]
                log = h.logfor(loglines)
                if log:
                    log = 'Updated ticket status,\n%s' % log
                ticketst.status = tck_status
                if tckstatdetail[2] == '':
                    ticketst.due_date = None
                elif tckstatdetail[2] != None:
                    ticketst.due_date = tckstatdetail[2]
                ticketst.owner = owner
                msession.flush()
            else:
                ticketst = TicketStatusHistory()
                ticketst.owner = owner
                ticketst.status = tck_status
                tckstatdetail[2] and setattr(ticketst, 'due_date', tckstatdetail[2])
                ticketst.ticket = ticket
                ticket.statushistory.append(ticketst)
                msession.add(ticketst)
                msession.flush()
                ticket.tsh_id = ticketst.id
                loglines = [
                 'Moved ticket to status,',
                 'status : %s' % tck_status.tck_statusname,
                 'due_date : %s' % (ticketst.due_date or '-')]
                log = ('\n').join(loglines)
        log and tlcomp.log(byuser, log, ticket=ticket)
        if index:
            srchcomp = XSearchComponent(self.compmgr)
            srchcomp.indexticket([ticket], replace=True)
        return ticketst

    def get_ticket(self, ticket=None, attrload=[], attrload_all=[]):
        """Get the Ticket instance corresponding to the ticket entry identified by,
        `ticket` can be,
            `id` or `Ticket` instance

        Return,
            A Ticket instance. or
            List of Ticket instances."""
        if isinstance(ticket, Ticket) and attrload == [] and attrload_all == []:
            return ticket
        else:
            msession = meta.Session()
            if isinstance(ticket, (int, long)):
                q = msession.query(Ticket).filter_by(id=ticket)
            elif isinstance(ticket, Ticket):
                q = msession.query(Ticket).filter_by(id=ticket.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                ticket = q.first()
            elif ticket == None:
                q = msession.query(Ticket)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                ticket = q.all()
            else:
                ticket = None
            return ticket

    def get_ticket_status(self, ticketst=None, attrload=[], attrload_all=[]):
        """Get the TicketStatusHistory instance identified by,
        `ticketst` which can be,
            `id` or `TicketStatusHistory` instance
        Return,
            TicketStatusHistory instance."""
        if isinstance(ticketst, TicketStatusHistory) and attrload == [] and attrload_all == []:
            return ticketst
        else:
            msession = meta.Session()
            if isinstance(ticketst, (int, long)):
                q = msession.query(TicketStatusHistory).filter_by(id=ticketst)
            elif isinstance(ticketst, TicketStatusHistory):
                q = msession.query(TicketStatusHistory).filter_by(id=ticketst.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                ticketst = q.first()
            elif ticketst == None:
                q = msession.query(TicketStatusHistory)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                ticketst = q.all()
            else:
                ticketst = None
            return ticketst

    def create_ticket_comment(self, ticket, tckcomment, update=False, byuser=None):
        """Create ticket comment for ticket identified by,
        `ticket` can be,
            `id` or `ticket_number` or `Ticket` instance
        `tckcomment` is a tuple of,
            ( id, text, commentby )
            commentby can be `id` or `username` or `User` instance.
        if update=True,
            The ticket comment identified by tckcomment[0] and updated.
            `id` can be `id` or `TicketComment` instance.

        Return,
            List of TicketComment instances."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        ticket = self.get_ticket(ticket, attrload=['project'])
        ticketcmt = update and self.get_ticket_comment(tckcomment[0]) or None
        commentby = userscomp.get_user(tckcomment[2])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if update and ticketcmt or ticketcmt:
                ticketcmt.commentby = commentby
                ticketcmt.text = tckcomment[1]
                ticketcmt.texthtml = ticketcmt.translate()
                log = 'updated comment,\n%s' % ticketcmt.text
            else:
                ticketcmt = TicketComment(tckcomment[1])
                ticketcmt.commentby = commentby
                ticketcmt.ticket = ticket
                ticketcmt.texthtml = ticketcmt.translate()
                ticket.comments.append(ticketcmt)
                msession.add(ticketcmt)
                log = 'comment as,\n%s' % ticketcmt.text
        tlcomp.log(byuser, log, ticket=ticket)
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexticket([ticket], replace=True)
        return ticketcmt

    def comment_reply(self, ticketcomment, replytocomment):
        """Make `ticketcomment` a reply to `replytocomment` where,
        `ticketcomment` and `replytocomment` can be,
            `id` or `TicketComment` instance"""
        msession = meta.Session()
        ticketcomment = ticketcomment and self.get_ticket_comment(ticketcomment)
        replytocomment = replytocomment and self.get_ticket_comment(replytocomment, attrload=['replies'])
        if ticketcomment and replytocomment:
            with msession.begin(subtransactions=True):
                replytocomment.replies.append(ticketcomment)

    def get_ticket_comment(self, ticketcmt=None, attrload=[], attrload_all=[]):
        """Get the TicketComment instance identified by `ticketcmt` for ticket 
        identified by,
        `ticketcmt` can be,
            `id` or `TicketComment` instance
        if ticketcmt==None
            Return the list of all TicketComment instances.

        Return,
            TicketComment instance or,
            List of TicketComment instances."""
        if isinstance(ticketcmt, TicketComment) and attrload == [] and attrload_all == []:
            return ticketcmt
        else:
            msession = meta.Session()
            if isinstance(ticketcmt, (int, long)):
                q = msession.query(TicketComment).filter_by(id=ticketcmt)
            elif isinstance(ticketcmt, TicketComment):
                q = msession.query(TicketComment).filter_by(id=ticketcmt.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                ticketcmt = q.first()
            elif ticketcmt == None:
                q = msession.query(TicketComment)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                ticketcmt = q.all()
            else:
                ticketcmt = None
            return ticketcmt

    def get_ticketfilter(self, tf=None, user=None, attrload=[], attrload_all=[]):
        """Get TicketFilter instance identified by,
        `tf`, which can be
            `id` or `TicketFilter` instance
        Return,
            TicketFilter instance or,
            List of TicketFilter instances."""
        if isinstance(tf, TicketFilter) and attrload == [] and attrload_all == []:
            return tf
        else:
            config = self.compmgr.config
            userscomp = config['userscomp']
            user = user and userscomp.get_user(user)
            msession = meta.Session()
            if isinstance(tf, (int, long)):
                q = msession.query(TicketFilter).filter_by(id=tf)
            elif isinstance(tf, TicketFilter):
                q = msession.query(TicketFilter).filter_by(id=tf.id)
            elif isinstance(user, (int, long)):
                q = msession.query(TicketFilter).filter_by(user_id=user)
            elif isinstance(user, User):
                q = msession.query(TicketFilter).filter_by(user_id=user.id)
            else:
                q = None
            if tf and q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                tf = q.first()
            elif q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                tf = q.all()
            elif tf == None:
                q = msession.query(TicketFilter)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                tf = q.all()
            else:
                tf = None
            return tf

    def create_ticketfilter(self, tf=None, name=None, filterbyjson=None, foruser=None, update=False, byuser=None):
        """Create ticket filter for user identified by,
        `foruser` can be,
            `id` or `username` or `User` instance
        `tf`, when update=True, can be,
            `id` or `TicketFilter` instance
        `name, ticket filter name
        `filterbyjson`, specifies filter map in JSON format
        if update=True,
            The ticket filter identified by `tf` will be updated

        Return,
            List of TicketFilter instance."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        tf = tf and self.get_ticketfilter(tf)
        foruser = foruser and userscomp.get_user(foruser)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if update and tf or tf:
                tf.name = name
                tf.filterbyjson = filterbyjson
                foruser not in [None, tf.foruser] and setattr(tf, 'foruser', foruser)
                log = 'updated ticket filter,\n%s' % tf.name
            else:
                tf = TicketFilter(name, filterbyjson)
                tf.foruser = foruser
                foruser.ticketfilters.append(tf)
                msession.add(tf)
                log = 'ticket filter created,\n%s' % tf.name
        tlcomp.log(byuser, log)
        return tf

    def del_ticketfilter(self, tfs=[], byuser=None):
        """Delete the ticket filters identified by,
        `tfs`, which is a list of,
            `id` or `TicketFilter` instance"""
        config = self.compmgr.config
        tlcomp = TimelineComponent(self.compmgr)
        if not isinstance(tfs, list):
            tfs = [
             tfs]
        tfs = [ self.get_ticketfilter(tf) for tf in tfs ]
        log = 'deleted ticket filters,\n%s' % (', ').join([ tf.name for tf in tfs ])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ msession.delete(tf) for tf in tfs ]
        tlcomp.log(byuser, log)

    def get_ticket_references(self, ticket=None):
        pass

    def update_ticket_references(self):
        pass

    def add_tags(self, ticket, tags=[], byuser=None):
        """For the ticket entry identified by,
        `ticket` which can be,
            `id` or `Ticket` instance.
        add tags specified by `tags`."""
        tagcomp = TagComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        ticket = self.get_ticket(ticket, attrload=['project'])
        if ticket and tags:
            addtags = tagcomp.model_add_tags(tags, ticket, byuser=byuser)
        else:
            addtags = []
        ticket and addtags and tlcomp.log(byuser, 'added tags, `%s`' % (', ').join(addtags), ticket=ticket)
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexticket([ticket], replace=True)

    def remove_tags(self, ticket, tags=[], byuser=None):
        """For the ticket entry identified by,
        `ticket` which can be,
            `id` or `Ticket` instance.
        remove tags specified by `tags`."""
        tagcomp = TagComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        ticket = self.get_ticket(ticket, attrload=['project'])
        if ticket and tags:
            rmtags = tagcomp.model_remove_tags(tags, ticket, byuser=byuser)
        else:
            rmtags = []
        ticket and rmtags and tlcomp.log(byuser, 'deleted tags, %s' % (', ').join(rmtags), ticket=ticket)
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexticket([ticket], replace=True)

    def add_attach(self, ticket, attach, byuser=None):
        """Add attachment to the ticket identified by,
        `ticket` which can be,
            `id` or `Ticket` instance.
        `attach` can be
            `id` or `resource_url` or `Attachment` instance."""
        attachcomp = AttachComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        ticket = self.get_ticket(ticket, attrload=['project'])
        attach = attachcomp.get_attach(attach)
        ticket and attachcomp.model_add_attach(attach, ticket, byuser=byuser)
        ticket and tlcomp.log(byuser, 'uploaded attachment, `%s`' % attach.filename, ticket=ticket)

    def remove_attach(self, ticket, attach, byuser=None):
        """Remove attachment to the ticket identified by,
        `ticket` which can be,
            `id` or `Ticket` instance.
        `attach` can be
            `id` or `resource_url` or `Attachment` instance."""
        attachcomp = AttachComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        ticket = self.get_ticket(ticket, attrload=['project'])
        attach = attachcomp.get_attach(attach)
        ticket and attachcomp.model_remove_attach(attach, ticket, byuser=byuser)
        ticket and tlcomp.log(byuser, 'deleted attachment, `%s`' % attach.filename, ticket=ticket)

    def voteup(self, ticket, user):
        """Increase popularity for the ticket"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        votecomp = VoteComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        log = ''
        user = userscomp.get_user(user)
        ticket = self.get_ticket(ticket, attrload=['project'])
        vote = votecomp.get_ticketvote(user, ticket)
        if vote:
            votecomp.recast_vote(vote, 'up')
            log = 're-casted vote'
        else:
            vote = votecomp.cast_vote(user, ticket, 'up')
            log = 'casted vote'
        tlcomp.log(user, log, ticket=ticket)
        return vote

    def votedown(self, ticket, user):
        """Decrease popularity for the ticket"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        votecomp = VoteComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        log = ''
        user = userscomp.get_user(user)
        ticket = self.get_ticket(ticket, attrload=['project'])
        vote = votecomp.get_ticketvote(user, ticket)
        if vote:
            votecomp.recast_vote(vote, 'down')
            log = 're-casted vote'
        else:
            vote = votecomp.cast_vote(user, ticket, 'down')
            log = 'casted vote'
        tlcomp.log(user, log, ticket=ticket)
        return vote

    def documentof(self, ticket, search='xapian'):
        """Make a document for 'ticket' entry to create a searchable index
            [ metadata, attributes, document ], where

            metadata   : { key, value } pairs to be associated with document
            attributes : searchable { key, value } pairs to be associated with
                         document
            document   : [ list , of, ... ] document string, with increasing
                         weightage
        """
        ticket = self.get_ticket(ticket, attrload=[
         'project', 'components', 'milestones',
         'versions', 'tags'])
        tbl_owner = t_user.alias('owner')
        q = select([tbl_owner.c.username], bind=meta.engine).select_from(t_ticket.outerjoin(t_ticket_status_history).outerjoin(at_ticketstatus_owners).outerjoin(tbl_owner, tbl_owner.c.id == at_ticketstatus_owners.c.ownerid)).where(t_ticket.c.id == ticket.id)
        tckowners = [ tup[0] for tup in q.execute().fetchall() if tup[0] ]
        tbl_commentor = t_user.alias('commentor')
        q = select([tbl_commentor.c.username, t_ticket_comment.c.text], bind=meta.engine).select_from(t_ticket.outerjoin(t_ticket_comment).outerjoin(at_ticketcomment_authors).outerjoin(tbl_commentor, tbl_commentor.c.id == at_ticketcomment_authors.c.authorid)).where(t_ticket.c.id == ticket.id)
        cmttexts = []
        for tup in q.execute().fetchall():
            tup[0] and tckowners.append(tup[0])
            tup[1] and cmttexts.append(tup[1])

        tagnames = [ t.tagname for t in ticket.tags ]
        metadata = {'doctype': 'ticket', 'id': ticket.id, 
           'projectname': ticket.project.projectname}
        attributes = search == 'xapian' and [
         'XID:ticket_%s' % ticket.id, 'XCLASS:ticket', 'XPROJECT:%s' % ticket.project.projectname] + [ 'XUSER:%s' % u for u in tckowners ] + [ 'XTAG:%s' % t for t in tagnames
                                                                                                                                             ] or []
        attrs = (' ').join([
         ticket.project.projectname] + tckowners + tagnames)
        document = [
         (' ').join([ticket.description, (' ').join(cmttexts)]),
         (' ').join([
          ticket.summary,
          (' ').join([ co.componentname for co in ticket.components ]),
          (' ').join([ m.milestone_name for m in ticket.milestones ]),
          (' ').join([ v.version_name for v in ticket.versions ])]),
         attrs]
        return [
         metadata, attributes, document]

    def upgradewiki(self, byuser='admin'):
        """Upgrade the database fields supporting wiki markup to the latest
        zwiki version"""
        tlcomp = TimelineComponent(self.compmgr)
        msession = meta.Session()
        tcmts = self.get_ticket_comment()
        tickets = self.get_ticket()
        counttck = len(tickets)
        counttcmt = len(tcmts)
        while tickets:
            with msession.begin(subtransactions=True):
                t = tickets.pop(0)
                t.descriptionhtml = t.translate()

        while tcmts:
            with msession.begin(subtransactions=True):
                tcmt = tcmts.pop(0)
                tcmt.texthtml = tcmt.translate()

        tlcomp.log(byuser, 'Upgraded ticket comments to latest wiki')
        return (
         counttck, counttcmt)

    def _tcktypenames(self):
        return [ tt.tck_typename for tt in self.get_tcktype() ]

    def _tckstatusnames(self):
        return [ tst.tck_statusname for tst in self.get_tckstatus() ]

    def _tckseveritynames(self):
        return [ tsv.tck_severityname for tsv in self.get_tckseverity() ]

    def countvotes(self, ticket=None, votes=[]):
        """Count votes and map it to dictionary
            { u'up' : count, u'down' : count }"""
        if ticket:
            d = {'up': [], 'down': []}
            oj = t_ticket.outerjoin(at_ticket_votes).outerjoin(t_vote)
            q = select([t_vote.c.votedas], bind=meta.engine).select_from(oj).where(t_ticket.c.id == ticket.id)
            [ d[tup[0]].append(1) for tup in q.execute().fetchall() if tup[0]
            ]
            d['up'] = len(d['up'])
            d['down'] = len(d['down'])
        elif votes:
            d = {'up': 0, 'down': 0}
            for vote in votes:
                d[vote.votedas] += 1

        return d

    def mstntickets(self, project):
        """Collect the tickets booked under given `milestone`, or for all the
        milestones for the project
        """
        mtcks = {}
        oj = t_project.outerjoin(t_milestone).outerjoin(at_ticket_milestones).outerjoin(t_ticket).outerjoin(t_ticket_severity).outerjoin(t_ticket_type).outerjoin(t_ticket_status_history, t_ticket.c.tsh_id == t_ticket_status_history.c.id).outerjoin(t_ticket_status).outerjoin(at_ticketstatus_owners).outerjoin(t_user)
        q = select([t_milestone.c.id, t_ticket_type.c.tck_typename,
         t_ticket_severity.c.tck_severityname,
         t_ticket_status.c.tck_statusname,
         t_user.c.username], bind=meta.engine).select_from(oj).where(t_project.c.id == project.id)
        d = {}
        [ d.setdefault(tup[0], []).append(tup[1:]) for tup in q.execute().fetchall() if tup[0]
        ]
        return d

    def ticketids(self, project):
        """Fetch all the ticket ids for the `project`"""
        oj = t_project.outerjoin(at_ticket_projects).outerjoin(t_ticket)
        q = select([t_ticket.c.id], order_by=[
         desc(t_ticket.c.id)], bind=meta.engine).select_from(oj)
        qw = None
        if isinstance(project, (int, long)):
            qw = q.where(t_project.c.id == project)
        elif isinstance(project, (str, unicode)):
            qw = q.where(t_project.c.projectname == project)
        elif isinstance(project, Project):
            qw = q.where(t_project.c.id == project.id)
        res = qw != None and [ tup[0] for tup in qw.execute().fetchall() if tup[0] ] or []
        return res

    def ticketsproject(self):
        """Fetch a mapping of ticket id and project to which the ticket
        belongs to"""
        oj = t_ticket.outerjoin(at_ticket_projects).outerjoin(t_project)
        q = select([t_ticket.c.id, t_project.c.id, t_project.c.projectname], order_by=[
         desc(t_ticket.c.id)], bind=meta.engine).select_from(oj)
        res = [ tup for tup in q.execute().fetchall() if tup[0] if tup[1] ]
        return res

    def ticketsummary(self, project):
        """Fetch all the ticket ids and its summary for the `project`"""
        oj = t_project.outerjoin(at_ticket_projects).outerjoin(t_ticket)
        q = select([t_ticket.c.id, t_ticket.c.summary], bind=meta.engine).select_from(oj)
        qw = None
        if isinstance(project, (int, long)):
            qw = q.where(t_project.c.id == project)
        elif isinstance(project, (str, unicode)):
            qw = q.where(t_project.c.projectname == project)
        elif isinstance(project, Project):
            qw = q.where(t_project.c.id == project.id)
        res = qw != None and [ tup for tup in qw.execute().fetchall() if tup[0] ] or []
        return res

    def projdetails(self, project):
        """Collect ticket's project detail"""
        oj = t_project.outerjoin(t_component).outerjoin(t_milestone).outerjoin(t_version).outerjoin(t_project_team).outerjoin(t_user, t_project_team.c.user_id == t_user.c.id)
        q = select([t_project.c.id,
         t_component.c.componentname, t_component.c.id,
         t_milestone.c.milestone_name, t_milestone.c.id,
         t_version.c.version_name, t_version.c.id,
         t_user.c.username], bind=meta.engine).select_from(oj)
        if isinstance(project, (int, long)):
            q = q.where(t_project.c.id == project)
        elif isinstance(project, (str, unicode)):
            q = q.where(t_project.c.projectname == project)
        elif isinstance(project, Project):
            q = q.where(t_project.c.id == project.id)
        entries = q.execute().fetchall()
        pusers = []
        pcomps = []
        pmstns = []
        pvers = []
        for tup in entries:
            tup[7] and pusers.append(tup[7])
            tup[2] and pcomps.append((tup[1], tup[2]))
            tup[4] and pmstns.append((tup[3], tup[4]))
            tup[6] and pvers.append((tup[5], tup[6]))

        return (list(set(pcomps)), list(set(pmstns)), list(set(pvers)),
         list(set(pusers)))

    def ticketlist(self, project=None, user=None, filters={}):
        """Collect a snap-shot of information for all project tickets"""
        tbl_owner = t_user.alias('owner')
        tbl_promptuser = t_user.alias('promptuser')
        oj = t_ticket.outerjoin(at_ticket_projects).outerjoin(t_project).outerjoin(t_ticket_type).outerjoin(t_ticket_severity).outerjoin(t_ticket_status_history, t_ticket.c.tsh_id == t_ticket_status_history.c.id).outerjoin(t_ticket_status).outerjoin(at_ticketstatus_owners).outerjoin(tbl_owner, at_ticketstatus_owners.c.ownerid == tbl_owner.c.id).outerjoin(at_ticket_components).outerjoin(t_component, at_ticket_components.c.componentid == t_component.c.id).outerjoin(at_ticket_milestones).outerjoin(t_milestone, at_ticket_milestones.c.milestoneid == t_milestone.c.id).outerjoin(at_ticket_versions).outerjoin(t_version, at_ticket_versions.c.versionid == t_version.c.id).outerjoin(at_ticket_promptusers, at_ticket_promptusers.c.ticketid == t_ticket.c.id).outerjoin(tbl_promptuser, at_ticket_promptusers.c.promptuserid == tbl_promptuser.c.id).outerjoin(at_ticket_votes).outerjoin(t_vote, at_ticket_votes.c.voteid == t_vote.c.id)
        q = select([t_ticket.c.id, t_project.c.projectname, t_ticket.c.summary,
         t_ticket.c.created_on,
         t_ticket_type.c.tck_typename,
         t_ticket_severity.c.tck_severityname,
         t_ticket_status.c.tck_statusname,
         t_ticket_status_history.c.id,
         t_ticket_status_history.c.due_date, tbl_owner.c.username,
         tbl_promptuser.c.username,
         t_component.c.id, t_component.c.componentname,
         t_milestone.c.id, t_milestone.c.milestone_name,
         t_version.c.id, t_version.c.version_name,
         t_vote.c.votedas], bind=meta.engine).select_from(oj)
        if project:
            q = q.where(t_project.c.id == project.id)
        elif user:
            q = q.where(or_(tbl_owner.c.id == user.id, tbl_promptuser.c.id == user.id))
        wherecl = []
        for (k, v) in filters.iteritems():
            k == 'tck_typename' and wherecl.append(t_ticket_type.c.tck_typename == v)
            k == 'tck_statusname' and wherecl.append(t_ticket_status.c.tck_statusname == v)
            k == 'tck_severityname' and wherecl.append(t_ticket_severity.c.tck_severityname == v)
            k == 'owner' and wherecl.append(tbl_owner.c.username == v)
            k == 'componentname' and wherecl.append(t_component.c.componentname == v)
            k == 'milestone_name' and wherecl.append(t_milestone.c.milestone_name == v)
            k == 'version_name' and wherecl.append(t_version.c.version_name == v)
            k == 'projectname' and wherecl.append(t_project.c.projectname == v)

        if wherecl:
            q = q.where(and_(*wherecl))
        entries = [ list(tup) for tup in q.execute().fetchall() ]
        tcklist = {}
        votes = {}
        [ (tcklist.setdefault(tup[0], tup[:-1]), votes.setdefault('%s%s' % (tup[0], tup[(-1)]), []).append(1)) for tup in entries
        ]
        tcklist = dict([ (tid, tcklist[tid] + [len(votes.get('%sup' % tid, [])), len(votes.get('%sdown' % tid, []))]) for tid in tcklist if tid
                       ])
        return tcklist

    def ticketdeps(self):
        """Collect a snap-shot of information for all tickets to calculate
        dependency between tickets."""
        tbl_owner = t_user.alias('owner')
        tbl_promptuser = t_user.alias('promptuser')
        oj = t_ticket.outerjoin(at_ticket_projects, at_ticket_projects.c.ticketid == t_ticket.c.id).outerjoin(t_project, at_ticket_projects.c.projectid == t_project.c.id).outerjoin(t_ticket_type).outerjoin(t_ticket_severity).outerjoin(t_ticket_status_history, t_ticket.c.tsh_id == t_ticket_status_history.c.id).outerjoin(t_ticket_status).outerjoin(at_ticketstatus_owners).outerjoin(tbl_owner, at_ticketstatus_owners.c.ownerid == tbl_owner.c.id).outerjoin(at_ticket_components).outerjoin(t_component, at_ticket_components.c.componentid == t_component.c.id).outerjoin(at_ticket_milestones).outerjoin(t_milestone, at_ticket_milestones.c.milestoneid == t_milestone.c.id).outerjoin(at_ticket_versions).outerjoin(t_version, at_ticket_versions.c.versionid == t_version.c.id).outerjoin(at_ticket_promptusers, at_ticket_promptusers.c.ticketid == t_ticket.c.id).outerjoin(tbl_promptuser, at_ticket_promptusers.c.promptuserid == tbl_promptuser.c.id)
        q = select([t_ticket.c.id, t_project.c.projectname,
         t_ticket.c.summary,
         t_ticket_type.c.tck_typename,
         t_ticket_severity.c.tck_severityname,
         t_ticket_status.c.tck_statusname,
         t_component.c.id, t_component.c.componentname,
         t_milestone.c.id, t_milestone.c.milestone_name,
         t_version.c.id, t_version.c.version_name,
         tbl_owner.c.username, tbl_promptuser.c.username,
         t_ticket_status_history.c.due_date,
         t_ticket.c.created_on], bind=meta.engine).select_from(oj)
        entries = q.execute().fetchall()
        tcklist = {}
        [ tcklist.setdefault(tup[0], tup[1:]) for tup in entries ]
        return tcklist

    def currticketstatus(self, t):
        """Return current ticket status"""
        tid = isinstance(t, Ticket) and t.id or t
        oj = t_ticket.outerjoin(t_ticket_status_history, t_ticket_status_history.c.id == t_ticket.c.tsh_id).outerjoin(t_ticket_status)
        q = select([t_ticket_status.c.id, t_ticket_status.c.tck_statusname], bind=meta.engine).select_from(oj).where(t_ticket.c.id == tid)
        res = filter(None, q.execute().fetchall())
        (id, name) = res[0] if res else (None, None)
        return (id, name)

    def isfavorite(self, userid, ticketid):
        """Select whether the ticket is favorite for user"""
        q = select([at_ticket_favorites.c.ticketid, at_ticket_favorites.c.userid], bind=meta.engine).where(and_(at_ticket_favorites.c.ticketid == ticketid, at_ticket_favorites.c.userid == userid))
        return filter(None, q.execute().fetchall())

    def tckcomments(self, ticketid):
        """Collect ticket comments"""
        oj = t_ticket.outerjoin(t_ticket_comment).outerjoin(at_ticketcomment_authors).outerjoin(t_user, at_ticketcomment_authors.c.authorid == t_user.c.id)
        q = select([t_ticket_comment.c.id,
         t_ticket_comment.c.text, t_ticket_comment.c.texthtml,
         t_ticket_comment.c.created_on,
         t_user.c.username], bind=meta.engine).select_from(oj).where(t_ticket_comment.c.ticket_id == ticketid)
        res = [ tup for tup in q.execute().fetchall() if tup[0] ]
        return res

    def tckrcomments(self, ticketid):
        """Collect ticket comments, in threaded mode"""
        oj = t_ticket.outerjoin(t_ticket_comment).outerjoin(at_ticketcomment_authors).outerjoin(t_user, at_ticketcomment_authors.c.authorid == t_user.c.id).outerjoin(at_ticket_replies, t_ticket_comment.c.id == at_ticket_replies.c.ticketcommentid)
        q = select([t_ticket_comment.c.id,
         t_ticket_comment.c.text, t_ticket_comment.c.texthtml,
         t_ticket_comment.c.created_on,
         t_user.c.username,
         at_ticket_replies.c.replytoid], bind=meta.engine).select_from(oj).where(t_ticket_comment.c.ticket_id == ticketid)
        entries = [ tup for tup in q.execute().fetchall() if tup[0] ]
        res = dict([ (tup[0], list(tup) + [[]]) for tup in entries ])
        [ res[res[id][5]][(-1)].append(res[id]) for id in res if res[id][5] ]

        def threaded(cmt, replies):
            for rcmt in cmt[(-1)]:
                replies.append(rcmt)
                threaded(rcmt, replies)

        for id in res.keys():
            if id in res:
                replies = []
                threaded(res[id], replies)
                res[id][-1] = replies
                [ res.pop(r[0], None) for r in replies ]

        return res.values()

    def ticketdetails(self, ticket):
        """Collect the required ticket details"""
        tbl_owner = t_user.alias('owner')
        tbl_promptuser = t_user.alias('promptuser')
        tbl_parent = t_ticket.alias('parent_ticket')
        oj = t_ticket.outerjoin(t_ticket_type).outerjoin(t_ticket_severity).outerjoin(t_ticket_status_history, t_ticket.c.tsh_id == t_ticket_status_history.c.id).outerjoin(t_ticket_status).outerjoin(at_ticketstatus_owners).outerjoin(tbl_owner, at_ticketstatus_owners.c.ownerid == tbl_owner.c.id).outerjoin(at_ticket_promptusers, at_ticket_promptusers.c.ticketid == t_ticket.c.id).outerjoin(tbl_promptuser, at_ticket_promptusers.c.promptuserid == tbl_promptuser.c.id).outerjoin(at_ticket_components).outerjoin(t_component).outerjoin(at_ticket_milestones).outerjoin(t_milestone).outerjoin(at_ticket_versions).outerjoin(t_version).outerjoin(at_ticket_hier, at_ticket_hier.c.childtckid == t_ticket.c.id).outerjoin(tbl_parent, at_ticket_hier.c.partckid == tbl_parent.c.id)
        q = select([t_ticket.c.id,
         t_ticket.c.summary,
         t_ticket_type.c.tck_typename,
         t_ticket_severity.c.tck_severityname,
         t_ticket_status.c.tck_statusname,
         t_ticket_status_history.c.due_date,
         t_ticket.c.created_on,
         tbl_owner.c.username,
         tbl_promptuser.c.username,
         t_component.c.id, t_component.c.componentname,
         t_milestone.c.id, t_milestone.c.milestone_name,
         t_version.c.id, t_version.c.version_name,
         tbl_parent.c.id,
         t_ticket.c.description,
         t_ticket.c.descriptionhtml], bind=meta.engine).select_from(oj).where(t_ticket.c.id == ticket.id)
        tup = q.execute().fetchone()
        d = {'id': tup[0], 'summary': tup[1], 'type': tup[2], 
           'severity': tup[3], 'status': tup[4], 
           'due_date': tup[5], 'created_on': tup[6], 
           'owner': tup[7], 'promptuser': tup[8], 
           'compid': tup[9], 
           'compname': tup[10], 'mstnid': tup[11], 
           'mstnname': tup[12], 'verid': tup[13], 
           'vername': tup[14], 'parent': tup[15], 
           'description': tup[16], 
           'descriptionhtml': tup[17]}
        return d

    def ticketstatus(self, ticket):
        """Collect the status flow for the ticket"""
        tbl_owner = t_user.alias('owner')
        oj = t_ticket.outerjoin(t_ticket_status_history).outerjoin(t_ticket_status).outerjoin(at_ticketstatus_owners).outerjoin(tbl_owner, at_ticketstatus_owners.c.ownerid == tbl_owner.c.id)
        q = select([t_ticket_status_history.c.id,
         t_ticket_status.c.tck_statusname,
         t_ticket_status_history.c.due_date,
         t_ticket_status_history.c.created_on,
         tbl_owner.c.username], order_by=[
         asc(t_ticket_status_history.c.id)], bind=meta.engine).select_from(oj).where(t_ticket.c.id == ticket.id)
        return [ tup for tup in q.execute().fetchall() if tup if tup[0] ]

    def blockersof(self, ticket):
        """Collect the list of blocking tickets"""
        q = select([at_ticket_blockers.c.blockedbyid], bind=meta.engine).where(at_ticket_blockers.c.blockingid == ticket.id)
        return [ tup[0] for tup in q.execute().fetchall() if tup[0] ]

    def blockingfor(self, ticket):
        """Collect the list of blocked by `ticket`"""
        q = select([at_ticket_blockers.c.blockingid], bind=meta.engine).where(at_ticket_blockers.c.blockedbyid == ticket.id)
        return [ tup[0] for tup in q.execute().fetchall() if tup[0] ]

    def allblockers(self):
        """Collect complete list of blocking and blockedby tickets"""
        q = select([at_ticket_blockers.c.blockedbyid,
         at_ticket_blockers.c.blockingid], bind=meta.engine)
        return q.execute().fetchall()

    def allparchild(self):
        """Collect complete list of parent and child tickets"""
        q = select([at_ticket_hier.c.partckid,
         at_ticket_hier.c.childtckid], bind=meta.engine)
        return q.execute().fetchall()

    def childrenfor(self, ticket):
        """Collect the list of child tickets"""
        q = select([at_ticket_hier.c.childtckid], bind=meta.engine).where(at_ticket_hier.c.partckid == ticket.id)
        return [ tup[0] for tup in q.execute().fetchall() if tup[0] ]

    def computefilters(self, ds, tckfilters=None):
        """Computer the filter booleans based on the filter-rules in
        `tckfilters` and/or `filtermaps`"""
        if not isinstance(ds, list):
            ds = [
             ds]
        if tckfilters:
            [ d.update({filtername: any([ all([ recomp.match(d[f]) for (f, recomp) in andlist ]) for andlist in orlist ])}) for d in ds for (filtername, orlist) in tckfilters
            ]
        return ds

    def attachments(self, project):
        """Collect attachment list for all tickets,
        Return attachments"""
        oj = at_ticket_attachments.outerjoin(t_ticket).outerjoin(t_attachment).outerjoin(at_attachment_tags, at_attachment_tags.c.attachmentid == t_attachment.c.id).outerjoin(t_tag, at_attachment_tags.c.tagid == t_tag.c.id).outerjoin(at_attachment_uploaders, at_attachment_uploaders.c.attachmentid == t_attachment.c.id).outerjoin(t_user, at_attachment_uploaders.c.uploaderid == t_user.c.id).outerjoin(at_ticket_projects, at_ticket_projects.c.ticketid == t_ticket.c.id).outerjoin(t_project, at_ticket_projects.c.projectid == t_project.c.id)
        q = select([t_ticket.c.id,
         t_attachment.c.id, t_attachment.c.filename,
         t_attachment.c.summary, t_attachment.c.download_count,
         t_attachment.c.created_on, t_user.c.username,
         t_tag.c.tagname], bind=meta.engine).select_from(oj).where(t_project.c.id == project.id)
        entries = q.execute().fetchall()
        result = {}
        for tup in entries:
            if tup[1] == None:
                continue
            fortck = result.get(tup[0], {})
            foratt = fortck.get(tup[1], [])
            if foratt:
                tup[7] and foratt[(-1)].append(tup[7])
            else:
                foratt = list(tup[2:7])
                foratt.append(tup[7] and [tup[7]] or [])
            fortck[tup[1]] = foratt
            result[tup[0]] = fortck

        return result

    def usertickets(self, user):
        """List of tickets in which `user` participated"""
        oj = at_ticketstatus_owners.outerjoin(t_ticket_status_history).outerjoin(t_ticket, t_ticket_status_history.c.ticket_id == t_ticket.c.id)
        q = select([t_ticket.c.id, t_ticket_status_history.c.id], bind=meta.engine).select_from(oj).where(at_ticketstatus_owners.c.ownerid == user.id)
        tickets = {}
        [ tickets.setdefault(tup[0], []).append(tup[1]) for tup in q.execute().fetchall() if tup[0]
        ]
        return tickets

    def usercomments(self, user):
        """List of comments by user"""
        oj = at_ticketcomment_authors.outerjoin(t_ticket_comment)
        q = select([t_ticket_comment.c.id], bind=meta.engine).select_from(oj).where(at_ticketcomment_authors.c.authorid == user.id)
        tcmts = [ tup[0] for tup in q.execute().fetchall() if tup[0] ]
        return tcmts

    tcktypenames = property(_tcktypenames)
    tckstatusnames = property(_tckstatusnames)
    tckseveritynames = property(_tckseveritynames)