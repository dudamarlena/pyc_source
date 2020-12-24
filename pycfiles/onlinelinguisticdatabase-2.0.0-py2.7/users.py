# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/users.py
# Compiled at: 2016-09-19 13:27:02
"""Contains the :class:`UsersController` and its auxiliary functions.

.. module:: users
   :synopsis: Contains the users controller and its auxiliary functions.

"""
import logging, datetime, simplejson as json
from pylons import request, response, session, config
from formencode.validators import Invalid
from onlinelinguisticdatabase.lib.base import BaseController
from onlinelinguisticdatabase.lib.schemata import UserSchema
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
from onlinelinguisticdatabase.model.meta import Session
from onlinelinguisticdatabase.model import User
log = logging.getLogger(__name__)

class UsersController(BaseController):
    """Generate responses to requests on user resources.

    REST Controller styled on the Atom Publishing Protocol.

    .. note::
    
       The ``h.jsonify`` decorator converts the return value of the methods to
       JSON.

    """
    query_builder = SQLAQueryBuilder('User', config=config)

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def index(self):
        """Get all user resources.

        :URL: ``GET /users`` with optional query string parameters for
            ordering and pagination.
        :returns: a list of all user resources.

        .. note::

           See :func:`utils.add_order_by` and :func:`utils.add_pagination` for the
           query string parameters that effect ordering and pagination.

        """
        try:
            query = Session.query(User)
            query = h.add_order_by(query, dict(request.GET), self.query_builder)
            return h.add_pagination(query, dict(request.GET))
        except Invalid as e:
            response.status_int = 400
            return {'errors': e.unpack_errors()}

    @h.jsonify
    @h.restrict('POST')
    @h.authenticate
    @h.authorize(['administrator'])
    def create(self):
        """Create a new user resource and return it.

        :URL: ``POST /users``
        :request body: JSON object representing the user to create.
        :returns: the newly created user.

        .. note::
        
            Only administrators are authorized to create users.

        """
        try:
            schema = UserSchema()
            values = json.loads(unicode(request.body, request.charset))
            data = schema.to_python(values)
            user = create_new_user(data)
            Session.add(user)
            Session.commit()
            return user.get_full_dict()
        except h.JSONDecodeError:
            response.status_int = 400
            return h.JSONDecodeErrorResponse
        except Invalid as e:
            response.status_int = 400
            return {'errors': e.unpack_errors()}

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    @h.authorize(['administrator'])
    def new(self):
        """Return the data necessary to create a new user.

        :URL: ``GET /users/new`` with optional query string parameters .
        :returns: a dictionary of lists of resources.

        .. note::
        
           See :func:`get_new_user_data` to understand how the query string
           parameters can affect the contents of the lists in the returned
           dictionary.

        """
        return get_new_user_data(request.GET)

    @h.jsonify
    @h.restrict('PUT')
    @h.authenticate
    @h.authorize(['administrator', 'contributor', 'viewer'], None, True)
    def update(self, id):
        """Update a user and return it.
        
        :URL: ``PUT /users/id``
        :Request body: JSON object representing the user with updated attribute values.
        :param str id: the ``id`` value of the user to be updated.
        :returns: the updated user model.

        """
        user = Session.query(User).get(int(id))
        if user:
            try:
                schema = UserSchema()
                values = json.loads(unicode(request.body, request.charset))
                state = h.get_state_object(values)
                state.user_to_update = user.get_full_dict()
                current_user = Session.query(User).get(session['user'].id)
                state.user = current_user.get_full_dict()
                data = schema.to_python(values, state)
                user = update_user(user, data)
                if user:
                    Session.add(user)
                    Session.commit()
                    return user.get_full_dict()
                response.status_int = 400
                return {'error': 'The update request failed because the submitted data were not new.'}
            except h.JSONDecodeError:
                response.status_int = 400
                return h.JSONDecodeErrorResponse
            except Invalid as e:
                response.status_int = 400
                return {'errors': e.unpack_errors()}

        else:
            response.status_int = 404
            return {'error': 'There is no user with id %s' % id}

    @h.jsonify
    @h.restrict('DELETE')
    @h.authenticate
    @h.authorize(['administrator'])
    def delete(self, id):
        """Delete an existing user and return it.

        :URL: ``DELETE /users/id``
        :param str id: the ``id`` value of the user to be deleted.
        :returns: the deleted user model.

        """
        user = Session.query(User).get(id)
        if user:
            h.destroy_user_directory(user)
            Session.delete(user)
            Session.commit()
            return user.get_full_dict()
        else:
            response.status_int = 404
            return {'error': 'There is no user with id %s' % id}

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    def show(self, id):
        """Return a user.
        
        :URL: ``GET /users/id``
        :param str id: the ``id`` value of the user to be returned.
        :returns: a user model object.

        """
        user = Session.query(User).get(id)
        if user:
            return user
        else:
            response.status_int = 404
            return {'error': 'There is no user with id %s' % id}

    @h.jsonify
    @h.restrict('GET')
    @h.authenticate
    @h.authorize(['administrator', 'contributor', 'viewer'], user_id_is_args1=True)
    def edit(self, id):
        """Return a user resource and the data needed to update it.

        :URL: ``GET /users/edit``
        :param str id: the ``id`` value of the user that will be updated.
        :returns: a dictionary of the form::

                {"user": {...}, "data": {...}}

            where the value of the ``user`` key is a dictionary representation
            of the user and the value of the ``user`` key is a dictionary of
            lists of resources.

        .. note::

           See :func:`get_new_user_data` to understand how the query string
           parameters can affect the contents of the lists in the returned
           dictionary.

        """
        user = Session.query(User).get(id)
        if user:
            data = get_new_user_data(request.GET)
            return {'data': data, 'user': user.get_full_dict()}
        else:
            response.status_int = 404
            return {'error': 'There is no user with id %s' % id}


