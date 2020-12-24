# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_extras/flask_extras/__init__.py
# Compiled at: 2016-12-12 18:45:57
"""Hook to setup app easily."""
import os
from flask_extras import macros
from flask_extras.filters import config as filter_conf
import jinja2

def FlaskExtras(app):
    """Setup app config."""
    extra_folders = jinja2.ChoiceLoader([
     app.jinja_loader,
     jinja2.FileSystemLoader(os.path.dirname(macros.__file__))])
    app.jinja_loader = extra_folders
    filter_conf.config_flask_filters(app)