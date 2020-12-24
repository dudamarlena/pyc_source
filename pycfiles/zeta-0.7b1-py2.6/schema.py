# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/model/schema.py
# Compiled at: 2010-06-12 02:50:47
from datetime import datetime
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, Index
from sqlalchemy import Integer, String, Unicode, UnicodeText, Text, LargeBinary, PickleType, DateTime, Boolean
from zeta.model import meta
from zeta.lib.constants import *
import zeta.lib.helpers as h
__all__ = [
 'at_permission_maps', 'at_user_permissions', 'at_user_photos', 'at_user_icons',
 'at_permgroup_logs',
 't_permission_name', 't_permission_group',
 'at_user_logs',
 't_userrelation_type', 't_user', 't_user_info', 't_user_relation',
 'at_attachment_tags', 'at_attachment_uploaders', 'at_license_attachments',
 'at_license_tags', 'at_tag_logs', 'at_attachment_logs', 'at_license_logs',
 't_system', 't_staticwiki', 't_tag', 't_attachment', 't_license', 't_vote',
 'at_project_logos', 'at_project_icons', 'at_project_admins', 'at_project_licenses',
 'at_project_tags', 'at_component_tags', 'at_component_owners', 'at_milestone_tags',
 'at_version_tags', 'at_project_attachments', 'at_project_favorites',
 'at_project_logs',
 't_projectteam_type', 't_project', 't_project_info', 't_mailinglist', 't_ircchannel',
 't_component', 't_milestone', 't_version', 't_project_perm', 't_projectteam_perm',
 't_project_team',
 'at_ticket_projects', 'at_ticket_promptusers', 'at_ticketstatus_owners',
 'at_ticketcomment_authors', 'at_ticket_versions', 'at_ticket_milestones',
 'at_ticket_components', 'at_ticket_blockers', 'at_ticket_attachments', 'at_ticket_tags',
 'at_ticket_hier', 'at_ticket_replies', 'at_ticket_votes', 'at_ticket_favorites',
 'at_ticket_logs',
 't_ticket_status', 't_ticket_type', 't_ticket_severity', 't_ticket', 't_ticket_status_history',
 't_ticket_comment', 't_ticket_filter', 't_ticket_reference',
 'at_review_projects', 'at_review_authors', 'at_review_moderators', 'at_review_participants',
 'at_review_favorites', 'at_review_commentors', 'at_review_replies',
 'at_reviewset_reviews', 'at_review_attachments', 'at_review_tags', 'at_review_logs',
 't_reviewcomment_nature', 't_reviewcomment_action', 't_review',
 't_reviewset', 't_review_comment',
 'at_vcs_projects', 'at_vcs_logs', 't_vcs_type', 't_vcs', 't_vcsmount',
 'at_wiki_creators', 'at_wiki_commentors', 'at_wiki_attachments', 'at_wiki_tags',
 'at_wiki_projects', 'at_wiki_replies', 'at_wiki_votes', 'at_wiki_favorites',
 'at_wiki_logs',
 't_wiki_type', 't_wiki', 't_wikitable_map', 't_wiki_comment',
 'at_survey_votes', 'at_survey_moderators',
 't_timeline', 't_userinvitation',
 't_survey']
