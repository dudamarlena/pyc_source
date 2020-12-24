# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/webassets.py
# Compiled at: 2016-12-06 12:24:25
from flask_assets import Environment
assets = Environment()

def init_webassets(self, asset_map=None):
    """
    Initialize web assets.

    :returns: None

    `webassets <https://github.com/miracle2k/webassets>`_ make it simpler
    to process and bundle CSS and Javascript assets.  This can be baked
    into a Flask application using
    `Flask-Assets <http://flask-assets.readthedocs.org/en/latest/>`_
    """
    assets.init_app(self.app)
    if asset_map:
        asset_map(assets)