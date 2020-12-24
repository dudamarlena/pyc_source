# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesitetemplate/template/+package+/lib/auth.py
# Compiled at: 2008-11-09 19:58:03
from authkit.permissions import ValidAuthKitUser
from authkit.permissions import HasAuthKitRole
from authkit.authorize.pylons_adaptors import authorized
from pylons.templating import render_mako as render
from authkit.authorize.pylons_adaptors import authorize
is_valid_user = ValidAuthKitUser()
has_delete_role = HasAuthKitRole(['delete'])

def render_signin():
    return render('/derived/account/signin.html').encode('utf-8')