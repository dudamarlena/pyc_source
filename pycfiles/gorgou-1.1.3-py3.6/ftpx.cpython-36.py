# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/x/ftpx.py
# Compiled at: 2018-02-04 06:44:34
# Size of source mod 2**32: 790 bytes
from ftplib import FTP

def downloadfile(host, username, password, remotepath, localpath):
    ftp = FTP()
    ftp.connect(host, 21)
    ftp.login(username, password)
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
    ftp.quit()


def uploadfile(host, username, password, remotepath, localpath):
    ftp = FTP()
    ftp.connect(host, 21)
    ftp.login(username, password)
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
    ftp.quit()