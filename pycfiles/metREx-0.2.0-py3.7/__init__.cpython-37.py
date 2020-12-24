# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/app/__init__.py
# Compiled at: 2020-04-16 16:30:09
# Size of source mod 2**32: 1894 bytes
from cfenv import AppEnv
from flask import Blueprint, url_for
from flask_restx import Api
import re
from __init__ import __description__, __title__, __version__
import main.controller.metrics_controller as metrics_ns
import main.controller.scheduler_controller as scheduler_ns
blueprint = Blueprint('api', __name__)
blueprint.config = {}

@blueprint.record
def record_config(setup_state):
    app = setup_state.app
    blueprint.config = dict([(key, value) for key, value in app.config.items()])


class MyApi(Api):
    __doc__ = '\n    Extension of the main entry point for the application.\n    Need to modify Swagger API behavior to support running in HTTPS when deployed to PCF\n    '

    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        """
        return url_for((self.endpoint('specs')), _external=False)


env = AppEnv()
kwargs_api = {'title':__title__, 
 'version':__version__, 
 'description':__description__}
if env.name is not None:
    pattern = re.compile('\n            (?P<title>.*)(?=-v[\\d\\.\\+]+$)\n            (?:\n                -v(?P<version>[\\d\\.\\+]+)$\n            )\n        ', re.X)
    m = pattern.match(env.name)
    if m is not None:
        components = m.groupdict()
        kwargs_api.update(components)
    else:
        kwargs_api['title'] = env.name
api = MyApi(blueprint, **kwargs_api)
api.add_namespace(metrics_ns, path='/metrics')
api.add_namespace(scheduler_ns, path='/scheduler')

@api.errorhandler
def default_error_handler(error):
    """
    Default error handler
    """
    message = str(error)
    if 'ERROR_INCLUDE_MESSAGE' in api.app.config.keys():
        if not api.app.config['ERROR_INCLUDE_MESSAGE']:
            message = 'Internal Server Error'
    return (
     {'message': message}, 500)