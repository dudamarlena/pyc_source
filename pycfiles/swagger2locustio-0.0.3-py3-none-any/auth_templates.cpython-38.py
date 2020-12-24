# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/templates/auth_templates.py
# Compiled at: 2020-05-08 14:15:42
# Size of source mod 2**32: 829 bytes
"""Module: Auth templates"""
from jinja2 import Template
AUTH_BASIC = Template('\n        \'\'\' Security config\n        {{ security_config }}\n        \'\'\'\n        auth_str = str(os.getenv("TEST_USER_LOGIN")) + ":" + str(os.getenv("TEST_USER_PASSWORD"))\n        credentials = b64encode(auth_str.encode()).decode("utf-8")\n        credentials = "Basic " + credentials\n        self.client.headers.update({"Authorization": credentials})\n')
AUTH_KEY_HEADER = Template('\n        \'\'\' Security config\n        {{ security_config }}\n        \'\'\'\n        self.client.headers.update({"{{ name }}": str(os.getenv("TEST_USER_API_KEY"))})\n')
AUTH_UNDEFINED = Template('\n        \'\'\' Security config\n        {{ security_config }}\n        \'\'\'\n        raise NotImplementedError("You should add or delete auth")\n')