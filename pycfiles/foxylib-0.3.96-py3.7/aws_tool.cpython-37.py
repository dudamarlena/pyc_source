# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/aws/aws_tool.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 587 bytes
import socket
from foxylib.tools.http.http_tool import HttpTool

class AWSTool:

    @classmethod
    def hostname2is_aws(cls, hostname):
        if hostname.startswith('domU-'):
            return True
        if hostname.startswith('ip-'):
            return True
        return False

    @classmethod
    def aws2ip(cls):
        hostname = socket.gethostname()
        if not cls.hostname2is_aws(hostname):
            return
        else:
            r = HttpTool.url_retries2httpr('http://169.254.169.254/latest/meta-data/public-ipv4', max_retries=5)
            return r or None
        return r.text