# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/bitnami/apps/jenkins/jenkins_home/jobs/Publish python-govuk-template/workspace/govuk_template/flask/assets/routes.py
# Compiled at: 2015-05-21 11:37:03
# Size of source mod 2**32: 313 bytes
from flask import send_from_directory
from os import path
__dot = path.dirname(path.realpath(__file__))
__asset_dir = path.join(__dot, '../../assets')

def register_routes(blueprint):

    @blueprint.route('/assets/<path:path>')
    def serve_assets(path):
        return send_from_directory(__asset_dir, path)