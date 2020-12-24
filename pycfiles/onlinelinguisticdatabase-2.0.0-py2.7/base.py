# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/lib/base.py
# Compiled at: 2016-09-19 13:27:02
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from onlinelinguisticdatabase.model.meta import Session
from onlinelinguisticdatabase.model import User
from pylons import request, response, session, app_globals
import onlinelinguisticdatabase.lib.helpers as h, logging
log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __before__(self):
        """This method is called before each controller action is called.  It is
        being used here for Pylons functional testing.  Specifically, it is
        being used to control the session and app_globals from within tests.
        
        If present, environ['test.authentication.role'] will evaluate to a user
        role that can be used to retrieve a user with that role from the db and
        put it in the (Beaker) session.  This permits simulation of
        authentication and authorization. See https://groups.google.com/forum/?fromgroups=#!searchin/pylons-discuss/test$20session/pylons-discuss/wiwOQBIxDw8/0yR3z3YiYzYJ
        for the origin of this hack.

        If present, setting environ['test.application_settings'] to a truthy
        value will result in app_globals.application_settings being set to an
        ApplicationSettings instance.  This permits simulation of the
        application settings cache in app_globals which is used for
        inventory-based validation.  One issue with this approach is that the
        app_globals.application_settings attribute is not unset after the test is
        run.  Therefore, the __after__ method (see below) deletes the attribute
        when environ['test.application_settings'] is truthy.

        WARNING: overwriting __before__ (or __after__) in a controller class
        (without calling their super methods) will cause nosetests to fail en
        masse.
        """
        if 'test.authentication.role' in request.environ:
            role = unicode(request.environ['test.authentication.role'])
            user = Session.query(User).filter(User.role == role).first()
            if user:
                session['user'] = user
        if 'test.authentication.id' in request.environ:
            user = Session.query(User).get(request.environ['test.authentication.id'])
            if user:
                session['user'] = user
        if request.environ.get('test.application_settings'):
            app_globals.application_settings = h.ApplicationSettings()

    def __after__(self):
        if request.environ.get('test.application_settings') and not request.environ.get('test.retain_application_settings'):
            del app_globals.application_settings