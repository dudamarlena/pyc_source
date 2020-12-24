# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\temp\sandbox\app\views.py
# Compiled at: 2020-02-04 02:27:43
# Size of source mod 2**32: 878 bytes
"""
ATS common view  module.

Created on 2019-3-3.
author: chenwen9.
"""
from . import appbuilder
import logging
from fab_admin.views import ApiUserView
from flask.templating import render_template

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    """The global page not found flask action."""
    return (
     render_template('404.html', base_template=(appbuilder.base_template), appbuilder=appbuilder), 404)


log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])
appbuilder.add_view_no_menu(ApiUserView)