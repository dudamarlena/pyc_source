# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eggbasket/controllers/admin.py
# Compiled at: 2008-07-13 16:55:56
import logging, os, cherrypy as cp, turbogears as tg
try:
    from dbsprockets.dbmechanic.frameworks.tg import DBMechanic
    from dbsprockets.saprovider import SAProvider
    has_dbsprockets = True
except ImportError:
    has_dbsprockets = False

from eggbasket import model
log = logging.getLogger('eggbasket.controllers')

class AdminController(tg.controllers.Controller, tg.identity.SecureResource):
    """Controller for administration and configuration pages."""
    require = tg.identity.in_group('admin')

    @tg.expose(template='eggbasket.templates.admin')
    def index(self, *args, **kw):
        """Show administration start page."""
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        return dict(pkg_root=pkg_root, has_dbsprockets=has_dbsprockets)

    if has_dbsprockets:
        database = DBMechanic(SAProvider(model.metadata), '/admin/database')