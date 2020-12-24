# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jon/.virtualenvs/kakeibox-presenter-json/lib/python3.7/site-packages/kakeibox_presenter_json/presenter/json_presenter.py
# Compiled at: 2019-10-16 22:14:34
# Size of source mod 2**32: 136 bytes
import json

class JsonPresenter(object):

    def show(self, str_json):
        return json.dumps(str_json, indent=4, sort_keys=True)