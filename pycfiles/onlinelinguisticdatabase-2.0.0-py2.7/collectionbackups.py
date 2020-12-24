# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/collectionbackups.py
# Compiled at: 2016-09-19 13:27:02
"""Contains the :class:`CollectionbackupsController`.

.. module:: collectionbackups
   :synopsis: Contains the collection backups controller.

"""
import logging, simplejson as json
from pylons import request, response, session, config
from formencode.validators import Invalid
from sqlalchemy.exc import OperationalError, InvalidRequestError
from onlinelinguisticdatabase.lib.base import BaseController
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder, OLDSearchParseError
from onlinelinguisticdatabase.model.meta import Session
from onlinelinguisticdatabase.model import CollectionBackup
log = logging.getLogger(__name__)

class CollectionbackupsController(BaseController):
    """Generate responses to requests on collection backup resources.

    REST Controller styled on the Atom Publishing Protocol.
    
    .. note::
    
       The ``h.jsonify`` decorator converts the return value of the methods to
       JSON.

    .. note::
    
        Collection backups are created when updating and deleting collections;
        they cannot be created directly and they should never be deleted.  This
        controller facilitates searching and getting of collection backups only.

    """
    query_builder = SQLAQueryBuilder('CollectionBackup', config=config)

    @h.jsonify
    @h.restrict('SEARCH', 'POST')
    @h.authenticate
    def search(self):
        """Return the list of collection backup resources matching the input
        JSON query.

        :URL: ``SEARCH /collectionbackups`` (or ``POST /collectionbackups/search``)
        :request body: A JSON object of the form::

                {"query": {"filter": [ ... ], "order_by": [ ... ]},
                 "paginator": { ... }}

            where the ``order_by`` and ``paginator`` attributes are optional.

        """
        try:
            json_search_params = unicode(request.body, request.charset)
            python_search_params = json.loads(json_search_params)
            SQLAQuery = self.query_builder.get_SQLA_query(python_search_params.get('query'))
            query = h.filter_restricted_models('CollectionBackup', SQLAQuery)
            return h.add_pagination(query, python_search_params.get('paginator'))
        except h.JSONDecodeError:
            response.status_int = 400
            return h.JSONDecodeErrorResponse
        except (OLDSearchParseError, Invalid) as e:
            response.status_int = 400
            return {'errors': e.unpack_errors()}
        except (OperationalError, AttributeError, InvalidRequestError, RuntimeError):
            response.status_int = 400
            return {'error': 'The specified search parameters generated an invalid database query'}

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def new_search(self):
        """Return the data necessary to search the collection backup resources.

        :URL: ``GET /collectionbackups/new_search``
        :returns: ``{"search_parameters": {"attributes": { ... }, "relations": { ... }}``

        """
        return {'search_parameters': h.get_search_parameters(self.query_builder)}

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def index(self):
        """Get all collection backup resources.

        :URL: ``GET /collectionbackups`` 
        :returns: a list of all collection backup resources.

        """
        try:
            query = Session.query(CollectionBackup)
            query = h.add_order_by(query, dict(request.GET), self.query_builder)
            query = h.filter_restricted_models('CollectionBackup', query)
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
        """Return a collection backup.
        
        :URL: ``GET /collectionbackups/id``
        :param str id: the ``id`` value of the collection backup to be returned.
        :returns: a collection backup model object.

        """
        collection_backup = Session.query(CollectionBackup).get(id)
        if collection_backup:
            unrestricted_users = h.get_unrestricted_users()
            user = session['user']
            if h.user_is_authorized_to_access_model(user, collection_backup, unrestricted_users):
                return collection_backup
            response.status_int = 403
            return h.unauthorized_msg
        else:
            response.status_int = 404
            return {'error': 'There is no collection backup with id %s' % id}

    @h.jsonify
    def edit(self, id, format='html'):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}