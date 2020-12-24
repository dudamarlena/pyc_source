# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/controllers/admin/auth_group.py
# Compiled at: 2005-08-12 03:13:27
import logging
from authproxy.lib.base import *
log = logging.getLogger(__name__)

class AuthGroupController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='html'):
        """GET /admin_auth_group: All items in the collection."""
        pass

    def create(self):
        """POST /admin_auth_group: Create a new item."""
        pass

    def new(self, format='html'):
        """GET /admin_auth_group/new: Form to create a new item."""
        pass

    def update(self, id):
        """PUT /admin_auth_group/id: Update an existing item."""
        pass

    def delete(self, id):
        """DELETE /admin_auth_group/id: Delete an existing item."""
        pass

    def show(self, id, format='html'):
        """GET /admin_auth_group/id: Show a specific item."""
        pass

    def edit(self, id, format='html'):
        """GET /admin_auth_group/id;edit: Form to edit an existing item."""
        pass