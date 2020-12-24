# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/tests/testish/testish/wsgiapp.py
# Compiled at: 2010-02-18 16:34:58
from restish.app import RestishApp
from restish.templating import Templating
from testish.resource import root
import os, pkg_resources
from restish.contrib.makorenderer import MakoRenderer
import mimetypes
try:
    mimetypes.init()
except AttributeError:
    pass

def make_app(global_conf, **app_conf):
    """
    PasteDeploy WSGI application factory.

    Called by PasteDeply (or a compatable WSGI application host) to create the
    testish WSGI application.
    """
    app = RestishApp(root.Root())
    app = setup_environ(app, global_conf, app_conf)
    return app


def setup_environ(app, global_conf, app_conf):
    """
    WSGI application wrapper factory for extending the WSGI environ with
    application-specific keys.
    """
    renderer = MakoRenderer(directories=[
     pkg_resources.resource_filename('testish', 'templates')], module_directory=os.path.join(app_conf['cache_dir'], 'templates'), input_encoding='utf-8', output_encoding='utf-8', default_filters=[
     'unicode', 'h'])

    def application(environ, start_response):
        environ['restish.templating'] = Templating(renderer)
        return app(environ, start_response)

    return application