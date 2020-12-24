# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/global_symbols.py
# Compiled at: 2008-05-20 04:51:58
__doc__ = '\n\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
import os, string, Log
if os.path.isfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'debug.txt')):
    Log.LOG_LEVEL = Log.LOG_DEBUG
    DEBUG_MODE = 1
else:
    Log.LOG_LEVEL = Log.LOG_NOTICE
    DEBUG_MODE = 0
from Log import *
if os.path.isfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version.txt')):
    __version_file_ = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version.txt'), 'r')
    version__ = __version_file_.read()[:-1]
    __version_file_.close()
else:
    version__ = '(UNKNOWN)'
PREVIEW_PLONE21_IN_PLONE20_ = 0
splitdir = os.path.split(os.path.abspath(os.path.dirname(__file__)))
products = os.path.join(*splitdir[:-1])
version_file = os.path.join(products, 'CMFPlone', 'version.txt')
if os.path.isfile(version_file):
    f = open(version_file, 'r')
    v = f.read()
    f.close()
    if string.find(v, '2.0.') != -1:
        PREVIEW_PLONE21_IN_PLONE20_ = 1
GROUP_PREFIX = 'group_'
GROUP_PREFIX_LEN = len(GROUP_PREFIX)
MAX_USERS_PER_PAGE = 100
MAX_TREE_USERS_AND_GROUPS = 100
TREE_CACHE_TIME = 10
INVALID_USER_NAMES = [
 'BASEPATH1', 'BASEPATH2', 'BASEPATH3', 'a_', 'URL', 'acl_users', 'misc_', 'management_view', 'management_page_charset', 'REQUEST', 'RESPONSE', 'MANAGE_TABS_NO_BANNER', 'tree-item-url', 'SCRIPT_NAME', 'n_', 'help_topic', 'Zope-Version', 'target']
LDAPUF_METHOD = 'manage_addLDAPSchemaItem'
LDAP_GROUP_RDN = 'cn'
LOCALROLE_BLOCK_PROPERTY = '__ac_local_roles_block__'