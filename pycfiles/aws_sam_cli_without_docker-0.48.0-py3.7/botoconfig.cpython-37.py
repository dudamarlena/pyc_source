# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/botoconfig.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 444 bytes
"""
Automatically add user agent string to boto configs.
"""
from botocore.config import Config
from samcli import __version__
from samcli.cli.global_config import GlobalConfig

def get_boto_config_with_user_agent(**kwargs):
    gc = GlobalConfig()
    return Config(user_agent_extra=f"aws-sam-cli/{__version__}/{gc.installation_id}" if gc.telemetry_enabled else f"aws-sam-cli/{__version__}", **kwargs)