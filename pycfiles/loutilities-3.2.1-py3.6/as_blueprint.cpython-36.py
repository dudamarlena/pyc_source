# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\flask_helpers\as_blueprint.py
# Compiled at: 2019-11-20 12:25:25
# Size of source mod 2**32: 1631 bytes
from flask import Flask, Blueprint
from flask.views import MethodView

class ApiResource(MethodView):
    endpoint = None
    url_prefix = None
    url_rules = {}

    @classmethod
    def as_blueprint(cls, name=None):
        name = name or cls.endpoint
        bp = Blueprint(name, (cls.__module__), url_prefix=(cls.url_prefix))
        for endpoint, options in list(cls.url_rules.items()):
            url_rule = options
            methods = ('GET', )
            defaults = {}
            if len(options) == 2:
                url_rule, methods = options
            else:
                if len(options) == 3:
                    url_rule, methods, defaults = options
            bp.add_url_rule(url_rule, endpoint=endpoint, methods=methods, defaults=defaults,
              view_func=(cls.as_view(endpoint)))

        return bp


class MyResource(ApiResource):
    endpoint = 'my'
    url_prefix = '/hello'
    url_rules = {'index':[
      '', ('GET', ), {'id': None}], 
     'select':[
      '/<id>', ('GET', )]}

    def get(self, id):
        if id is None:
            return 'hello'
        else:
            return id


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(MyResource.as_blueprint())
    assert app.url_map.is_endpoint_expecting('my.index')
    assert app.url_map.is_endpoint_expecting('my.select', 'id')
    with app.test_client() as (client):
        if not client.get('/hello').data == 'hello':
            raise AssertionError
        elif not client.get('/hello/stuff').data == 'stuff':
            raise AssertionError
    print('Tests passed successfully!')