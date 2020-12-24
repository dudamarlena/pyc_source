# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/views.py
# Compiled at: 2018-02-20 08:15:54
# Size of source mod 2**32: 11253 bytes
import datetime
from flask.views import MethodView
from flask import request, jsonify, g
from werkzeug.exceptions import BadRequest
from odcs.server import app, db, log, conf
from odcs.server.errors import NotFound
from odcs.server.models import Compose
from odcs.common.types import COMPOSE_RESULTS, COMPOSE_FLAGS, COMPOSE_STATES, PUNGI_SOURCE_TYPE_NAMES, INVERSE_PUNGI_SOURCE_TYPE_NAMES, PungiSourceType
from odcs.server.api_utils import pagination_metadata, filter_composes, validate_json_data
from odcs.server.auth import requires_role, login_required
from odcs.server.auth import require_scopes
from odcs.server.auth import raise_if_source_type_not_allowed
api_v1 = {'composes':{'url':'/api/1/composes/', 
  'options':{'defaults':{'id': None}, 
   'methods':[
    'GET']}}, 
 'compose':{'url':'/api/1/composes/<int:id>', 
  'options':{'methods': ['GET']}}, 
 'composes_post':{'url':'/api/1/composes/', 
  'options':{'methods': ['POST']}}, 
 'compose_regenerate':{'url':'/api/1/composes/<int:id>', 
  'options':{'methods': ['PATCH']}}, 
 'composes_delete':{'url':'/api/1/composes/<int:id>', 
  'options':{'methods': ['DELETE']}}}

