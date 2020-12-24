# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scottblevins/git/impression/impression/extensions.py
# Compiled at: 2016-07-22 10:55:12
from flask_cache import Cache
try:
    from flask_debugtoolbar import DebugToolbarExtension
    debug_toolbar = DebugToolbarExtension()
except ImportError:
    debug_toolbar = None

from flask_login import LoginManager
from flask_assets import Environment
from flask_themes2 import Themes
from impression.models import User
cache = Cache()
themes2 = Themes()
assets_env = Environment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main_controller.login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)