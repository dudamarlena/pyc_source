# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/static_config.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 2326 bytes
from __future__ import print_function
import os, json
from typing import Dict
from flask import url_for
manifest = dict()

def configure_manifest_files(app):
    """
    Loads the manifest file and register the `url_for_asset_` template tag.
    :param app:
    :return:
    """

    def parse_manifest_json():
        global manifest
        try:
            manifest_file = os.path.join(os.path.dirname(__file__), 'static/dist/manifest.json')
            with open(manifest_file, 'r') as (f):
                manifest.update(json.load(f))
                for k in manifest.keys():
                    manifest[k] = os.path.join('dist', manifest[k])

        except Exception:
            print('Please make sure to build the frontend in static/ directory and restart the server')

    def get_asset_url(filename):
        if app.debug:
            parse_manifest_json()
        return url_for('static', filename=(manifest.get(filename, '')))

    parse_manifest_json()

    @app.context_processor
    def get_url_for_asset():
        return dict(url_for_asset=get_asset_url)