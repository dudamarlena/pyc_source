# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/ftpsUpload.py
# Compiled at: 2018-09-13 11:06:18
__author__ = 'Ned Batchelder'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import ftpUpload, ftplib, socket, ssl, pickle, sys, md5, os, string, logging, path, upload

class tyFTP(ftplib.FTP_TLS):

    def __init__(self, host='', user='', passwd='', acct='', keyfile=None, certfile=None, timeout=60):
        ftplib.FTP_TLS.__init__(self, host=host, user=user, passwd=passwd, acct=acct, keyfile=keyfile, certfile=certfile, timeout=timeout)

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        self.voidcmd('TYPE I')
        conn = self.transfercmd(cmd, rest)
        try:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)

            if isinstance(conn, ssl.SSLSocket):
                conn.unwrap()
        finally:
            conn.close()

        return self.voidresp()

    def storlines(self, cmd, fp, callback=None):
        self.voidcmd('TYPE A')
        conn = self.transfercmd(cmd)
        try:
            while 1:
                buf = fp.readline(self.maxline + 1)
                if len(buf) > self.maxline:
                    raise Error('got more than %d bytes' % self.maxline)
                if not buf:
                    break
                if buf[-2:] != CRLF:
                    if buf[(-1)] in CRLF:
                        buf = buf[:-1]
                    buf = buf + CRLF
                conn.sendall(buf)
                if callback:
                    callback(buf)

            if isinstance(conn, ssl.SSLSocket):
                conn.unwrap()
        finally:
            conn.close()

        return self.voidresp()


class FtpsUpload(ftpUpload.FtpUpload):
    """
    Provides intelligent FTPS uploading of files, using MD5 hashes to track
    which files have to be uploaded.  Each upload is recorded in a local
    file so that the next upload can skip the file if its contents haven't
    changed.  File timestamps are ignored, allowing regenerated files to
    be properly uploaded only if their contents have changed.

    Call `setHost` and `setMd5File` to establish the settings for a session,
    then `upload` for each set of files to upload.  If you want to have
    removed local files automatically delete the remote files, call
    `deleteOldFiles` once, then `finish` to perform the closing bookkeeping.

    ::

        fu = FtpsUpload(config, 'ftp.myhost.com', 'myusername', 'password')
        fu.setHost('ftp.myhost.com', 'myusername', 'password')
        fu.setMd5File('myhost.md5') # optional
        fu.upload(
            hostdir='www', src='.',
            text='*.html *.css', binary='*.gif *.jpg'
        )
        # more upload() calls can go here..
        fu.deleteOldFiles()
        fu.finish()

    """

    def __init__(self, host, username, password, id='master'):
        upload.Upload.__init__(self, host, username, password, id)
        self.ftp = None
        self.ezftp = None
        self.md5file = None
        self.md5DictIn = {}
        self.md5DictOut = {}
        self.md5DictUp = {}
        return

    def setHost(self, host, username, password):
        """
        Set the host, the username and password.
        """
        if not self.ftp:
            try:
                hoststr, portstr = host.split(':')
            except:
                hoststr = host
                portstr = None

            self.ftp = tyFTP(timeout=60)
            self.ftp.set_debuglevel(3)
            if portstr:
                port = int(portstr)
                self.ftp.connect(hoststr, port)
            else:
                self.ftp.connect(hoststr, 22)
            self.ftp.auth()
            self.ftp.login(username, password)
            self.ftp.prot_p()
            self.ftp.set_pasv(1)
        return