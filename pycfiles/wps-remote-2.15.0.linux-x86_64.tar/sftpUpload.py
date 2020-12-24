# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/sftpUpload.py
# Compiled at: 2018-09-13 11:06:18
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import paramiko, pickle, sys, md5, os, string, logging, path, upload

class EzFtp:
    """
    A simplified interface to ftplib.

    Lets you use full pathnames, with server-side
    directory management handled automatically.
    """

    def __init__(self, ftp):
        self.ftp = ftp
        self.serverDir = ''

    def setRoot(self, dir):
        """
        Set the remote directory that we'll call the root.
        """
        self.cd(dir, create=True)
        self.ftp.exec_command('cd ..; pwd')
        self.ftp.exec_command('cd ' + dir + '; pwd')

    def cd(self, dir, create=1):
        """
        Change the directory on the server, if need be.
        If create is true, directories are created if necessary to get to the full path.
        Returns true if the directory is changed.
        """
        if dir != self.serverDir:
            while not dir.startswith(self.serverDir):
                logging.info('ftpcd ..')
                self.ftp.exec_command('cd ..; pwd')
                self.serverDir = os.path.split(self.serverDir)[0]

            doDirs = dir[len(self.serverDir):]
            for d in string.split(doDirs, os.sep):
                if d:
                    try:
                        logging.info('ftpcd %s' % d)
                        self.ftp.exec_command('cd ' + d + '; pwd')
                    except:
                        if create:
                            logging.info('ftpmkdir %s' % d)
                            try:
                                self.ftp.mkdir(d)
                            except:
                                pass

                            self.ftp.exec_command('cd ' + d + '; pwd')
                        else:
                            return 0

                    self.serverDir = os.path.join(self.serverDir, d)

        return 1

    def putasc(self, this, that):
        """
        Put a text file to the server.
        """
        thatDir, thatFile = os.path.split(that)
        self.cd(thatDir)
        f = open(this, 'r')
        logging.info('ftpstorasc %s' % that)
        self.ftp.putfo(f, thatFile)

    def putbin(self, this, that):
        """
        Put a binary file to the server.
        """
        thatDir, thatFile = os.path.split(that)
        self.cd(thatDir)
        f = open(this, 'rb')
        logging.info('ftpstorbin %s' % that)
        self.ftp.putfo(f, thatFile)

    def delete(self, that):
        """
        Delete a file on the server.
        """
        thatDir, thatFile = os.path.split(that)
        if self.cd(thatDir, 0):
            logging.info('ftpdel %s' % that)
            try:
                self.ftp.remove(thatFile)
            except:
                pass

    def quit(self):
        """
        Quit.
        """
        self.ftp.close()


class SFtpUpload(upload.Upload):
    """
    Provides intelligent FTP uploading of files, using MD5 hashes to track
    which files have to be uploaded.  Each upload is recorded in a local
    file so that the next upload can skip the file if its contents haven't
    changed.  File timestamps are ignored, allowing regenerated files to
    be properly uploaded only if their contents have changed.

    Call `setHost` and `setMd5File` to establish the settings for a session,
    then `upload` for each set of files to upload.  If you want to have
    removed local files automatically delete the remote files, call
    `deleteOldFiles` once, then `finish` to perform the closing bookkeeping.

    ::

        fu = SFtpUpload(config, 'ftp.myhost.com', 'myusername', 'password')
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
        self.setHost(host, username, password)
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
        try:
            hoststr, portstr = host.split(':')
        except:
            hoststr = host
            portstr = None

        if portstr:
            transport = paramiko.Transport((hoststr, int(portstr)))
        else:
            transport = paramiko.Transport((hoststr, 22))
        transport.connect(username=username, password=password)
        self.ftp = paramiko.SFTPClient.from_transport(transport)
        return

    def setMd5File(self, md5file):
        """
        Assign a filename to use for the MD5 tracking.
        """
        self.md5file = md5file
        if self.md5file:
            try:
                inf = open(self.md5file, 'r')
                self.md5DictIn = pickle.load(inf)
                self.md5DictUp.update(self.md5DictIn)
                inf.close()
            except IOError:
                self.md5DictIn = {}

    def Upload(self, hostdir='.', text='*.*', binary='', src='.'):
        """
        Upload a set of files.
        Source files are found in the directory named by `src`
        (and its subdirectories recursively).  The files are uploaded
        to the directory named by `hostdir` on the remote host.
        Files that match one of the space-separated patterns in `text`
        are uploaded as text files, those that match the patterns in
        `binary` are uploaded as binary files.

        This method can be called a number of times to upload different
        sets of files to or from different directories within the same
        FtpUpload session.
        """
        if not self.ezftp:
            if not self.ftp:
                self.setHost(self.host, self.username, self.password)
            self.ezftp = EzFtp(self.ftp)
        if hostdir != '.':
            self.ezftp.setRoot('/')
            self.ezftp.setRoot(hostdir)
        patdict = {}
        for pat in text.split():
            patdict[pat] = self.ezftp.putasc

        for pat in binary.split():
            patdict[pat] = self.ezftp.putbin

        srcpath = path.path(src)
        for thispath in srcpath.walkfiles():
            thatpath = hostdir + os.sep + srcpath.relpathto(thispath)
            logging.info('thatpath %s' % thatpath)
            thatpathstr = str(thatpath)
            m = md5.new()
            f = open(thispath, 'rb')
            for l in f.readlines():
                m.update(l)

            thisMd5 = m.hexdigest()
            thatMd5 = self.md5DictIn.get(thatpathstr, '')
            if thisMd5 != thatMd5:
                for pat in patdict.keys():
                    if thispath.fnmatch(pat):
                        ftpfn = patdict[pat]
                        ftpfn(thispath, thatpath)

            self.md5DictOut[thatpathstr] = thisMd5
            self.md5DictUp[thatpathstr] = thisMd5

    def deleteOldFiles(self):
        """
        Delete any remote files that we have uploaded previously but
        that weren't considered in this FtpUpload session.  This doesn't
        touch files that exist on the remote host but were never uploaded
        by this module.
        """
        for this in self.md5DictIn:
            if this not in self.md5DictOut:
                self.ezftp.delete(this)
                del self.md5DictUp[this]

    def finish(self):
        """
        Do our final bookkeeping.
        """
        self.ezftp.quit()
        if self.md5file:
            outf = open(self.md5file, 'w')
            pickle.dump(self.md5DictUp, outf)
            outf.close()