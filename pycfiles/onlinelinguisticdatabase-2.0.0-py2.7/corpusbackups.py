# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/corpusbackups.py
# Compiled at: 2016-09-19 13:27:02
"""Contains the :class:`CorpusbackupsController`.

.. module:: corpusbackups
   :synopsis: Contains the corpus backups controller.

"""
import logging, simplejson as json
from pylons import request, response, session, config
from formencode.validators import Invalid
from sqlalchemy.exc import OperationalError, InvalidRequestError
from onlinelinguisticdatabase.lib.base import BaseController
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder, OLDSearchParseError
from onlinelinguisticdatabase.model.meta import Session
from onlinelinguisticdatabase.model import CorpusBackup
log = logging.getLogger(__name__)

class CorpusbackupsController(BaseController):
    """Generate responses to requests on corpus backup resources.

    REST Controller styled on the Atom Publishing Protocol.
    
    .. note::
    
       The ``h.jsonify`` decorator converts the return value of the methods to
       JSON.

    .. note::
    
        Corpus backups are created when updating and deleting corpora;
        they cannot be created directly and they should never be deleted.  This
        controller facilitates searching and getting of corpus backups only.

    """
    query_builder = SQLAQueryBuilder('CorpusBackup', config=config)

    @h.jsonify
    @h.restrict('SEARCH', 'POST')
    @h.authenticate
    def search(self):
        """Return the list of corpus backup resources matching the input
        JSON query.

        :URL: ``SEARCH /corpusbackups`` (or ``POST /corpusbackups/search``)
        :request body: A JSON object of the form::

                {"query": {"filter": [ ... ], "order_by": [ ... ]},
                 "paginator": { ... }}

            where the ``order_by`` and ``paginator`` attributes are optional.

        """
        try:
            json_search_params = unicode(request.body, request.charset)
            python_search_params = json.loads(json_search_params)
            query = self.query_builder.get_SQLA_query(python_search_params.get('query'))
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
        """Return the data necessary to search the corpus backup resources.

        :URL: ``GET /corpusbackups/new_search``
        :returns: ``{"search_parameters": {"attributes": { ... }, "relations": { ... }}``

        """
        return {'search_parameters': h.get_search_parameters(self.query_builder)}

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def index(self):
        """Get all corpus backup resources.

        :URL: ``GET /corpusbackups`` 
        :returns: a list of all corpus backup resources.

        """
        try:
            query = Session.query(CorpusBackup)
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
        """Return a corpus backup.
        
        :URL: ``GET /corpusbackups/id``
        :param str id: the ``id`` value of the corpus backup to be returned.
        :returns: a corpus backup model object.

        """
        corpus_backup = Session.query(CorpusBackup).get(id)
        if corpus_backup:
            unrestricted_users = h.get_unrestricted_users()
            user = session['user']
            if h.user_is_authorized_to_access_model(user, corpus_backup, unrestricted_users):
                return corpus_backup
            response.status_int = 403
            return h.unauthorized_msg
        else:
            response.status_int = 404
            return {'error': 'There is no corpus backup with id %s' % id}

    @h.jsonify
    def edit(self, id, format='html'):
        response.status_int = 404
        return {'error': 'This resource is read-only.'}