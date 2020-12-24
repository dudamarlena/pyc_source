# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/morphologicalparserbackups.py
# Compiled at: 2016-09-19 13:27:02
"""Contains the :class:`MorphologicalparserbackupsController`.

.. module:: morphologicalparserbackups
   :synopsis: Contains the morphological parser backups controller.

"""
import logging
from pylons import request, response, config
from formencode.validators import Invalid
from onlinelinguisticdatabase.lib.base import BaseController
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
from onlinelinguisticdatabase.model.meta import Session
from onlinelinguisticdatabase.model import MorphologicalParserBackup
log = logging.getLogger(__name__)

class MorphologicalparserbackupsController(BaseController):
    """Generate responses to requests on morphological parser backup resources.

    REST Controller styled on the Atom Publishing Protocol.

    .. note::

       The ``h.jsonify`` decorator converts the return value of the methods to
       JSON.

    .. note::

        Morphological parser backups are created when updating and deleting morphological
        parsers; they cannot be created directly and they should never be deleted.  This
        controller facilitates retrieval of morphological parser backups only.

    """
    query_builder = SQLAQueryBuilder('MorphologicalParserBackup', config=config)

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def index(self):
        """Get all morphological parser backup resources.

        :URL: ``GET /morphologicalparserbackups`` 
        :returns: a list of all morphological parser backup resources.

        """
        try:
            query = Session.query(MorphologicalParserBackup)
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
        """Return a morphological parser backup.

        :URL: ``GET /morphologicalparserbackups/id``
        :param str id: the ``id`` value of the morphological parser backup to be returned.
        :returns: a morphological parser backup model object.

        """
        morphological_parser_backup = Session.query(MorphologicalParserBackup).get(id)
        if morphological_parser_backup:
            return morphological_parser_backup
        else:
            response.status_int = 404
            return {'error': 'There is no morphological parser backup with id %s' % id}

    @h.jsonify
    def edit(self, id, format='html'):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}