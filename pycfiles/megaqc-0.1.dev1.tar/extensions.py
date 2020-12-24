# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewels/GitHub/MegaQC/megaqc/extensions.py
# Compiled at: 2017-10-19 03:04:36
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
cache = Cache()
debug_toolbar = DebugToolbarExtension()