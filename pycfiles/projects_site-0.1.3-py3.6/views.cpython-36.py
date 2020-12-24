# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/projects_base/base/views.py
# Compiled at: 2020-04-20 14:39:32
# Size of source mod 2**32: 349 bytes
import os
from projects_base.base import base_blueprint
from projects_base.base.conf import config
from flask import send_from_directory

@base_blueprint.route('/images/<path:filename>', methods=['GET'])
def img_render(filename):
    return send_from_directory((os.path.abspath(config.get('BASE', 'upload_folder'))),
      filename=filename)