t_system = Table('system', meta.metadata, Column('id', Integer, primary_key=True), Column('field', Unicode(LEN_SYSFIELD), unique=True, nullable=False), Column('value', Unicode(LEN_SYSVALUE), nullable=False), mysql_engine='InnoDB')
t_staticwiki = Table('staticwiki', meta.metadata, Column('id', Integer, primary_key=True), Column('path', Unicode(LEN_RESOURCEURL), unique=True), Column('text', UnicodeText(LEN_DESCRIBE)), Column('texthtml', UnicodeText(LEN_DESCRIBE * 2)), mysql_engine='InnoDB')
at_permission_maps = Table('permission_maps', meta.metadata, Column('groupid', None, ForeignKey('permission_group.id'), nullable=False), Column('permid', None, ForeignKey('permission_name.id'), nullable=False), mysql_engine='InnoDB')
at_permgroup_logs = Table('permgroup_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('groupid', None, ForeignKey('permission_group.id'), nullable=False), mysql_engine='InnoDB')
t_permission_name = Table('permission_name', meta.metadata, Column('id', Integer, primary_key=True), Column('perm_name', String(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_permission_group = Table('permission_group', meta.metadata, Column('id', Integer, primary_key=True), Column('perm_group', String(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
at_user_permissions = Table('user_permissions', meta.metadata, Column('userid', None, ForeignKey('user.id'), nullable=False), Column('groupid', None, ForeignKey('permission_group.id'), nullable=False), mysql_engine='InnoDB')
at_user_photos = Table('user_photos', meta.metadata, Column('userid', None, ForeignKey('user.id'), nullable=False), Column('attachid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_user_icons = Table('user_icons', meta.metadata, Column('userid', None, ForeignKey('user.id'), nullable=False), Column('attachid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_user_logs = Table('user_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('userid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
t_userrelation_type = Table('userrelation_type', meta.metadata, Column('id', Integer, primary_key=True), Column('userrel_type', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_user = Table('user', meta.metadata, Column('id', Integer, primary_key=True), Column('username', Unicode(LEN_NAME), unique=True, nullable=False), Column('emailid', Unicode(LEN_EMAILID), nullable=False), Column('password', LargeBinary(256)), Column('timezone', String(LEN_TZ), default='UTC'), Column('disabled', Boolean, default=False), mysql_engine='InnoDB')
t_user_info = Table('user_info', meta.metadata, Column('id', Integer, nullable=False, primary_key=True), Column('user_id', None, ForeignKey('user.id'), nullable=False), Column('firstname', Unicode(LEN_NAME)), Column('middlename', Unicode(LEN_NAME)), Column('lastname', Unicode(LEN_NAME)), Column('addressline1', Unicode(LEN_ADDRLINE)), Column('addressline2', Unicode(LEN_ADDRLINE)), Column('city', Unicode(LEN_NAME)), Column('pincode', String(LEN_PINCODE)), Column('state', Unicode(LEN_NAME)), Column('country', Unicode(LEN_NAME)), Column('userpanes', Unicode(LEN_256), default='siteuserpanes'), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_user_relation = Table('user_relation', meta.metadata, Column('id', Integer, nullable=False, primary_key=True), Column('userfrom_id', None, ForeignKey('user.id'), nullable=False, index=True), Column('userto_id', None, ForeignKey('user.id'), nullable=False, index=True), Column('userreltype_id', None, ForeignKey('userrelation_type.id'), nullable=False, index=True), Column('approved', Boolean, default=False), mysql_engine='InnoDB')
Index('idx_user_fromtorel', t_user_relation.c.userfrom_id, t_user_relation.c.userto_id, t_user_relation.c.userreltype_id)
at_attachment_tags = Table('attachment_tags', meta.metadata, Column('attachmentid', None, ForeignKey('attachment.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_attachment_uploaders = Table('attachment_uploaders', meta.metadata, Column('attachmentid', None, ForeignKey('attachment.id'), nullable=False), Column('uploaderid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_license_attachments = Table('license_attachments', meta.metadata, Column('licenseid', None, ForeignKey('license.id'), nullable=False), Column('attachmentid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_license_tags = Table('license_tags', meta.metadata, Column('licenseid', None, ForeignKey('license.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_tag_logs = Table('tag_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_attachment_logs = Table('attachment_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('attachid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_license_logs = Table('license_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('licenseid', None, ForeignKey('license.id'), nullable=False), mysql_engine='InnoDB')
t_tag = Table('tag', meta.metadata, Column('id', Integer, primary_key=True), Column('tagname', Unicode(LEN_TAGNAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_attachment = Table('attachment', meta.metadata, Column('id', Integer, primary_key=True), Column('summary', Unicode(LEN_SUMMARY)), Column('filename', String(LEN_RESOURCEURL), nullable=False), Column('content', LargeBinary(LEN_ATTACHSIZE)), Column('download_count', Integer, default=0), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_license = Table('license', meta.metadata, Column('id', Integer, primary_key=True), Column('licensename', Unicode(LEN_LICENSENAME), unique=True, nullable=False, index=True), Column('summary', Unicode(LEN_SUMMARY), nullable=False), Column('text', UnicodeText(LEN_DESCRIBE), nullable=False), Column('source', Unicode(LEN_LICENSESOURCE), nullable=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_vote = Table('vote', meta.metadata, Column('id', Integer, primary_key=True), Column('user_id', None, ForeignKey('user.id'), nullable=False), Column('votedas', Unicode(LEN_NAME)), Column('medium', Unicode(LEN_NAME)), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
at_project_logos = Table('project_logos', meta.metadata, Column('projectid', None, ForeignKey('project.id'), nullable=False), Column('attachid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_project_icons = Table('project_icons', meta.metadata, Column('projectid', None, ForeignKey('project.id'), nullable=False), Column('attachid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_project_admins = Table('project_admins', meta.metadata, Column('projectid', None, ForeignKey('project.id'), nullable=False), Column('adminid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_project_licenses = Table('project_licenses', meta.metadata, Column('projectid', None, ForeignKey('project.id'), nullable=False), Column('license_id', None, ForeignKey('license.id'), nullable=False), mysql_engine='InnoDB')
at_project_tags = Table('project_tags', meta.metadata, Column('projectid', None, ForeignKey('project.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_component_owners = Table('component_owners', meta.metadata, Column('componentid', None, ForeignKey('component.id'), nullable=False), Column('ownerid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_component_tags = Table('component_tags', meta.metadata, Column('componentid', None, ForeignKey('component.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_milestone_tags = Table('milestone_tags', meta.metadata, Column('milestoneid', None, ForeignKey('milestone.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_version_tags = Table('version_tags', meta.metadata, Column('versionid', None, ForeignKey('version.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_project_attachments = Table('project_attachments', meta.metadata, Column('projectid', None, ForeignKey('project.id'), nullable=False), Column('attachmentid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_project_favorites = Table('project_favorites', meta.metadata, Column('projectid', None, ForeignKey('project.id'), nullable=False), Column('userid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_project_logs = Table('project_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('projectid', None, ForeignKey('project.id'), nullable=False), mysql_engine='InnoDB')
t_projectteam_type = Table('projectteam_type', meta.metadata, Column('id', Integer, primary_key=True), Column('team_type', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_project = Table('project', meta.metadata, Column('id', Integer, primary_key=True), Column('projectname', Unicode(LEN_NAME), unique=True, nullable=False, index=True), Column('summary', Unicode(LEN_SUMMARY), nullable=False), Column('admin_email', Unicode(LEN_EMAILID), nullable=False), Column('exposed', Boolean, default=True), Column('disabled', Boolean, default=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_project_info = Table('project_info', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id'), unique=True, nullable=False, index=True), Column('description', UnicodeText(LEN_DESCRIBE), nullable=False), Column('descriptionhtml', UnicodeText(LEN_DESCRIBE * 2)), mysql_engine='InnoDB')
t_mailinglist = Table('mailinglist', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id')), Column('mailing_list', Unicode(LEN_EMAILID)), mysql_engine='InnoDB')
t_ircchannel = Table('ircchannel', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id')), Column('ircchannel', Unicode(LEN_EMAILID)), mysql_engine='InnoDB')
t_component = Table('component', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id'), nullable=False), Column('componentname', Unicode(LEN_NAME), nullable=False), Column('comp_number', Integer, nullable=False), Column('description', UnicodeText(LEN_DESCRIBE), nullable=False), Column('descriptionhtml', UnicodeText(LEN_DESCRIBE * 2)), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_milestone = Table('milestone', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id'), nullable=False), Column('milestone_name', Unicode(LEN_NAME1), nullable=False), Column('mstn_number', Integer, nullable=False), Column('description', UnicodeText(LEN_DESCRIBE), nullable=False), Column('descriptionhtml', UnicodeText(LEN_DESCRIBE * 2)), Column('due_date', PickleType()), Column('closing_remark', UnicodeText(LEN_DESCRIBE), default=''), Column('closing_remarkhtml', UnicodeText(LEN_DESCRIBE * 2)), Column('completed', Boolean, default=False), Column('cancelled', Boolean, default=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_version = Table('version', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id'), nullable=False), Column('version_name', Unicode(LEN_NAME1), nullable=False), Column('ver_number', Integer, nullable=False), Column('description', UnicodeText(LEN_DESCRIBE), nullable=False), Column('descriptionhtml', UnicodeText(LEN_DESCRIBE * 2)), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_project_perm = Table('project_perm', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id'), nullable=False), Column('user_id', None, ForeignKey('user.id'), nullable=False), Column('perm_group_id', ForeignKey('permission_group.id'), nullable=False), mysql_engine='InnoDB')
t_projectteam_perm = Table('projectteam_perm', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id'), nullable=False), Column('teamtype_id', None, ForeignKey('projectteam_type.id'), nullable=False), Column('perm_group_id', None, ForeignKey('permission_group.id'), nullable=False), mysql_engine='InnoDB')
t_project_team = Table('project_team', meta.metadata, Column('id', Integer, nullable=False, primary_key=True), Column('user_id', None, ForeignKey('user.id'), nullable=False), Column('project_id', None, ForeignKey('project.id'), nullable=False), Column('teamtype_id', None, ForeignKey('projectteam_type.id'), nullable=False), Column('approved', Boolean, default=False), mysql_engine='InnoDB')
at_ticket_projects = Table('ticket_projects', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('projectid', None, ForeignKey('project.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_promptusers = Table('ticket_promptusers', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('promptuserid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_components = Table('ticket_components', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('componentid', None, ForeignKey('component.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_milestones = Table('ticket_milestones', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('milestoneid', None, ForeignKey('milestone.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_versions = Table('ticket_versions', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('versionid', None, ForeignKey('version.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_blockers = Table('ticket_blockers', meta.metadata, Column('blockedbyid', None, ForeignKey('ticket.id'), nullable=False), Column('blockingid', None, ForeignKey('ticket.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_hier = Table('ticket_hier', meta.metadata, Column('partckid', None, ForeignKey('ticket.id'), nullable=False), Column('childtckid', None, ForeignKey('ticket.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_tags = Table('ticket_tags', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_attachments = Table('ticket_attachments', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('attachmentid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_ticketstatus_owners = Table('ticketstatus_owners', meta.metadata, Column('ticketstatusid', None, ForeignKey('ticket_status_history.id'), nullable=False), Column('ownerid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_ticketcomment_authors = Table('ticketcomment_authors', meta.metadata, Column('ticketcommentid', None, ForeignKey('ticket_comment.id'), nullable=False), Column('authorid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_replies = Table('ticket_replies', meta.metadata, Column('ticketcommentid', None, ForeignKey('ticket_comment.id'), nullable=False), Column('replytoid', None, ForeignKey('ticket_comment.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_votes = Table('ticket_votes', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('voteid', None, ForeignKey('vote.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_favorites = Table('ticket_favorites', meta.metadata, Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), Column('userid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_ticket_logs = Table('ticket_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('ticketid', None, ForeignKey('ticket.id'), nullable=False), mysql_engine='InnoDB')
t_ticket_status = Table('ticket_status', meta.metadata, Column('id', Integer, primary_key=True), Column('tck_statusname', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_ticket_type = Table('ticket_type', meta.metadata, Column('id', Integer, primary_key=True), Column('tck_typename', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_ticket_severity = Table('ticket_severity', meta.metadata, Column('id', Integer, primary_key=True), Column('tck_severityname', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_ticket = Table('ticket', meta.metadata, Column('id', Integer, primary_key=True), Column('ticket_number', Integer, nullable=False), Column('summary', Unicode(LEN_SUMMARY), nullable=False), Column('description', UnicodeText(LEN_DESCRIBE)), Column('descriptionhtml', UnicodeText(LEN_DESCRIBE * 2)), Column('type_id', None, ForeignKey('ticket_type.id'), nullable=False), Column('severity_id', None, ForeignKey('ticket_severity.id'), nullable=False), Column('tsh_id', Integer), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_ticket_status_history = Table('ticket_status_history', meta.metadata, Column('id', Integer, primary_key=True), Column('ticket_id', None, ForeignKey('ticket.id'), nullable=False), Column('status_id', None, ForeignKey('ticket_status.id'), nullable=False), Column('due_date', PickleType()), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_ticket_comment = Table('ticket_comment', meta.metadata, Column('id', Integer, primary_key=True), Column('ticket_id', None, ForeignKey('ticket.id'), nullable=False), Column('text', UnicodeText(LEN_DESCRIBE), nullable=False), Column('texthtml', UnicodeText(LEN_DESCRIBE * 2)), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_ticket_filter = Table('ticket_filter', meta.metadata, Column('id', Integer, primary_key=True), Column('name', Unicode(LEN_256), nullable=False), Column('user_id', None, ForeignKey('user.id'), nullable=False), Column('filterbyjson', Unicode(LEN_QUERYSTRING)), mysql_engine='InnoDB')
t_ticket_reference = Table('ticket_reference', meta.metadata, Column('id', Integer, primary_key=True), Column('ticket_id', None, ForeignKey('ticket.id'), nullable=False), Column('resource_url', Unicode(LEN_RESOURCEURL), nullable=False), mysql_engine='InnoDB')
at_vcs_projects = Table('vcs_projects', meta.metadata, Column('vscid', None, ForeignKey('vcs.id'), nullable=False), Column('projectid', None, ForeignKey('project.id'), nullable=False), mysql_engine='InnoDB')
at_vcs_logs = Table('vcs_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('vcsid', None, ForeignKey('vcs.id'), nullable=False), mysql_engine='InnoDB')
t_vcs_type = Table('vcs_type', meta.metadata, Column('id', Integer, primary_key=True), Column('vcs_typename', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_vcs = Table('vcs', meta.metadata, Column('id', Integer, primary_key=True), Column('type_id', None, ForeignKey('vcs_type.id'), nullable=False), Column('name', Unicode(LEN_NAME), nullable=False), Column('rooturl', Unicode(LEN_RESOURCEURL), nullable=False), Column('loginname', Unicode(LEN_NAME)), Column('password', Unicode(LEN_NAME)), Column('created_on', DateTime(timezone=True), default=datetime.utcnow), mysql_engine='InnoDB')
t_vcsmount = Table('vcsmount', meta.metadata, Column('id', Integer, primary_key=True), Column('name', Unicode(LEN_NAME), nullable=False), Column('content', Unicode(LEN_NAME), nullable=False), Column('vcs_id', None, ForeignKey('vcs.id')), Column('repospath', Unicode(LEN_RESOURCEURL), nullable=False), Column('created_on', DateTime(timezone=True), default=datetime.utcnow), mysql_engine='InnoDB')
at_review_projects = Table('review_projects', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('projectid', None, ForeignKey('project.id'), nullable=False), mysql_engine='InnoDB')
at_review_authors = Table('review_authors', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('authorid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_review_moderators = Table('review_moderators', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('moderatorid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_review_participants = Table('review_participants', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('participantid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_review_favorites = Table('review_favorites', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('userid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_review_commentors = Table('review_commentors', meta.metadata, Column('reviewcommentid', None, ForeignKey('review_comment.id'), nullable=False), Column('commentorid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_review_replies = Table('review_replies', meta.metadata, Column('reviewcommentid', None, ForeignKey('review_comment.id'), nullable=False), Column('replytoid', None, ForeignKey('review_comment.id'), nullable=False), mysql_engine='InnoDB')
at_reviewset_reviews = Table('reviewset_reviews', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('reviewsetid', None, ForeignKey('reviewset.id'), nullable=False), mysql_engine='InnoDB')
at_review_attachments = Table('review_attachments', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('attachmentid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_review_tags = Table('review_tags', meta.metadata, Column('reviewid', None, ForeignKey('review.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_review_logs = Table('review_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('reviewid', None, ForeignKey('review.id'), nullable=False), mysql_engine='InnoDB')
t_reviewcomment_nature = Table('reviewcomment_nature', meta.metadata, Column('id', Integer, primary_key=True), Column('naturename', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_reviewcomment_action = Table('reviewcomment_action', meta.metadata, Column('id', Integer, primary_key=True), Column('actionname', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_review = Table('review', meta.metadata, Column('id', Integer, primary_key=True), Column('review_number', Integer, nullable=False), Column('resource_url', Unicode(LEN_RESOURCEURL), nullable=False), Column('version', Integer), Column('closed', Boolean, default=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_reviewset = Table('reviewset', meta.metadata, Column('id', Integer, primary_key=True), Column('project_id', None, ForeignKey('project.id'), nullable=False), Column('name', Unicode(LEN_NAME), nullable=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_review_comment = Table('review_comment', meta.metadata, Column('id', Integer, primary_key=True), Column('review_id', None, ForeignKey('review.id'), nullable=False), Column('nature_id', None, ForeignKey('reviewcomment_nature.id')), Column('position', Integer), Column('text', UnicodeText(LEN_DESCRIBE), nullable=False), Column('texthtml', UnicodeText(LEN_DESCRIBE * 2)), Column('action_id', None, ForeignKey('reviewcomment_action.id')), Column('approved', Boolean, default=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
at_wiki_creators = Table('wiki_creators', meta.metadata, Column('wikiid', None, ForeignKey('wiki.id'), nullable=False), Column('creatorid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_projects = Table('wiki_projects', meta.metadata, Column('wikiid', None, ForeignKey('wiki.id'), nullable=False), Column('projectid', None, ForeignKey('project.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_attachments = Table('wiki_attachments', meta.metadata, Column('wikiid', None, ForeignKey('wiki.id'), nullable=False), Column('attachmentid', None, ForeignKey('attachment.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_tags = Table('wiki_tags', meta.metadata, Column('wikiid', None, ForeignKey('wiki.id'), nullable=False), Column('tagid', None, ForeignKey('tag.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_commentors = Table('wiki_commentors', meta.metadata, Column('wikicommentid', None, ForeignKey('wiki_comment.id'), nullable=False), Column('commentorid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_replies = Table('wiki_replies', meta.metadata, Column('wikicommentid', None, ForeignKey('wiki_comment.id'), nullable=False), Column('replytoid', None, ForeignKey('wiki_comment.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_votes = Table('wiki_votes', meta.metadata, Column('wikiid', None, ForeignKey('wiki.id'), nullable=False), Column('voteid', None, ForeignKey('vote.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_favorites = Table('wiki_favorites', meta.metadata, Column('wikiid', None, ForeignKey('wiki.id'), nullable=False), Column('userid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
at_wiki_logs = Table('wiki_logs', meta.metadata, Column('timelineid', None, ForeignKey('timeline.id'), nullable=False), Column('wikiid', None, ForeignKey('wiki.id'), nullable=False), mysql_engine='InnoDB')
t_wiki_type = Table('wiki_type', meta.metadata, Column('id', Integer, primary_key=True), Column('wiki_typename', Unicode(LEN_NAME), unique=True, nullable=False), mysql_engine='InnoDB')
t_wiki = Table('wiki', meta.metadata, Column('id', Integer, primary_key=True), Column('wikiurl', Unicode(LEN_RESOURCEURL), unique=True, nullable=False), Column('type_id', None, ForeignKey('wiki_type.id'), nullable=False), Column('summary', Unicode(LEN_SUMMARY)), Column('latest_version', Integer), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_wikitable_map = Table('wikitable_map', meta.metadata, Column('id', Integer, primary_key=True), Column('wiki_id', None, ForeignKey('wiki.id'), nullable=False), Column('table_pagenum', Integer, nullable=False), mysql_engine='InnoDB')
t_wiki_comment = Table('wiki_comment', meta.metadata, Column('id', Integer, primary_key=True), Column('wiki_id', None, ForeignKey('wiki.id'), nullable=False), Column('version_id', Integer), Column('text', UnicodeText(LEN_DESCRIBE), nullable=False), Column('texthtml', UnicodeText(LEN_DESCRIBE * 2)), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')

def t_wikipage(table_pagenum):
    return Table('wikipage' + str(table_pagenum), meta.metadata, Column('id', Integer, primary_key=True), Column('text', UnicodeText(LEN_DESCRIBE), nullable=False), Column('texthtml', UnicodeText(LEN_DESCRIBE * 2)), Column('author', Unicode(LEN_NAME), nullable=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')


t_timeline = Table('timeline', meta.metadata, Column('id', Integer, primary_key=True), Column('log', Unicode(LEN_1K), nullable=False), Column('userhtml', Unicode(LEN_RESOURCEURL)), Column('itemhtml', Unicode(LEN_1K)), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
t_userinvitation = Table('userinvitation', meta.metadata, Column('id', Integer, primary_key=True), Column('byuser_id', None, ForeignKey('user.id')), Column('emailid', Unicode(LEN_EMAILID), nullable=False), Column('digest', LargeBinary(256), nullable=False), Column('acceptedby', Unicode(LEN_NAME)), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')
at_survey_votes = Table('survey_votes', meta.metadata, Column('surveyid', None, ForeignKey('survey.id'), nullable=False), Column('voteid', None, ForeignKey('vote.id'), nullable=False), mysql_engine='InnoDB')
at_survey_moderators = Table('survey_moderators', meta.metadata, Column('surveyid', None, ForeignKey('survey.id'), nullable=False), Column('moderatorid', None, ForeignKey('user.id'), nullable=False), mysql_engine='InnoDB')
t_survey = Table('survey', meta.metadata, Column('id', Integer, primary_key=True), Column('name', Unicode(LEN_NAME), unique=True, nullable=False), Column('question', Unicode(LEN_SUMMARY)), Column('options', Unicode(LEN_1K)), Column('start_time', PickleType()), Column('end_time', PickleType()), Column('anonymous', Boolean, default=False), Column('created_on', DateTime(timezone=True), default=h.utcnow), mysql_engine='InnoDB')