# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sslmanage/base.py
# Compiled at: 2019-07-05 06:05:21
# Size of source mod 2**32: 582 bytes
import logging
logging.basicConfig(filename='/tmp/upssl.log', level=(logging.INFO),
  format='%(asctime)s %(message)s',
  datefmt='%m/%d/%Y %I:%M:%S %p')
log_info = logging.info

class BaseSsl:

    def __init__(self, cert_file, key_file):
        self.cert_file = cert_file
        self.key_file = key_file

    def _get_ssl(self):
        with open(self.cert_file, 'r+') as (f_ca):
            self.cert = f_ca.read()
        with open(self.key_file, 'r+') as (f_pri):
            self.cert_key = f_pri.read()