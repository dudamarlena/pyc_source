# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/services/assets.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 2014 bytes
import json, os
from windflow.services import Service

class Assets(dict):

    def __init__(self, path, iterable=None, **kwargs):
        super().__init__(iterable or (), **kwargs)
        self._path = path

    def get_style(self, name):
        try:
            bundle = self[name]
        except KeyError as e:
            return ''

        try:
            return '<link href="' + os.path.join(self._path, bundle['css']) + '" rel="stylesheet">'
        except KeyError as e:
            return ''

    def get_script(self, name):
        try:
            bundle = self[name]
        except KeyError as e:
            return ''

        try:
            return '<script src="' + os.path.join(self._path, bundle['js']) + '" type="text/javascript"></script>'
        except KeyError as e:
            return ''


class UnavailableAssets(Assets):

    def get_style(self, name):
        return ''

    def get_script(self, name):
        return '<script type="text/javascript">document.write("Assets are not available. It may means that the bundling process is still running, or that the webpack AssetsPlugin did not run. Look for the assets.json file in your static directory (and look at webpack output).")</script>'


class WebpackAssets(Service):
    __doc__ = '\n    Webpack assets service.\n\n    Simply reads the output of the assets plugin (json) so it can be used in a templating context.\n\n    '
    filename = 'static/assets.json'
    path = '/'
    assets_type = Assets
    unavailable_assets_type = UnavailableAssets

    def get(self):
        try:
            with open(self.filename) as (f):
                return self.assets_type(self.path, json.load(f))
        except:
            return self.unavailable_assets_type(self.path)