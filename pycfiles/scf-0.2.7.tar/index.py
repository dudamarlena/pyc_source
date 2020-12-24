# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-MsePIp/scf/tcfcli/cmds/init/templates/tcf-demo-python/{{cookiecutter.project_name}}/index.py
# Compiled at: 2019-12-02 05:04:19


def main_handler(event, context):
    print str(event)
    return 'hello world'