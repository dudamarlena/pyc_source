# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/aws/aws_tools.py
# Compiled at: 2019-03-25 20:26:52
# Size of source mod 2**32: 614 bytes
import socket, requests
from foxylib.tools.http.http_tools import HttpToolkit

class AWSToolkit:

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
            r = HttpToolkit.url_retries2httpr('http://169.254.169.254/latest/meta-data/public-ipv4', max_retries=5)
            return r or None
        return r.text