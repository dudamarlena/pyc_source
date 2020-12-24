# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/controllers/admin/auth_user.py
# Compiled at: 2005-08-12 03:13:27
"""
 genere par la commande "paster restcontroller admin_user admin.auth_user"

"""
import logging
from authproxy.lib.base import *
log = logging.getLogger('authproxy')

def parse_query_string(content):
    """
        parse a string like that into
        username=me&password=me&group=guest&roles=admin&roles=reviewer
    ((username,me),(group,guest),(roles,admin)(roles,reviewer)
    
    """
    result = []
    entries = content.split('&')
    for e in entries:
        (k, v) = e.split('=')
        result.append([k, v])

    return result


class AuthUserController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='html'):
        """GET /admin_auth_user: All items in the collection."""
        return 'admin auth user Page'

    def create(self):
        """POST /admin_auth_user: Create a new item."""
        log.debug('create a user')
        return self.show('new_user')

    def new(self, format='html'):
        """GET /admin_auth_user/new: Form to create a new item."""
        log.debug('form for a new user')
        c.users = request.environ['authkit.users']
        return render('genshi', 'user')

    def update(self, id):
        """PUT /admin_auth_user/id: Update an existing item."""
        pass

    def delete(self, id):
        """DELETE /admin_auth_user/id: Delete an existing item."""
        pass

    def show(self, id, format='html'):
        """GET /admin_auth_user/id: Show a specific item."""
        log.debug('show user id:%s' % id)
        return 'auth user show %s' % id

    def edit(self, id, format='html'):
        """GET /admin_auth_user/id;edit: Form to edit an existing item."""
        pass