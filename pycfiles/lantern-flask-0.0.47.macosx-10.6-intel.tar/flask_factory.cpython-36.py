# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/coding/Lantern/lantern-flask/.virtualenv/lib/python3.6/site-packages/lantern_flask/flask/flask_factory.py
# Compiled at: 2018-11-30 11:45:11
# Size of source mod 2**32: 136 bytes
from flask import Flask
from flask_dotenv import DotEnv
app = Flask(__name__)
env = DotEnv()
env.init_app(app)
settings = app.config