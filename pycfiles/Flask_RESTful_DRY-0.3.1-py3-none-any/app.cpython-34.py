# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/api/app.py
# Compiled at: 2015-04-14 08:12:05
# Size of source mod 2**32: 4661 bytes
"""This is where the DRY_Flask app class is declared.
"""
import sys
from collections import defaultdict
from sqlalchemy.event import listen
from sqlalchemy.orm import mapper, configure_mappers
from flask import Flask, request_finished, session, current_app
from flask.sessions import SecureCookieSessionInterface
from flask.wrappers import Response
from ..model.utils import db, names_from_module

class DRY_Response(Response):
    default_mimetype = None


class DRY_Flask(Flask):
    response_class = DRY_Response

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dry_keyed_links = defaultdict(list)
        self.dry_relation_category_links = defaultdict(list)
        if self.testing:
            print('WARNING: Using Insecure session cookies for testing', file=sys.stderr)

            def serialize(data):
                """Serialize session data.

                Format is space separated key:value pairs.
                """
                assert isinstance(data, dict)
                return ' '.join('{}:{}'.format(k, s(v)) for k, v in sorted(data.items()))

            def deserialize(data):
                """Deserialize serialized session data.
                """

                def de_kv(kv):
                    k, v = kv.split(':')
                    return (k, d(v))

                return dict(de_kv(kv) for kv in data.split(' '))

            def s(v):
                """Serialize a value.
                """
                return repr(v)

            def d(v):
                """Deserialize a serialized value.

                Wasn't brave (foolish?) enough to use "eval" here...
                """
                if v[0] == "'":
                    return v[1:-1]
                try:
                    return float(v)
                except ValueError:
                    try:
                        return int(v)
                    except ValueError:
                        return bool(v)

            class InsecureSessionInterface(SecureCookieSessionInterface):
                override_header = 'X-Session'

                def open_session(self, app, request):
                    if self.override_header not in request.headers:
                        print('open_session deferring to super')
                        return super().open_session(app, request)
                    val = request.headers.get(self.override_header)
                    print('open_session got', repr(val))
                    if not val:
                        return self.session_class()
                    try:
                        data = deserialize(val)
                    except ValueError:
                        return self.session_class()

                    print('open_session deserialized', data)
                    return self.session_class(data)

            self.session_interface = InsecureSessionInterface()

            def dump_session(app, response):
                print('final session:')
                for k, v in sorted(session.items()):
                    print('    {}: {!r}'.format(k, v))

            request_finished.connect(dump_session)

    def load_models_from_module(self, all_models):
        """Takes a module that has imported all of models.
        
        Returns {model.__name__: model}
        """
        return self.load_models(*names_from_module(all_models))

    def load_models(self, *models):
        """Loads models into the app.
        """
        db.init_app(self)
        self.dry_unique_constraints = {}
        self.dry_foreign_key_constraints = {}
        self.dry_models_by_tablename = {}
        models_map = {}
        for model in models:
            self.dry_models_by_tablename[model.__tablename__] = model
            models_map[model.__name__] = model

        listen(mapper, 'after_configured', self._register)
        with self.app_context():
            configure_mappers()
        return models_map

    def _register(self):
        for model in self.dry_models_by_tablename.values():
            model._dry_register()