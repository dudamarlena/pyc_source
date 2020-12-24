# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/constants.py
# Compiled at: 2019-03-11 23:04:44
from jirafs import __version__ as version
TICKET_DETAILS = 'fields.jira'
TICKET_COMMENTS = 'comments.read_only.jira'
TICKET_NEW_COMMENT = 'new_comment.jira'
TICKET_LINKS = 'links.jira'
TICKET_FILE_FIELD_TEMPLATE = '{field_name}.jira'
LOCAL_ONLY_FILE = '.jirafs_local'
REMOTE_IGNORE_FILE = '.jirafs_remote_ignore'
GIT_IGNORE_FILE_PARTIAL = '.jirafs_ignore'
GIT_IGNORE_FILE = '.jirafs/combined_ignore'
GIT_EXCLUDE_FILE = '.jirafs/git/info/exclude'
TICKET_OPERATION_LOG = 'operation.log'
METADATA_DIR = '.jirafs'
GLOBAL_CONFIG = '.jirafs_config'
GIT_AUTHOR = 'Jirafs %s <jirafs@localhost>' % version
CONFIG_JIRA = 'jira'
CONFIG_MAIN = 'main'
CONFIG_PLUGINS = 'plugins'
NO_DETAIL_FIELDS = [
 'comment',
 'watches',
 'attachment']
FILE_FIELDS = [
 'description']
FILE_FIELD_BLACKLIST = [
 'new_comment',
 'fields',
 'links']
ALLOW_USER_INPUT = True
CURRENT_REPO_VERSION = 16
from environmental_override import override
override(locals(), 'JIRAFS_')