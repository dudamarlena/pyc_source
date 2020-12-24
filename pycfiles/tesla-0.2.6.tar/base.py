# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/lib/base.py
# Compiled at: 2007-09-06 07:54:15
from pylons import Response, c, g, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, validate
from pylons.templating import render
from pylons.helpers import abort, redirect_to, etag_cache
from pylons.i18n import N_, _, ungettext
from projectname.lib.helpers import get_object_or_404
import projectname.model as model, projectname.lib.helpers as h

class BaseController(WSGIController):
    __model__ = None

    def __call__(self, environ, start_response):
        model.resync()
        return WSGIController.__call__(self, environ, start_response)

    def __before__(self):
        self._check_action()
        self._load_model()
        self._context()

    def _load_model(self):
        """
        If __model__ variable is set will automatically load model instance into context
        if "id" is in Routes. The name used in the context is the same name as the model
        (in lowercase); otherwise you can use the __name__ attribute. 
        """
        if self.__model__:
            routes_id = request.environ['pylons.routes_dict']['id']
            if routes_id:
                instance = get_object_or_404(self.__model__, id=routes_id)
                name = getattr(self, '__name__', self.__model__.__name__.lower())
                setattr(c, name, instance)

    def _context(self):
        """
        Put your common context variables in here
        """
        pass

    def _check_action(self):
        action = request.environ['pylons.routes_dict']['action']
        if not hasattr(self, action):
            abort(404)


__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') or __name == '_'
          ]