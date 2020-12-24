# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/coremods/permissions.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 2742 bytes
__doc__ = '\npermissions.py - Permissions Abstraction for PyLink IRC Services.\n'
import threading
from collections import defaultdict
from pylinkirc import conf, utils
from pylinkirc.log import log
default_permissions = defaultdict(set)

def add_default_permissions(perms):
    """Adds default permissions to the index."""
    global default_permissions
    for target, permlist in perms.items():
        default_permissions[target] |= set(permlist)


addDefaultPermissions = add_default_permissions

def remove_default_permissions(perms):
    """Remove default permissions from the index."""
    for target, permlist in perms.items():
        default_permissions[target] -= set(permlist)


removeDefaultPermissions = remove_default_permissions

def check_permissions(irc, uid, perms, also_show=[]):
    """
    Checks permissions of the caller. If the caller has any of the permissions listed in perms,
    this function returns True. Otherwise, NotAuthorizedError is raised.
    """
    olduser = conf.conf['login'].get('user')
    if olduser:
        if irc.match_host('$pylinkacc:%s' % olduser, uid):
            log.debug('permissions: overriding permissions check for old-style admin user %s', irc.get_hostmask(uid))
            return True
    permissions = defaultdict(set)
    for k, v in (conf.conf.get('permissions') or {}).items():
        permissions[k] |= set(v)

    if conf.conf.get('permissions_merge_defaults', True):
        for k, v in default_permissions.items():
            permissions[k] |= v

    for host, permlist in permissions.items():
        log.debug('permissions: permlist for %s: %s', host, permlist)
        if irc.match_host(host, uid):
            for perm in permlist:
                log.debug('permissions: checking if %s glob matches anything in %s', perm, permlist)
                if any(irc.match_host(perm, p) for p in perms):
                    return True

    raise utils.NotAuthorizedError('You are missing one of the following permissions: %s' % ', '.join(perms + also_show))


checkPermissions = check_permissions