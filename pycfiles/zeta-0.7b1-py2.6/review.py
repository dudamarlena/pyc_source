# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/review.py
# Compiled at: 2010-06-12 13:39:12
"""Component to access data base and do data-crunching on review tables.
"""
from __future__ import with_statement
import os
from os.path import commonprefix, join
from sqlalchemy import *
from sqlalchemy.orm import *
from authkit.permissions import no_authkit_users_in_environ
from zeta.ccore import Component
import zeta.lib.helpers as h, zeta.lib.vcsadaptor as va
from zeta.model.schema import t_user, t_project, t_review, t_reviewset, t_attachment, t_review_comment, t_reviewcomment_nature, t_reviewcomment_action, t_tag, t_user, at_review_projects, at_review_authors, at_review_moderators, at_reviewset_reviews, at_review_commentors, at_review_replies, at_review_favorites, at_review_participants, at_review_attachments, at_attachment_tags, at_attachment_uploaders
from zeta.model import meta
from zeta.model.tables import ReviewComment_Nature, ReviewComment_Action, ReviewSet, Review, ReviewComment, Project
from zeta.comp.project import ProjectComponent
from zeta.comp.tag import TagComponent
from zeta.comp.attach import AttachComponent
from zeta.comp.timeline import TimelineComponent
from zeta.comp.vcs import VcsComponent
from zeta.comp.wiki import WikiComponent
from zeta.comp.xsearch import XSearchComponent