class ODCSAPI(MethodView):

    def _get_compose_owner(self):
        if conf.auth_backend == 'noauth':
            log.warn("Cannot determine the owner of compose, because 'noauth' auth_backend is used.")
            return 'unknown'
        else:
            return g.user.username

    def _get_seconds_to_live(self, request_data):
        if 'seconds-to-live' in request_data:
            try:
                return min(int(request_data['seconds-to-live']), conf.max_seconds_to_live)
            except ValueError:
                err = 'Invalid seconds-to-live specified in request: %s' % request_data
                log.error(err)
                raise ValueError(err)

        else:
            return conf.seconds_to_live

    def get(self, id):
        if id is None:
            p_query = filter_composes(request)
            json_data = {'meta':pagination_metadata(p_query, request.args), 
             'items':[item.json() for item in p_query.items]}
            return (
             jsonify(json_data), 200)
        compose = Compose.query.filter_by(id=id).first()
        if compose:
            return (
             jsonify(compose.json()), 200)
        raise NotFound('No such compose found.')

    @login_required
    @require_scopes('renew-compose')
    @requires_role('allowed_clients')
    def patch(self, id):
        if request.data:
            data = request.get_json(force=True)
        else:
            data = {}
        validate_json_data(data)
        seconds_to_live = self._get_seconds_to_live(data)
        old_compose = Compose.query.filter(Compose.id == id, Compose.state.in_([
         COMPOSE_STATES['removed'],
         COMPOSE_STATES['done'],
         COMPOSE_STATES['failed']])).first()
        if not old_compose:
            err = 'No compose with id %s found' % id
            log.error(err)
            raise NotFound(err)
        source_type = INVERSE_PUNGI_SOURCE_TYPE_NAMES[old_compose.source_type]
        raise_if_source_type_not_allowed(source_type)
        has_to_create_a_copy = old_compose.state in (
         COMPOSE_STATES['removed'], COMPOSE_STATES['failed'])
        if has_to_create_a_copy:
            log.info('%r: Going to regenerate the compose', old_compose)
            compose = Compose.create_copy(db.session, old_compose, self._get_compose_owner(), seconds_to_live)
            db.session.add(compose)
            db.session.commit()
            return (
             jsonify(compose.json()), 200)
        else:
            extend_from = datetime.datetime.utcnow()
            old_compose.extend_expiration(extend_from, seconds_to_live)
            log.info('Extended time_to_expire for compose %r to %s', old_compose, old_compose.time_to_expire)
            reused_compose = old_compose.get_reused_compose()
            if reused_compose:
                reused_compose.extend_expiration(extend_from, seconds_to_live)
            for c in old_compose.get_reusing_composes():
                c.extend_expiration(extend_from, seconds_to_live)

            db.session.commit()
            return (jsonify(old_compose.json()), 200)

    @login_required
    @require_scopes('new-compose')
    @requires_role('allowed_clients')
    def post(self):
        data = request.get_json(force=True)
        if not data:
            raise ValueError('No JSON POST data submitted')
        validate_json_data(data)
        seconds_to_live = self._get_seconds_to_live(data)
        source_data = data.get('source', None)
        if not isinstance(source_data, dict):
            err = 'Invalid source configuration provided: %s' % str(data)
            log.error(err)
            raise ValueError(err)
        needed_keys = ['type', 'source']
        for key in needed_keys:
            if key not in source_data:
                err = 'Missing %s in source configuration, received: %s' % (key, str(source_data))
                log.error(err)
                raise ValueError(err)

        source_type = source_data['type']
        if source_type not in PUNGI_SOURCE_TYPE_NAMES:
            err = 'Unknown source type "%s"' % source_type
            log.error(err)
            raise ValueError(err)
        else:
            raise_if_source_type_not_allowed(source_type)
            source_type = PUNGI_SOURCE_TYPE_NAMES[source_type]
            source = source_data['source'].split(' ')
            if not source:
                err = 'No source provided for %s' % source_type
                log.error(err)
                raise ValueError(err)
            if source_type == PungiSourceType.RAW_CONFIG:
                if len(source) > 1:
                    raise ValueError('Only single source is allowed for "raw_config" source_type')
                else:
                    source_name_hash = source[0].split('#')
                    if len(source_name_hash) != 2 or not source_name_hash[0] or not source_name_hash[1]:
                        raise ValueError('Source must be in "source_name#commit_hash" format for "raw_config" source_type.')
                    source_name, source_hash = source_name_hash
                    if source_name not in conf.raw_config_urls:
                        raise ValueError('Source "%s" does not exist in server configuration.' % source_name)
            source = ' '.join(source)
            packages = None
            if 'packages' in source_data:
                packages = ' '.join(source_data['packages'])
            sigkeys = ''
            if 'sigkeys' in source_data:
                sigkeys = ' '.join(source_data['sigkeys'])
            else:
                sigkeys = ' '.join(conf.sigkeys)
        flags = 0
        if 'flags' in data:
            for name in data['flags']:
                if name not in COMPOSE_FLAGS:
                    raise ValueError('Unknown flag %s', name)
                flags |= COMPOSE_FLAGS[name]

        results = COMPOSE_RESULTS['repository']
        if 'results' in data:
            for name in data['results']:
                if name not in COMPOSE_RESULTS:
                    raise ValueError('Unknown result %s', name)
                results |= COMPOSE_RESULTS[name]

        arches = None
        if 'arches' in data:
            arches = ' '.join(data['arches'])
        compose = Compose.create(db.session, self._get_compose_owner(), source_type, source, results, seconds_to_live, packages, flags, sigkeys, arches)
        db.session.add(compose)
        db.session.commit()
        return (
         jsonify(compose.json()), 200)

    @login_required
    @require_scopes('delete-compose')
    @requires_role('admins')
    def delete(self, id):
        compose = Compose.query.filter_by(id=id).first()
        if compose:
            deletable_states = {n:COMPOSE_STATES[n] for n in ('done', 'failed')}
            if compose.state not in deletable_states.values():
                raise BadRequest('Compose (id=%s) can not be removed, its state need to be in %s.' % (
                 id, deletable_states.keys()))
            compose.time_to_expire = datetime.datetime.utcnow()
            db.session.add(compose)
            db.session.commit()
            message = 'The delete request for compose (id=%s) has been accepted and will be processed by backend later.' % compose.id
            response = jsonify({'status':202,  'message':message})
            response.status_code = 202
            return response
        raise NotFound('No such compose found.')


def register_api_v1():
    """ Registers version 1 of ODCS API. """
    module_view = ODCSAPI.as_view('composes')
    for key, val in api_v1.items():
        (app.add_url_rule)(val['url'], endpoint=key, 
         view_func=module_view, **val['options'])


register_api_v1()