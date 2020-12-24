# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/attach.py
# Compiled at: 2010-06-12 09:23:03
"""Component to access data base and do data-crunching on attachment tables.
"""
from __future__ import with_statement
import shutil, os
from sqlalchemy import *
from sqlalchemy.orm import *
from authkit.permissions import no_authkit_users_in_environ
from pylons import config
from zeta.ccore import Component
from zeta.model import meta
from zeta.model.tables import Attachment
from zeta.model.schema import t_attachment, t_tag, t_user, at_user_icons, at_user_photos, at_project_icons, at_project_logos, at_project_attachments, at_ticket_attachments, at_license_attachments, at_review_attachments, at_wiki_attachments, at_attachment_tags, at_attachment_uploaders
from zeta.lib.constants import ATTACH_DIR
import zeta.lib.helpers as h
from zeta.comp.tag import TagComponent
from zeta.comp.timeline import TimelineComponent
from zeta.comp.xsearch import XSearchComponent

class AttachComponent(Component):
    """Component to handle all attachments."""

    def _store_fileupload(self, fdsrc, attach):
        """'fdsrc' is a file like object object which contain the attached
        file. Store the file in the attachment table."""
        envpath = h.fromconfig('zeta.envpath')
        dstfilename = os.path.join(envpath, ATTACH_DIR, str(attach.id))
        fd = open(dstfilename, 'wb')
        shutil.copyfileobj(fdsrc, fd)
        fdsrc.close()
        fd.close()
        return

    def downloadattach(self, attach=None):
        """Get the attachment entry specified by,
        `attach`, which can be,
            `id` or `Attachment` instance.
        and send the file for downloading."""
        attach = self.get_attach(attach=attach)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            attach.download_count += 1
        return attach

    def get_attach(self, attach=None, attrload=[], attrload_all=[]):
        """Get the attachment entry identified by,
        `attach` which can be
            `id` or `Attachment` instance.

        Return,
            Attachment Instance(s)."""
        if isinstance(attach, Attachment) and eagerload == [] and eagerload_all == []:
            return attach
        else:
            msession = meta.Session()
            if isinstance(attach, (int, long)):
                q = msession.query(Attachment).filter_by(id=attach)
            elif isinstance(attach, Attachment):
                q = msession.query(Attachment).filter_by(id=attach.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                attach = q.first()
            elif attach == None:
                q = msession.query(Attachment)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                attach = q.all()
            return attach

    def create_attach(self, filename, fdfile=None, uploader=None, summary=None):
        """Create an attachment for `filename`,
        Return,
            Attachment instance."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        uploader = uploader and userscomp.get_user(uploader)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            attach = Attachment(filename, 0)
            summary and setattr(attach, 'summary', summary)
            uploader and setattr(attach, 'uploader', uploader)
            if fdfile:
                attach.content = fdfile.read()
                fdfile.close()
            msession.add(attach)
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexattach([attach])
        return attach

    def edit_summary(self, attach, summary='', byuser=None):
        """Edit the summary text for already created attachment, specified by,
        `attach` which can be,
            `id` or `Attachment` instance."""
        userscomp = self.compmgr.config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        attach = self.get_attach(attach)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            attach.summary = summary
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexattach([attach], replace=True)
        attach and tlcomp.log(byuser, 'Updated summary, `%s`' % summary, attach=attach)

    def remove_attach(self, attach=None, byuser=None):
        """Remove the attachment entry identified by,
        `attach` which can be
            `id` or `Attachment` instance.
        """
        attach = self.get_attach(attach=attach)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            attach and msession.delete(attach)
            msession.flush()

    def add_tags(self, attach, tags=[], byuser=None):
        """Add tags for the attachment entry identified by,
        `attach` which can be
            `id` or `Attachment` instance.
        `tags` can be,
            list of `tagname` strings
            list of `Tag` instances"""
        tagcomp = TagComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        attach = self.get_attach(attach=attach)
        if attach and tags:
            addtags = tagcomp.model_add_tags(tags, attach, byuser=byuser)
        else:
            addtags = []
        srchcomp = XSearchComponent(self.compmgr)
        attach and addtags and tlcomp.log(byuser, 'added tags, `%s`' % (', ').join(addtags), attach=attach)
        srchcomp.indexattach([attach], replace=True)

    def remove_tags(self, attach, tags=[], byuser=None):
        """Remove tags for the attachment entry identified by,
        `attach` which can be
            `id` or `Attachment` instance.
        `tags` can be,
            list of `tagname` strings
            list of `Tag` instances"""
        tagcomp = TagComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        attach = self.get_attach(attach=attach)
        if attach and tags:
            rmtags = tagcomp.model_remove_tags(tags, attach, byuser=byuser)
        else:
            rmtags = []
        srchcomp = XSearchComponent(self.compmgr)
        attach and rmtags and tlcomp.log(byuser, 'deleted tags , `%s`' % (', ').join(rmtags), attach=attach)
        srchcomp.indexattach([attach], replace=True)

    def model_add_attach(self, attach, modelobj, byuser=None):
        """Add attachment to the model instance `modelobj`.
        `attach` which can be
            `id` or `Attachment` instance."""
        attach = self.get_attach(attach=attach)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            attach and modelobj.attachments.append(attach)

    def model_remove_attach(self, attach, modelobj, byuser=None):
        """Remove attachment from model instance `modelobj`.
        `attach` which can be
            `id` or `Attachment` instance."""
        attach = self.get_attach(attach=attach)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if attach:
                msession.delete(attach)

    def attachments(self, offset=None, limit=None):
        """Collect all attachments.
        Return attachments"""
        oj = t_attachment.outerjoin(at_attachment_tags, at_attachment_tags.c.attachmentid == t_attachment.c.id).outerjoin(t_tag, at_attachment_tags.c.tagid == t_tag.c.id).outerjoin(at_attachment_uploaders, at_attachment_uploaders.c.attachmentid == t_attachment.c.id).outerjoin(t_user, at_attachment_uploaders.c.uploaderid == t_user.c.id)
        q = select([t_attachment.c.id, t_attachment.c.filename,
         t_attachment.c.summary, t_attachment.c.download_count,
         t_attachment.c.created_on, t_user.c.username,
         t_tag.c.tagname], bind=meta.engine).select_from(oj)
        if offset:
            q = q.offset(offset)
        if limit:
            q = q.limit(limit)
        entries = q.execute().fetchall()
        result = {}
        for tup in entries:
            if tup[0] == None:
                continue
            foratt = result.get(tup[0], [])
            if foratt:
                tup[6] and foratt[(-1)].append(tup[6])
            else:
                foratt = list(tup[1:6])
                foratt.append(tup[6] and [tup[6]] or [])
            result[tup[0]] = foratt

        return result

    def latestattachs(self):
        """Fetch the latest attachment"""
        msession = meta.Session()
        q = msession.query(Attachment).order_by(Attachment.id.desc()).limit(1)
        attachs = q.all()
        attach = attachs and attachs[0] or None
        return attach

    def attachassc(self):
        """Fetch all the entries for user, project, license, ticket, wiki,
        review etc... that have associated attachments"""
        attachs = {}
        q = select([at_user_icons.c.attachid, at_user_icons.c.userid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('user', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_user_photos.c.attachid, at_user_photos.c.userid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('user', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_license_attachments.c.attachmentid,
         at_license_attachments.c.licenseid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('license', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_project_icons.c.attachid,
         at_project_icons.c.projectid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('project', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_project_logos.c.attachid,
         at_project_logos.c.projectid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('project', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_project_attachments.c.attachmentid,
         at_project_attachments.c.projectid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('project', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_ticket_attachments.c.attachmentid,
         at_ticket_attachments.c.ticketid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('ticket', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_review_attachments.c.attachmentid,
         at_review_attachments.c.reviewid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('review', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        q = select([at_wiki_attachments.c.attachmentid,
         at_wiki_attachments.c.wikiid], bind=meta.engine)
        [ attachs.setdefault(aid, []).append(('wiki', uid)) for (aid, uid) in q.execute().fetchall()
        ]
        return attachs

    def uploadedbyuser(self, user):
        """Find all the attachments uploaded by `user`"""
        oj = at_attachment_uploaders.outerjoin(t_attachment).outerjoin(at_attachment_tags, at_attachment_tags.c.attachmentid == t_attachment.c.id).outerjoin(t_tag, at_attachment_tags.c.tagid == t_tag.c.id)
        q = select([t_attachment.c.id, t_attachment.c.filename,
         t_attachment.c.summary, t_attachment.c.download_count,
         t_attachment.c.created_on,
         t_tag.c.tagname], bind=meta.engine).select_from(oj).where(at_attachment_uploaders.c.uploaderid == user.id)
        entries = q.execute().fetchall()
        attachs = {}
        for tup in entries:
            if tup[0] == None:
                continue
            foratt = attachs.get(tup[0], [])
            if foratt:
                tup[5] and foratt[(-1)].append(tup[5])
            else:
                foratt = list(tup[1:5])
                foratt.append(tup[5] and [tup[5]] or [])
            attachs[tup[0]] = foratt

        return attachs

    def documentof(self, attach, search='xapian'):
        """Make a document for 'attach' entry to create a searchable index
            [ metadata, attributes, document ], where

            metadata   : { key, value } pairs to be associated with document
            attributes : searchable { key, value } pairs to be associated with
                         document
            document   : [ list , of, ... ] document string, with increasing
                         weightage
        """
        attach = self.get_attach(attach, attrload=['tags', 'uploader'])
        tagnames = [ t.tagname for t in attach.tags ]
        metadata = {'doctype': 'attach', 'id': attach.id}
        attributes = search == 'xapian' and [
         'XID:attach_%s' % attach.id,
         'XCLASS:site', 'XCLASS:attach',
         'XUSER:%s' % attach.uploader.username,
         'XFILE:%s' % attach.filename] + [ 'XTAG:%s' % t for t in tagnames
                                         ] or []
        attrs = (' ').join([
         attach.uploader.username, attach.filename] + tagnames)
        try:
            content = unicode(attach.content)
        except:
            content = ''

        document = [
         content, attach.summary, attrs]
        return [
         metadata, attributes, document]