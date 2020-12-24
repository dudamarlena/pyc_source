# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/controllers/commit.py
# Compiled at: 2008-08-07 05:56:02
import logging
from divimon.lib.base import *
from divimon import model
from pylons.decorators import jsonify
log = logging.getLogger(__name__)

def get_id(entry):
    return getattr(entry, 'id')


class CommitController(BaseController):

    def __after__(self):
        env = dict(request.environ.items())
        wsgi = env['wsgiorg.routing_args'][1]
        if wsgi['action'] in ('login', 'logout', 'index', 'list') or wsgi['controller'] in ('index', ):
            return
        history = model.History(user=None, controller=unicode(wsgi['controller']), action=unicode(wsgi['action']), arguments=unicode(env['QUERY_STRING']))
        model.Session.save(history)
        model.Session.commit()
        return

    def __before__(self, action, **kw):
        env = {}
        for (k, v) in request.environ.items():
            env[k] = v

        env['SCRIPT_NAME'] = ''
        import routes
        config = routes.request_config()
        config.environ = env

    def test(self):
        data = dict(one=1, two=2, three=3)
        entries = map(get_id, model.list(model.Agent))
        data['entries'] = entries
        data['request'] = request.params
        response.content_type = 'text/plain'
        return data

    def open_remote(self):
        from urllib import FancyURLopener
        opener = FancyURLopener()
        server = '10.0.2.2:5001'
        content = opener.open('http://%s/commit/test' % server, data='user=admin&password=admin')
        print dir(content)
        print content.headers
        return ('\n').join(content.readlines())

    def _get_last_commit(self):
        query = model.list(model.History)
        query = query.filter_by(controller='commit').order_by(model.History.c.created.desc())
        return query[0]

    def items(self):
        last_commit = self._get_last_commit().created
        response.content_type = 'text/plain'
        response.cache = 'no'
        return last_commit