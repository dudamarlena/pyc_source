# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/niedbalski/src/vcs/vcs/utils/hgcompat.py
# Compiled at: 2016-04-08 09:25:43
"""
Mercurial libs compatibility
"""
from mercurial import archival, merge as hg_merge, patch, ui
from mercurial.commands import clone, nullid, pull
from mercurial.context import memctx, memfilectx
from mercurial.error import RepoError, RepoLookupError, Abort
from mercurial.hgweb.common import get_contact
from mercurial.localrepo import localrepository
from mercurial.match import match
from mercurial.mdiff import diffopts
from mercurial.node import hex
from mercurial.encoding import tolocal
from mercurial import discovery
from mercurial import localrepo
from mercurial import scmutil
from mercurial.discovery import findcommonoutgoing
from mercurial.util import url as hg_url
from mercurial.url import httpbasicauthhandler, httpdigestauthhandler