class ReviewComponent(Component):
    """Component Review."""

    def get_reviewcomment_nature(self, revnature=None):
        """Get the review nature instance identified by,
        `revnature` which can be,
            `id` or `review_naturename` `ReviewComment_Nature` instance.
        if revnature==None, 
            Return all the ReviewComment_Nature instances

        Return,
            A list of one or more ReviewComment_Nature instance."""
        msession = meta.Session()
        if isinstance(revnature, (int, long)):
            revnature = msession.query(ReviewComment_Nature).filter_by(id=revnature).first()
        elif isinstance(revnature, (str, unicode)):
            revnature = msession.query(ReviewComment_Nature).filter_by(naturename=revnature).first()
        elif revnature == None:
            revnature = msession.query(ReviewComment_Nature).all()
        elif isinstance(revnature, ReviewComment_Nature):
            pass
        else:
            revnature = None
        return revnature

    def get_reviewcomment_action(self, revaction=None):
        """Get the review action instance identified by,
        `revaction` which can be,
            `id` or `actionname` `ReviewComment_Action` instance.
        if revaction==None, 
            Return all the ReviewComment_Action instances

        Return,
            A list of one or more ReviewComment_Action instance."""
        msession = meta.Session()
        if isinstance(revaction, (int, long)):
            revaction = msession.query(ReviewComment_Action).filter_by(id=revaction).first()
        elif isinstance(revaction, (str, unicode)):
            revaction = msession.query(ReviewComment_Action).filter_by(actionname=revaction).first()
        elif revaction == None:
            revaction = msession.query(ReviewComment_Action).all()
        elif isinstance(revaction, ReviewComment_Action):
            pass
        else:
            revaction = None
        return revaction

    def get_reviewset(self, reviewset=None, attrload=[], attrload_all=[]):
        """Get the reviewset entry identified by,
        `reviewset` which can be
            `id` or `ReviewSet` instance.
        if reviewset is None, all the ReviewSet entries (instances) associated with
        the will be returned.

        Return,
            A list of one or more ReviewSet instance."""
        msession = meta.Session()
        if isinstance(reviewset, ReviewSet) and attrload == [] and attrload_all == []:
            return reviewset
        else:
            if isinstance(reviewset, (int, long)):
                q = msession.query(ReviewSet).filter_by(id=reviewset)
            elif isinstance(reviewset, ReviewSet):
                q = msession.query(ReviewSet).filter_by(id=reviewset.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                reviewset = q.first()
            elif reviewset == None:
                q = msession.query(ReviewSet)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                reviewset = q.all()
            else:
                reviewset = None
            return reviewset

    def get_review(self, review=None, attrload=[], attrload_all=[]):
        """Get the review entry identified by,
        `review` which can be
            `id` or `Review` instance.
        if review is None, all the Review entries (instances) associated with
        the will be returned.

        Return,
            A list of one or more Review instance."""
        msession = meta.Session()
        if isinstance(review, Review) and attrload == [] and attrload_all == []:
            return review
        else:
            if isinstance(review, (int, long)):
                q = msession.query(Review).filter_by(id=review)
            elif isinstance(review, Review):
                q = msession.query(Review).filter_by(id=review.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                review = q.first()
            elif review == None:
                q = msession.query(Review)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                review = q.all()
            else:
                review = None
            return review

    def create_reviewnature(self, naturenames, byuser=None):
        """Create naturename  entries for the naturenames specified by,
        `naturenames`
            which can be, a string specifying the naturename or a list of
            such strings"""
        tlcomp = TimelineComponent(self.compmgr)
        if isinstance(naturenames, (str, unicode)):
            naturenames = [
             naturenames]
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            for n in naturenames:
                msession.add(ReviewComment_Nature(unicode(n)))

        tlcomp.log(byuser, 'added review natures, `%s`' % (', ').join(naturenames))

    def create_reviewaction(self, actionnames, byuser=None):
        """Create actionname  entries for the actionnames specified by,
        `actionnames`
            which can be, a string specifying the actionname or a list of
            such strings"""
        tlcomp = TimelineComponent(self.compmgr)
        if isinstance(actionnames, (str, unicode)):
            actionnames = [
             actionnames]
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            for a in actionnames:
                msession.add(ReviewComment_Action(unicode(a)))

        tlcomp.log(byuser, 'added review action types, `%s`' % (', ').join(actionnames))

    def create_reviewset(self, project, name, byuser=None):
        """Create ReviewSet  entry, with `name` for,
        `project`, which can be,
            `id` or `Project` instance"""
        tlcomp = TimelineComponent(self.compmgr)
        projcomp = ProjectComponent(self.compmgr)
        rs = None
        project = projcomp.get_project(project)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if project:
                rs = ReviewSet(unicode(name))
                rs.project = project
                msession.add(rs)
        project and tlcomp.log(byuser, 'Created review set, `%s`' % name, project=project)
        return rs

    def update_reviewset(self, rset, name, byuser=None):
        """Update ReviewSet, identified by,
        `rset`, which can be,
            `id` or `ReviewSet` instance"""
        tlcomp = TimelineComponent(self.compmgr)
        rset = self.get_reviewset(rset)
        log = ''
        msession = meta.Session()
        if rset and rset.name != name:
            with msession.begin(subtransactions=True):
                setattr(rset, 'name', name)
                log = 'Updated review set name to `%s`' % name
        log and tlcomp.log(byuser, log, project=rset.project)
        return rset

    def add_reviewtoset(self, rset, review, byuser=None):
        """Add `review` to `rset`, where,
        `review`, can be,
            `id` or `Review` instance
        `rset`, can be,
            `id` or `ReviewSet` instance"""
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review)
        rset = self.get_reviewset(rset)
        log = ''
        msession = meta.Session()
        if review and rset:
            with msession.begin(subtransactions=True):
                rset.reviews.append(review)
            log = 'Added review `%s` to review set, `%s`' % (
             review.id, rset.name)
        log and tlcomp.log(byuser, log, review=review)

    def remove_reviewfromset(self, review, byuser=None):
        """Remove `review` from its review set, where,
        `review`, can be,
            `id` or `Review` instance
        """
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review)
        log = ''
        rset = review.reviewset
        msession = meta.Session()
        if review and rset:
            with msession.begin(subtransactions=True):
                review.reviewset = None
            log = 'Removed review `%s` from review set, `%s`' % (
             review.id, rset.name)
        log and tlcomp.log(byuser, log, review=review)
        return

    def create_review(self, project, revdetail, update=False, byuser=None):
        """Create review entry for project identified by,
        `project` which can be,
            `id` or `Project` instance.
        `revdetail` is a tuple of,
            (id, resource_url, version, author, moderator)
            author can be `id` or `username` or `User` instance.
            moderator can be `id` or `username` or `User` instance or None
        if update=True,
            An exisiting review entiry will be updated with revdetail.
            `id` can be `id` or `Review` instance.
        Return,
            Review instance."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        prjcomp = ProjectComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        log = ''
        review = update and self.get_review(revdetail[0]) or None
        project = prjcomp.get_project(project)
        res_url = revdetail[1]
        version = revdetail[2]
        author = revdetail[3]
        if revdetail[3] not in ('', None):
            author = userscomp.get_user(revdetail[3])
        moderator = revdetail[4]
        if revdetail[4] not in ('', None):
            moderator = userscomp.get_user(revdetail[4])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if update and review or review:
                loglines = []
                res_url and loglines.append((
                 'resource-url', review.resource_url, res_url))
                version and loglines.append((
                 'version', review.version, version))
                revdetail[3] != None and loglines.append((
                 'author', '', revdetail[3]))
                revdetail[4] != None and loglines.append((
                 'moderator', '', revdetail[4]))
                log = h.logfor(loglines)
                if log:
                    log = 'updated review details,\n%s' % log
                res_url and setattr(review, 'resource_url', res_url)
                version and setattr(review, 'version', version)
                if author == '':
                    review.author = None
                elif author != None:
                    review.author = author
                if moderator == '':
                    review.moderator = None
                elif moderator != None:
                    review.moderator = moderator
                idxreplace = True
            else:
                lastrev = prjcomp._last_entry(project.reviews, 'review_number')
                nextrevnum = lastrev and lastrev.review_number + 1 or 1
                review = Review(res_url, version, nextrevnum)
                author and setattr(review, 'author', author)
                moderator and setattr(review, 'moderator', moderator)
                project.reviews.append(review)
                msession.add(review)
                msession.flush()
                loglines = [
                 'created new review for, %s' % review.resource_url]
                author and loglines.append('author : %s' % author.username)
                moderator and loglines.append('moderator : %s' % moderator.username)
                log = ('\n').join(loglines)
                idxreplace = False
        log and tlcomp.log(byuser, log, review=review)
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexreview([review], replace=idxreplace)
        return review

    def set_participants(self, review, participants, append=False, remove=False, byuser=None):
        """Either  append or replace the current review paricipant list with
        `participants`, which can be a list of,
            `id` or `username` or `User` instance.
        `review` can be,
            `id` or `Review` instance.
        `append` will all the participants to the existing list
        `remove` will remove the participants form the existing list"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review, attrload=['project'])
        participants = [ userscomp.get_user(u) for u in participants if u ]
        logforusers = (', ').join([ u.username for u in participants if u ])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if append:
                review.participants.extend(participants)
                log = 'added participants, `%s`' % logforusers
            elif remove:
                [ review.participants.remove(u) for u in participants if u ]
                log = 'removed participants, `%s`' % logforusers
            else:
                review.participants = participants
                log = 'participants, `%s`' % logforusers
        if logforusers:
            tlcomp.log(byuser, log, review=review)
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexreview([review], replace=True)

    def close_review(self, review, close=True, byuser=None):
        """Close the review identified by,
        `review` which can be
            `id` or `Review` instance.
        close field will be set as `close`.
        
        Return,
            True if review is closed.
            False if review is not closed."""
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review, attrload=[
         'project'], attrload_all=[
         'comments.replies'])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if close == True and self.allapproved(review):
                review.closed = True
                rcode = True
                log = 'closed '
            elif close == False:
                review.closed = False
                rcode = False
                log = 'opened '
            else:
                review.closed = False
                rcode = False
                log = 'failed closing '
        tlcomp.log(byuser, log, review=review)
        return rcode

    def addfavorites(self, review, favusers, byuser=None):
        """Add the review as favorite for users identified by
        `favusers`, which can be (also can be an array of)
            `id` or `username` or `User` instance.
        to `review` which can be,
            `id` or `Review` instance"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        if not isinstance(favusers, list):
            favusers = [
             favusers]
        favusers = [ userscomp.get_user(u) for u in favusers ]
        review = self.get_review(review, attrload=['project'])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ review.favoriteof.append(u) for u in favusers ]
        tlcomp.log(byuser, 'added review as favorite', review=review)

    def delfavorites(self, review, favusers, byuser=None):
        """Delete the review as favorite for users identified by
        `favusers`, which can be (also can be an array of)
            `id` or `username` or `User` instance.
        to `review` which can be,
            `id` or `Review` instance"""
        if not isinstance(favusers, list):
            favusers = [
             favusers]
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        favusers = [ userscomp.get_user(u) for u in favusers ]
        review = self.get_review(review, attrload=['project'])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ review.favoriteof.remove(u) for u in favusers if u in review.favoriteof ]
        tlcomp.log(byuser, 'removed review from favorite', review=review)

    def create_reviewcomment(self, review, commentdetail, update=False, byuser=None):
        """Create review comment entry for which
        `commentdetail` is a tuple of,
            ( id, position, text, commentor, nature, action )
        if update=True,
            An exisiting reviewcomment entry will be updated with commentdetail

        Return,
            ReviewComment instance."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        tlcomp = TimelineComponent(self.compmgr)
        log = ''
        review = self.get_review(review, attrload=['project'])
        revcomment = update and self.get_reviewcomment(commentdetail[0]) or None
        commentby = userscomp.get_user(commentdetail[3])
        nature = commentdetail[4] and self.get_reviewcomment_nature(commentdetail[4]) or None
        action = commentdetail[5] and self.get_reviewcomment_action(commentdetail[5]) or None
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if update and revcomment or revcomment:
                commentdetail[1] and setattr(revcomment, 'position', commentdetail[1])
                if commentdetail[2]:
                    revcomment.text = commentdetail[2]
                    revcomment.texthtml = revcomment.translate()
                commentby and setattr(revcomment, 'commentby', commentby)
                nature and setattr(revcomment, 'nature', nature)
                action and setattr(revcomment, 'action', action)
                log = 'updated comment,\n%s' % revcomment.text
            elif review:
                revcomment = ReviewComment(commentdetail[1], commentdetail[2])
                nature and setattr(revcomment, 'nature', nature)
                commentby and setattr(revcomment, 'commentby', commentby)
                revcomment.texthtml = revcomment.translate()
                revcomment.review = review
                review.comments.append(revcomment)
                msession.add(revcomment)
                loglines = [
                 'comment,position : %s' % commentdetail[1]]
                nature and loglines.append('nature : %s' % nature.naturename)
                action and loglines.append('action : %s' % action.actionname)
                loglines.append(revcomment.text)
                log = ('\n').join(loglines)
        log and tlcomp.log(byuser, log, review=review)
        srchcomp = XSearchComponent(self.compmgr)
        srchcomp.indexreview([review], replace=True)
        return revcomment

    def process_reviewcomment(self, revcomment, reviewnature=None, reviewaction=None, approve=None, byuser=None):
        """Approve review comment for review comment identified by,
        `revcomment` which can be,
            `id`
        approved field will be set as `approve`."""
        tlcomp = TimelineComponent(self.compmgr)
        revcomment = self.get_reviewcomment(revcomment, attrload_all=[
         'review.project'])
        review = revcomment.review
        if reviewnature not in ('', None):
            reviewnature = self.get_reviewcomment_nature(reviewnature)
        if reviewaction not in ('', None):
            reviewaction = self.get_reviewcomment_action(reviewaction)
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            loglines = []
            if reviewnature == '':
                revcomment.nature = None
                loglines.append('nature : ')
            elif reviewnature != None:
                revcomment.nature = reviewnature
                loglines.append('nature : `%s`' % reviewnature.naturename)
            if reviewaction == '':
                revcomment.action = None
                loglines.append('action : ')
            elif reviewaction != None:
                revcomment.action = reviewaction
                loglines.append('action : `%s`' % reviewaction.actionname)
            if approve != None:
                setattr(revcomment, 'approved', approve)
                loglines.append('approved : %s' % approve)
        if loglines:
            log = 'processing review comment `%s`...,\n%s' % (
             revcomment.text[:10], ('\n').join(loglines))
            tlcomp.log(byuser, log, review=review)
        return

    def get_reviewcomment(self, revcomment=None, attrload=[], attrload_all=[]):
        """Get review comment entry for review comment identified by,
        `revcomment` which can be,
            `id` or `ReviewComment` instance.
        if `revcomment` is None, then all the ReviewComment entries
        (instances) associated with `review` will be returned.

        Return,
            A list of one or more ReviewComment instances."""
        if isinstance(revcomment, ReviewComment) and attrload == [] and attrload_all == []:
            pass
        msession = meta.Session()
        if isinstance(revcomment, (int, long)):
            q = msession.query(ReviewComment).filter_by(id=revcomment)
        elif isinstance(revcomment, ReviewComment):
            q = msession.query(ReviewComment).filter_by(id=revcomment.id)
        else:
            q = None
        if q != None:
            q = q.options(*[ eagerload_all(e) for e in attrload_all ])
            q = q.options(*[ eagerload(e) for e in attrload ])
            revcomment = q.first()
        elif revcomment == None:
            q = msession.query(ReviewComment)
            q = q.options(*[ eagerload_all(e) for e in attrload_all ])
            q = q.options(*[ eagerload(e) for e in attrload ])
            revcomment = q.all()
        else:
            revcomment = None
        return revcomment

    def comment_reply(self, reviewcomment, replytocomment):
        """Make `reviewcomment` a reply to `replytocomment` where,
        `reviewcomment` and `replytocomment` can be,
            `id` or `ReviewComment` instance"""
        msession = meta.Session()
        reviewcomment = reviewcomment and self.get_reviewcomment(reviewcomment)
        replytocomment = replytocomment and self.get_reviewcomment(replytocomment)
        if reviewcomment and replytocomment:
            with msession.begin(subtransactions=True):
                replytocomment.replies.append(reviewcomment)

    def add_tags(self, review, tags=[], byuser=None):
        """For the review entry added tags.
        `review` which can be,
            `id` or Review instance.
        `tags` which can be,
            `tagname`."""
        tagcomp = TagComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review, attrload=['project'])
        if review and tags:
            addtags = tagcomp.model_add_tags(tags, review, byuser)
        else:
            addtags = []
        srchcomp = XSearchComponent(self.compmgr)
        review and addtags and tlcomp.log(byuser, 'added tags, `%s`' % (', ').join(addtags), review=review)
        srchcomp.indexreview([review], replace=True)

    def remove_tags(self, review, tags=[], byuser=None):
        """For the review entry identified by,
        `review` which can be,
            `id` or Review instance.
        remove tags specified by `tags`."""
        tagcomp = TagComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review, attrload=['project'])
        if review and tags:
            rmtags = tagcomp.model_remove_tags(tags, review, byuser)
        else:
            rmtags = []
        srchcomp = XSearchComponent(self.compmgr)
        review and rmtags and tlcomp.log(byuser, 'deleted tags, `%s`' % (', ').join(rmtags), review=review)
        srchcomp.indexreview([review], replace=True)

    def add_attach(self, review, attach, byuser=None):
        """Add attachment to the review identified by,
        `review` which can be,
            `id` or Review instance.
        `attach` can be
            `id` or `Attachment` instance."""
        attachcomp = AttachComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review, attrload=['project'])
        attach = attachcomp.get_attach(attach)
        if review and attach:
            attachcomp.model_add_attach(attach, review, byuser)
            tlcomp.log(byuser, 'uploaded attachment, `%s`' % attach.filename, review=review)

    def remove_attach(self, review, attach, byuser=None):
        """Remove attachment to the review identified by,
        `review` which can be,
            `id` or Review instance.
        `attach` can be
            `id` or `resource_url` or `Attachment` instance."""
        attachcomp = AttachComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        review = self.get_review(review)
        attach = attachcomp.get_attach(attach)
        if review and attach:
            attachcomp.model_remove_attach(attach, review, byuser)
            tlcomp.log(byuser, 'deleted attachment, `%s`' % attach.filename, review=review)

    def documentof(self, review, search='xapian'):
        """Make a document for 'review' entry to create a searchable index
            [ metadata, attributes, document ], where

            metadata   : { key, value } pairs to be associated with document
            attributes : searchable { key, value } pairs to be associated with
                         document
            document   : [ list , of, ... ] document string, with increasing
                         weightage
        """
        review = self.get_review(review, attrload=[
         'author', 'moderator', 'tags'])
        revusers = [
         review.author and review.author.username or '',
         review.moderator and review.moderator.username or '']
        tbl_participant = t_user.alias('participant')
        q = select([tbl_participant.c.username], bind=meta.engine).select_from(t_review.outerjoin(at_review_participants).outerjoin(tbl_participant, at_review_participants.c.participantid == tbl_participant.c.id)).where(t_review.c.id == review.id)
        [ revusers.append(tup[0]) for tup in q.execute().fetchall() if tup[0] ]
        tbl_commentor = t_user.alias('commentor')
        q = select([tbl_commentor.c.username, t_review_comment.c.text], bind=meta.engine).select_from(t_review.outerjoin(t_review_comment).outerjoin(at_review_commentors).outerjoin(tbl_commentor, at_review_commentors.c.commentorid == tbl_commentor.c.id)).where(t_review.c.id == review.id)
        cmttexts = []
        for tup in q.execute().fetchall():
            tup[0] and revusers.append(tup[0])
            tup[1] and cmttexts.append(tup[1])

        tagnames = [ t.tagname for t in review.tags ]
        metadata = {'doctype': 'review', 'id': review.id, 
           'projectname': review.project.projectname}
        attributes = search == 'xapian' and [
         'XID:review_%s' % review.id, 'XCLASS:review', 'XPROJECT:%s' % review.project.projectname] + [ 'XUSER:%s' % u for u in revusers ] + [ 'XTAG:%s' % t for t in tagnames
                                                                                                                                            ] or []
        attrs = (' ').join([
         review.project.projectname] + revusers + tagnames)
        document = [
         (' ').join(cmttexts), attrs]
        return [
         metadata, attributes, document]

    def guess_revwsource(self, review):
        """Guess the url source for the review and fetch the content."""
        config = self.compmgr.config
        projcomp = ProjectComponent(self.compmgr)
        vcscomp = VcsComponent(self.compmgr)
        wikicomp = WikiComponent(self.compmgr)
        review = review and self.get_review(review)
        url = review.resource_url
        difflno = None
        filelines = []
        if url[0] == '/':
            routes_map = config['routes.map']
            (d, robj) = routes_map.routematch(url)
            projectname = d.get('projectname', None)
            project = projectname and projcomp.get_project(projectname)
            if project:
                if robj.name == h.r_projwiki:
                    wikiurl = d.get('url', None)
                    try:
                        w = wikicomp.get_wiki(url)
                        wcnt_old = wikicomp.get_content(w, version=review.version - 1)
                        wcnt = wikicomp.get_content(w, version=review.version)
                        filelines = wcnt and wcnt.text.splitlines() or []
                        oldlines = wcnt_old and wcnt_old.text.splitlines() or []
                        difflno = h.wikidifflno(filelines, oldlines)
                    except:
                        raise

                elif robj.name == h.r_projvcsfile:
                    vcs_id = d.get('id', None)
                    filepath = d.get('filepath', '')
                    try:
                        vcs = vcs_id and vcscomp.get_vcs(int(vcs_id)) or None
                        vrep = va.open_repository(vcs)
                        fileurl = vrep.rooturl + '/' + filepath
                        filelines = vrep.file(fileurl, revno=review.version).cat(revno=review.version)
                    except:
                        pass
                    else:
                        filelines = [ l[1] for l in filelines ]

                    try:
                        difflno = h.udifftolno(vrep.diff(fileurl, review.version, review.version - 1))
                    except:
                        pass

        else:
            try:
                vrep = h.guessrep(url)
                filelines = vrep and vrep.file(url, revno=review.version).cat(revno=review.version) or []
            except:
                pass
            else:
                filelines = [ l[1] for l in filelines ]

            try:
                difflno = h.udifftolno(vrep.diff(url, review.version, review.version - 1))
            except:
                pass

            return (
             filelines, difflno)

    def upgradewiki(self, byuser='admin'):
        """Upgrade the database fields supporting wiki markup to the latest
        zwiki version"""
        tlcomp = TimelineComponent(self.compmgr)
        msession = meta.Session()
        rcmts = self.get_reviewcomment()
        with msession.begin(subtransactions=True):
            for rcmt in rcmts:
                rcmt.texthtml = rcmt.translate()

        tlcomp.log(byuser, 'Upgraded review comments to latest wiki')
        return len(rcmts)

    def allapproved(self, review):
        """Return a boolean indicating whether all review comments are
        approved"""
        review = self.get_review(review)
        rcmts = review.comments[:]
        primarycomments = []
        while rcmts:
            rcmt = rcmts[0]
            nreplies = []
            h.nestedreplies(rcmt, nreplies)
            rcmts.remove(rcmt)
            [ rcmts.remove(rrcmt) for rrcmt in nreplies if rrcmt in rcmts ]
            primarycomments.append(rcmt)

        return all([ cmt.approved for cmt in primarycomments ])

    def _naturenames(self):
        return [ rn.naturename for rn in self.get_reviewcomment_nature() ]

    def _actionnames(self):
        return [ ra.actionname for ra in self.get_reviewcomment_action() ]

    def reviewlist(self, project):
        """Collect a snap-shot of information for all project review"""
        tbl_author = t_user.alias('author')
        tbl_moderator = t_user.alias('moderator')
        oj = t_project.outerjoin(at_review_projects).outerjoin(t_review).outerjoin(at_reviewset_reviews).outerjoin(t_reviewset, t_reviewset.c.id == at_reviewset_reviews.c.reviewsetid).outerjoin(at_review_authors).outerjoin(tbl_author, at_review_authors.c.authorid == tbl_author.c.id).outerjoin(at_review_moderators, at_review_moderators.c.reviewid == t_review.c.id).outerjoin(tbl_moderator, at_review_moderators.c.moderatorid == tbl_moderator.c.id)
        q = select([t_review.c.id,
         t_review.c.resource_url,
         t_reviewset.c.name,
         t_reviewset.c.id,
         t_review.c.version,
         tbl_author.c.username,
         tbl_moderator.c.username,
         t_review.c.created_on], bind=meta.engine).select_from(oj).where(t_project.c.id == project.id)
        revwlist = dict([ (tup[0], list(tup)) for tup in q.execute().fetchall() if tup[0]
                        ])
        return revwlist

    def countcomments(self, r):
        """Count the number of comments for review 'r'"""
        id = isinstance(r, Review) and r.id or r
        oj = t_review_comment.outerjoin(t_review)
        q = select([t_review_comment.c.id], bind=meta.engine).select_from(oj).where(t_review.c.id == id)
        return len(q.execute().fetchall())

    def reviewopts(self, project):
        """Collect all the reviews for `project` and compose them for
        selectable options"""
        oj = t_project.outerjoin(at_review_projects).outerjoin(t_review)
        q = select([t_review.c.id, t_review.c.resource_url], bind=meta.engine).select_from(oj)
        qw = None
        if isinstance(project, (int, long)):
            qw = q.where(t_project.c.id == project)
        elif isinstance(project, (str, unicode)):
            qw = q.where(t_project.c.projectname == project)
        elif isinstance(project, Project):
            qw = q.where(t_project.c.id == project.id)
        return qw != None and [ tup for tup in qw.execute().fetchall() if tup[0] ] or []

    def reviewsproject(self):
        """Fetch a mapping of review id and project to which the review
        belongs to"""
        oj = t_review.outerjoin(at_review_projects).outerjoin(t_project)
        q = select([t_review.c.id, t_project.c.id, t_project.c.projectname], order_by=[
         desc(t_review.c.id)], bind=meta.engine).select_from(oj)
        res = [ tup for tup in q.execute().fetchall() if tup[0] if tup[1] ]
        return res

    def projectrset(self, project):
        """Collect all the review sets for `project` and compose them for
        selectable options"""
        oj = t_project.outerjoin(t_reviewset)
        q = select([t_reviewset.c.id, t_reviewset.c.name], bind=meta.engine).select_from(oj)
        qw = None
        if isinstance(project, (int, long)):
            qw = q.where(t_project.c.id == project)
        elif isinstance(project, (str, unicode)):
            qw = q.where(t_project.c.projectname == project)
        elif isinstance(project, Project):
            qw = q.where(t_project.c.id == project.id)
        return qw != None and [ tup for tup in qw.execute().fetchall() if tup[0] ] or []

    def reviewrcomments(self, review):
        """Collect review comments, in threaded mode"""
        oj = t_review.outerjoin(t_review_comment).outerjoin(t_reviewcomment_nature).outerjoin(t_reviewcomment_action).outerjoin(at_review_commentors, at_review_commentors.c.reviewcommentid == t_review_comment.c.id).outerjoin(t_user, at_review_commentors.c.commentorid == t_user.c.id).outerjoin(at_review_replies, t_review_comment.c.id == at_review_replies.c.reviewcommentid)
        q = select([t_review_comment.c.id,
         t_review_comment.c.position,
         t_review_comment.c.text,
         t_review_comment.c.texthtml,
         t_review_comment.c.approved,
         t_review_comment.c.created_on,
         t_user.c.username,
         t_reviewcomment_nature.c.naturename,
         t_reviewcomment_action.c.actionname,
         at_review_replies.c.replytoid], bind=meta.engine).select_from(oj).where(t_review.c.id == review.id)
        entries = q.execute().fetchall()
        res = dict([ (tup[0], list(tup) + [[]]) for tup in entries if tup[0]
                   ])
        [ res[res[id][9]][(-1)].append(res[id]) for id in res if res[id][9] ]

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

        return res

    def isfavorite(self, userid, reviewid):
        """Select whether the review is favorite for user"""
        q = select([at_review_favorites.c.reviewid, at_review_favorites.c.userid], bind=meta.engine).where(and_(at_review_favorites.c.reviewid == reviewid, at_review_favorites.c.userid == userid))
        return filter(None, q.execute().fetchall())

    def attachments(self, project):
        """Collect attachment list for all review,
        Return attachments"""
        oj = at_review_attachments.outerjoin(t_review).outerjoin(t_attachment).outerjoin(at_attachment_tags, at_attachment_tags.c.attachmentid == t_attachment.c.id).outerjoin(t_tag, at_attachment_tags.c.tagid == t_tag.c.id).outerjoin(at_attachment_uploaders, at_attachment_uploaders.c.attachmentid == t_attachment.c.id).outerjoin(t_user, at_attachment_uploaders.c.uploaderid == t_user.c.id).outerjoin(at_review_projects, at_review_projects.c.reviewid == t_review.c.id).outerjoin(t_project, at_review_projects.c.projectid == t_project.c.id)
        q = select([t_review.c.id, t_review.c.resource_url,
         t_attachment.c.id, t_attachment.c.filename,
         t_attachment.c.summary, t_attachment.c.download_count,
         t_attachment.c.created_on, t_user.c.username,
         t_tag.c.tagname], bind=meta.engine).select_from(oj).where(t_project.c.id == project.id)
        entries = q.execute().fetchall()
        result = {}
        for tup in entries:
            if tup[2] == None:
                continue
            fortck = result.get(tup[0:2], {})
            foratt = fortck.get(tup[2], [])
            if foratt:
                tup[8] and foratt[(-1)].append(tup[8])
            else:
                foratt = list(tup[3:8])
                foratt.append(tup[8] and [tup[8]] or [])
            fortck[tup[2]] = foratt
            result[tup[0:2]] = fortck

        return result

    def userasauthor(self, user):
        """List all the reviews authored by `user`"""
        oj = at_review_authors
        q = select([at_review_authors.c.reviewid], bind=meta.engine).select_from(oj).where(at_review_authors.c.authorid == user.id)
        revws = [ tup[0] for tup in q.execute().fetchall() if tup[0] ]
        return revws

    def userasmoderator(self, user):
        """List all the reviews moderated by `user`"""
        oj = at_review_moderators
        q = select([at_review_moderators.c.reviewid], bind=meta.engine).select_from(oj).where(at_review_moderators.c.moderatorid == user.id)
        revws = [ tup[0] for tup in q.execute().fetchall() if tup[0] ]
        return revws

    def userasparticipant(self, user):
        """List all the reviews participated by `user`"""
        oj = at_review_participants
        q = select([at_review_participants.c.reviewid], bind=meta.engine).select_from(oj).where(at_review_participants.c.participantid == user.id)
        revws = [ tup[0] for tup in q.execute().fetchall() if tup[0] ]
        return revws

    def usercomments(self, user):
        """List all the reviews comments by `user`"""
        oj = at_review_commentors
        q = select([at_review_commentors.c.reviewcommentid], bind=meta.engine).select_from(oj).where(at_review_commentors.c.commentorid == user.id)
        rcmts = [ tup[0] for tup in q.execute().fetchall() if tup[0] ]
        return rcmts

    actionnames = property(_actionnames)
    naturenames = property(_naturenames)