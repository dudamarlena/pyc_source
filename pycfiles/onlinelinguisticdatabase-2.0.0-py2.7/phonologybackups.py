# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/phonologybackups.py
# Compiled at: 2016-09-19 13:27:02
"""Contains the :class:`PhonologybackupsController`.

.. module:: phonologybackups
   :synopsis: Contains the phonology backups controller.

"""
import logging
from pylons import request, response, config
from formencode.validators import Invalid
from onlinelinguisticdatabase.lib.base import BaseController
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
from onlinelinguisticdatabase.model.meta import Session
from onlinelinguisticdatabase.model import PhonologyBackup
log = logging.getLogger(__name__)

class PhonologybackupsController(BaseController):
    """Generate responses to requests on phonology backup resources.

    REST Controller styled on the Atom Publishing Protocol.

    .. note::

       The ``h.jsonify`` decorator converts the return value of the methods to
       JSON.

    .. note::
    
        Phonology backups are created when updating and deleting phonologies;
        they cannot be created directly and they should never be deleted.  This
        controller facilitates retrieval of phonology backups only.

    """
    query_builder = SQLAQueryBuilder('PhonologyBackup', config=config)

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def index(self):
        """Get all phonology backup resources.

        :URL: ``GET /phonologybackups`` 
        :returns: a list of all phonology backup resources.

        """
        try:
            query = Session.query(PhonologyBackup)
            query = h.add_order_by(query, dict(request.GET), self.query_builder)
            return h.add_pagination(query, dict(request.GET))
        except Invalid as e:
            response.status_int = 400
            return {'errors': e.unpack_errors()}

    @h.jsonify
    def create(self):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}

    @h.jsonify
    def new(self, format='html'):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}

    @h.jsonify
    def update(self, id):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}

    @h.jsonify
    def delete(self, id):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def show(self, id):
        """Return a phonology backup.

        :URL: ``GET /phonologybackups/id``
        :param str id: the ``id`` value of the phonology backup to be returned.
        :returns: a phonology backup model object.

        """
        phonology_backup = Session.query(PhonologyBackup).get(id)
        if phonology_backup:
            return phonology_backup
        else:
            response.status_int = 404
            return {'error': 'There is no phonology backup with id %s' % id}

    @h.jsonify
    def edit(self, id, format='html'):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}