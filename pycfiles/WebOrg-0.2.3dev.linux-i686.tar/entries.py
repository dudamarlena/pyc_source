# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/controllers/entries.py
# Compiled at: 2011-07-19 05:59:06
import logging, json
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.templating import render_jinja2
from weborg.lib.base import BaseController
from weborg.lib import client
log = logging.getLogger(__name__)

class EntriesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='html'):
        """GET /entries: All items in the collection"""
        if format == 'json':
            return client.entry_index()
        if format == 'html':
            c.heading = 'index'
            c.items = [ json.loads(client.entry_show(eid)) for eid in json.loads(client.entry_index())
                      ]
            return render_jinja2('entry-list.html')

    def create(self, id, format='json'):
        """POST /entries/{id}.json: Create a new item"""
        return client.entry_create(id, json.dumps(request.params))

    def new(self, id, format='html'):
        """GET /entries/{id}/new.html: Form to create a new item"""
        c.back = url.current(id=id)
        c.items = json.loads(client.entry_new(id))
        print c.items
        return render_jinja2('entry-new-or-edit.html')

    def update(self, id):
        """PUT /entries/id: Update an existing item"""
        pass

    def delete(self, id):
        """DELETE /entries/id: Delete an existing item"""
        pass

    def show(self, id, format='html'):
        """GET /entries/id: Show a specific item"""
        if format == 'json':
            return client.entry_show(id)
        if format == 'html':
            entry = json.loads(client.entry_show(id))
            c.id = id
            c.back = url.current(id=entry['parent'])
            c.heading = entry['heading']
            if entry['children']:
                c.items = [ json.loads(client.entry_show(child)) for child in entry['children'] ]
            return render_jinja2('entry-list.html')

    def edit(self, id, format='html'):
        """GET /entries/id/edit: Form to edit an existing item"""
        pass