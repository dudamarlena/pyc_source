# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/plugins/runmethods.py
# Compiled at: 2007-01-10 11:06:24
import sys, simpleweb.app, simpleweb.utils

def cgi(urls, config):
    from wsgiref.handlers import CGIHandler
    wsgiapp = simpleweb.app.SimplewebApp(urls, config)
    CGIHandler().run(wsgiapp)


def fcgi(urls, config):
    try:
        from flup.server.fcgi import WSGIServer
    except ImportError:
        simpleweb.utils.optional_dependency_err('FCGI WSGI server for "%s"' % config.working_directory, 'flup')
    else:
        wsgiapp = simpleweb.app.SimplewebApp(urls, config)
        WSGIServer(wsgiapp, debug=config.enable_debug).run()


def development(urls, config):
    from simpleweb.extlib import memento
    import simpleweb.webserver
    if config.server_reload:
        wsgiapp = memento.Assassin('simpleweb.app:SimplewebReloadingApp()', ['controllers', 'urls', 'simpleweb', 'config'])
    else:
        wsgiapp = simpleweb.app.SimplewebApp(urls, config)
    warnmsg = None
    if config.enable_sessions:
        try:
            import flup.middleware.session
        except ImportError:
            warnmsg = "'flup' not installed. Sessions will be unavailable"

    simpleweb.webserver.wsgiserve(wsgiapp, config.server_host, config.server_port, config.server_reload, config.server_user, config.server_group, warnmsg=warnmsg)
    return