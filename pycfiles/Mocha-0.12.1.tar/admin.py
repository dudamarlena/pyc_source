# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/mocha/mocha/contrib/views/admin.py
# Compiled at: 2017-06-04 16:07:38
"""
views.admin is a basic home page for your admin area
"""
from mocha import Mocha, utils, render, decorators as deco
import mocha.contrib
__options__ = utils.dict_dot({})

@mocha.contrib.admin
class Admin(Mocha):

    @classmethod
    def _register(cls, app, **kwargs):
        kwargs['base_route'] = __options__.get('route', '/admin/')
        super(cls, cls)._register(app, **kwargs)

    @render.template('contrib/admin/Admin/index.jade')
    @render.nav('Admin Home', tags=mocha.contrib.ADMIN_TAG, attach_to=['mocha.contrib.views.auth.Account', 'self'])
    def index(self):
        pass