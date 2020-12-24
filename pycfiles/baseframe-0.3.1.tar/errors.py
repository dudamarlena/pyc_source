# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jace/Dropbox/projects/hasgeek/baseframe/baseframe/errors.py
# Compiled at: 2015-11-25 03:30:49
from . import baseframe, current_app, baseframe_translations
from flask import request, redirect
from coaster.views import render_with
from coaster.db import db
from werkzeug.routing import NotFound, MethodNotAllowed, RequestRedirect

@baseframe.app_errorhandler(404)
@render_with('404.html', json=True)
def error404(e):
    if request.path.endswith('/') and request.method == 'GET':
        newpath = request.path[:-1]
        try:
            adapter = current_app.url_map.bind_to_environ(request)
            matchinfo = adapter.match(newpath)
            if matchinfo[0] != request.endpoint:
                redirect_url = request.base_url[:-1]
                if request.query_string:
                    redirect_url = redirect_url + '?' + request.query_string
                return redirect(redirect_url)
        except (NotFound, RequestRedirect, MethodNotAllowed):
            pass

    baseframe_translations.as_default()
    return ({'error': '404 Not Found'}, 404)


@baseframe.app_errorhandler(403)
@render_with('403.html', json=True)
def error403(e):
    baseframe_translations.as_default()
    return ({'error': '403 Forbidden'}, 403)


@baseframe.app_errorhandler(500)
@render_with('500.html', json=True)
def error500(e):
    db.session.rollback()
    baseframe_translations.as_default()
    return ({'error': '500 Internal Server Error'}, 500)