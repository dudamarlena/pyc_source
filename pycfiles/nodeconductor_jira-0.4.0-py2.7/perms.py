# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/perms.py
# Compiled at: 2016-09-16 10:02:59
from nodeconductor.structure import perms as structure_perms
PERMISSION_LOGICS = (
 (
  'nodeconductor_jira.JiraService', structure_perms.service_permission_logic),
 (
  'nodeconductor_jira.JiraServiceProjectLink', structure_perms.service_project_link_permission_logic),
 (
  'nodeconductor_jira.Project', structure_perms.resource_permission_logic),
 (
  'nodeconductor_jira.Issue', structure_perms.property_permission_logic('project', user_field='user')),
 (
  'nodeconductor_jira.Comment', structure_perms.property_permission_logic('issue__project', user_field='user')),
 (
  'nodeconductor_jira.Attachment', structure_perms.property_permission_logic('issue__project', user_field='user')))