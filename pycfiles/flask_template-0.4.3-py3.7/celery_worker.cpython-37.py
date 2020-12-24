# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/mongo/celery_worker.py
# Compiled at: 2020-04-01 02:43:02
# Size of source mod 2**32: 162 bytes
from proj import create_app
from proj.extensions import celery
app = create_app()
app.app_context().push()