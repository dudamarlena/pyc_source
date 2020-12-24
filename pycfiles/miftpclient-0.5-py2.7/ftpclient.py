# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/miftpclient/ftpclient.py
# Compiled at: 2015-09-05 02:29:16
import subprocess

def connect_server(ftp_ip):
    cmd = 'firefox ftp://%s:2121' % ftp_ip
    subprocess.call(cmd, shell=True)