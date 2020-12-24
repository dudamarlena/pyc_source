# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/constants.py
# Compiled at: 2019-12-16 16:08:11
# Size of source mod 2**32: 535 bytes
from .helpers import django_service, flask_service, start_super_jopi_infra
CLI_SERVICE_SPLASH = '\n    ___________     __    __          \n    \\__    ___/___ |  | _|  | ______  \n      |    | /    \\|  |/ /  |/ /    \\ \n      |    |(  []  )    <|    <  []  )\n      |____| \\____/|__|_ \\__|_ \\____/ \n                        \\/    \\/      \n'
FLASK = 'flask'
DJANGO = 'django'
SUPER_JOPI = 'super-jopi'
AVAILABLE_TEMPLATES = {FLASK: flask_service, DJANGO: django_service}
AVAILABLE_INFRA = {SUPER_JOPI: start_super_jopi_infra}