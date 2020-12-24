# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/projects_base/base/views.py
# Compiled at: 2020-04-25 05:24:47
# Size of source mod 2**32: 349 bytes
import os
from projects_base.base import base_blueprint
from projects_base.base.conf import config
from flask import send_from_directory

@base_blueprint.route('/images/<path:filename>', methods=['GET'])
def img_render(filename):
    return send_from_directory((os.path.abspath(config.get('BASE', 'upload_folder'))),
      filename=filename)