def get_new_user_data(GET_params):
    """Return the data necessary to create a new OLD user or update an existing one.
    
    :param GET_params: the ``request.GET`` dictionary-like object generated by
        Pylons which contains the query string parameters of the request.
    :returns: A dictionary whose values are lists of objects needed to create or
        update user.

    If ``GET_params`` has no keys, then return all data.  If ``GET_params`` does
    have keys, then for each key whose value is a non-empty string (and not a
    valid ISO 8601 datetime) add the appropriate list of objects to the return
    dictionary.  If the value of a key is a valid ISO 8601 datetime string, add
    the corresponding list of objects *only* if the datetime does *not* match
    the most recent ``datetime_modified`` value of the resource.  That is, a
    non-matching datetime indicates that the requester has out-of-date data.

    """
    model_name_map = {'orthographies': 'Orthography'}
    getter_map = {'orthographies': h.get_mini_dicts_getter('Orthography')}
    result = dict([ (key, []) for key in getter_map ])
    result['roles'] = h.user_roles
    result['markup_languages'] = h.markup_languages
    if GET_params:
        for key in getter_map:
            val = GET_params.get(key)
            if val:
                val_as_datetime_obj = h.datetime_string2datetime(val)
                if val_as_datetime_obj:
                    if val_as_datetime_obj != h.get_most_recent_modification_datetime(model_name_map[key]):
                        result[key] = getter_map[key]()
                else:
                    result[key] = getter_map[key]()

    else:
        for key in getter_map:
            result[key] = getter_map[key]()

    return result


def create_new_user(data):
    """Create a new user.

    :param dict data: the data for the user to be created.
    :returns: an SQLAlchemy model object representing the user.

    """
    user = User()
    user.salt = h.generate_salt()
    user.password = unicode(h.encrypt_password(data['password'], str(user.salt)))
    user.username = h.normalize(data['username'])
    user.first_name = h.normalize(data['first_name'])
    user.last_name = h.normalize(data['last_name'])
    user.email = h.normalize(data['email'])
    user.affiliation = h.normalize(data['affiliation'])
    user.role = h.normalize(data['role'])
    user.markup_language = h.normalize(data['markup_language'])
    user.page_content = h.normalize(data['page_content'])
    user.html = h.get_HTML_from_contents(user.page_content, user.markup_language)
    if data['input_orthography']:
        user.input_orthography = data['input_orthography']
    if data['output_orthography']:
        user.output_orthography = data['output_orthography']
    user.datetime_modified = datetime.datetime.utcnow()
    h.create_user_directory(user)
    return user


def update_user(user, data):
    """Update a user.

    :param user: the user model to be updated.
    :param dict data: representation of the updated user.
    :returns: the updated user model or, if ``changed`` has not been set
        to ``True``, ``False``.

    """
    changed = False
    changed = user.set_attr('first_name', h.normalize(data['first_name']), changed)
    changed = user.set_attr('last_name', h.normalize(data['last_name']), changed)
    changed = user.set_attr('email', h.normalize(data['email']), changed)
    changed = user.set_attr('affiliation', h.normalize(data['affiliation']), changed)
    changed = user.set_attr('role', h.normalize(data['role']), changed)
    changed = user.set_attr('page_content', h.normalize(data['page_content']), changed)
    changed = user.set_attr('markup_language', h.normalize(data['markup_language']), changed)
    changed = user.set_attr('html', h.get_HTML_from_contents(user.page_content, user.markup_language), changed)
    if data['password'] is not None:
        changed = user.set_attr('password', unicode(h.encrypt_password(data['password'], str(user.salt))), changed)
    if data['username'] is not None:
        username = h.normalize(data['username'])
        if username != user.username:
            h.rename_user_directory(user.username, username)
        changed = user.set_attr('username', username, changed)
    changed = user.set_attr('input_orthography', data['input_orthography'], changed)
    changed = user.set_attr('output_orthography', data['output_orthography'], changed)
    if changed:
        user.datetime_modified = datetime.datetime.utcnow()
        return user
    else:
        return changed