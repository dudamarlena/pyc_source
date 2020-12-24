# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/upload.py
# Compiled at: 2018-09-13 11:06:18
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'

class Upload(object):

    def __init__(self, host, username, password, id):
        self.callbacks = {}
        self.id = id
        self.host = host
        self.username = username
        self.password = password

    def Upload(self, hostdir='.', text='*.*', binary='', src='.'):
        """
        Upload a set of files.
        Source files are found in the directory named by `src`
        (and its subdirectories recursively).  The files are uploaded
        to the directory named by `hostdir` on the remote host.
        Files that match one of the space-separated patterns in `text`
        are uploaded as text files, those that match the patterns in
        `binary` are uploaded as binary files.
        """
        pass