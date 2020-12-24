# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/templates/constants_templates.py
# Compiled at: 2020-05-07 07:40:51
# Size of source mod 2**32: 340 bytes
"""Module: constants templates"""
from jinja2 import Template
CONSTANTS_BASE_FILE = Template('from helpers import Helper\n\nAPI_PREFIX = ""\n\n')
CONSTANTS_FILE = Template('from helpers import Helper\n\n{% for const in constants %}# value type -> {{ const.value_type }}\n{{ const.name }} = [{{ const.val }}]\n{% endfor %}\n')