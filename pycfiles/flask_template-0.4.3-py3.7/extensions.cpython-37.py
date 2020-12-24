# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/simple/proj/extensions.py
# Compiled at: 2020-03-11 03:42:34
# Size of source mod 2**32: 113 bytes
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()