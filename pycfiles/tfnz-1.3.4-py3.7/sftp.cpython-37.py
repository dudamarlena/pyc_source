# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/sftp.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 6250 bytes
import os, weakref, logging
from paramiko import SFTPServerInterface, SFTPAttributes, SFTPHandle
from paramiko.sftp import SFTP_OK
from paramiko.sftp_server import SFTPServer

class Sftp(SFTPServerInterface):
    __doc__ = 'Proxy object for a filesystem'

    def __init__(self, transport):
        super().__init__(transport)
        self.node_pk = transport.parent().node().pk
        self.container = weakref.ref(transport.container())
        self.conn = weakref.ref(transport.container().conn())

    def list_folder(self, directory):
        ls = self.conn().send_blocking_cmd(b'ls_dir', {'node':self.node_pk,  'container':self.container().uuid, 
         'directory':directory})
        rtn = []
        if 'error' in ls.params:
            return SFTPServer.convert_errno(ls.params['error'])
        for entry in ls.params['entries']:
            attr = SFTPAttributes.from_stat(os.stat_result(entry[1]), entry[0])
            rtn.append(attr)

        return rtn

    def stat(self, path):
        stat = self.conn().send_blocking_cmd(b'stat_file', {'node':self.node_pk,  'container':self.container().uuid, 
         'filename':path})
        if 'error' in stat.params:
            return SFTPServer.convert_errno(stat.params['error'])
        return SFTPAttributes.from_stat(os.stat_result(stat.params['stat']))

    def lstat(self, path):
        stat = self.conn().send_blocking_cmd(b'lstat_file', {'node':self.node_pk,  'container':self.container().uuid, 
         'filename':path})
        if 'error' in stat.params:
            return SFTPServer.convert_errno(stat.params['error'])
        return SFTPAttributes.from_stat(os.stat_result(stat.params['lstat']))

    def open(self, path, flags, attr):
        return SftpFile(flags, self.node_pk, self.container, path)

    def remove(self, path):
        rm = self.conn().send_blocking_cmd(b'rm_file', {'node':self.node_pk,  'container':self.container().uuid, 
         'filename':path})
        if 'error' in rm.params:
            return SFTPServer.convert_errno(rm.params['error'])
        return SFTP_OK

    def rename(self, path, newpath):
        mv = self.conn().send_blocking_cmd(b'mv_file', {'node':self.node_pk,  'container':self.container().uuid, 
         'filename':path, 
         'newpath':newpath})
        if 'error' in mv.params:
            return SFTPServer.convert_errno(mv.params['error'])
        return SFTP_OK

    def mkdir(self, path, attr):
        md = self.conn().send_blocking_cmd(b'mk_dir', {'node':self.node_pk,  'container':self.container().uuid, 
         'directory':path})
        if 'error' in md.params:
            return SFTPServer.convert_errno(md.params['error'])
        return SFTP_OK

    def rmdir(self, path):
        rm = self.conn().send_blocking_cmd(b'rm_dir', {'node':self.node_pk,  'container':self.container().uuid, 
         'directory':path})
        if 'error' in rm.params:
            return SFTPServer.convert_errno(rm.params['error'])
        return SFTP_OK

    def __repr__(self):
        return '<tfnz.sftp.Sftp object at %x (container=%s)>' % (id(self), self.container().uuid.decode())


class SftpFile(SFTPHandle):
    __doc__ = 'Proxy object for an actual file'

    def __init__(self, flags, node_pk, container, filename):
        super().__init__(flags)
        logging.debug('Opened a file via sftp: ' + filename)
        self.node_pk = node_pk
        self.container = container
        self.filename = filename
        try:
            self.data = bytearray(container().fetch(filename))
            logging.debug('...retrieved file: ' + filename)
        except ValueError:
            self.data = bytearray()
            logging.debug('...will create new file on writing: ' + filename)

    def read(self, offset, length):
        mv = memoryview(self.data)
        return bytes(mv[offset:offset + length])

    def write(self, offset, data):
        self.data[offset:offset + len(data)] = data
        self.container().conn().send_blocking_cmd(b'write_file', {'node':self.node_pk,  'container':self.container().uuid, 
         'filename':self.filename, 
         'offset':offset},
          bulk=data)
        return SFTP_OK

    def close(self):
        logging.debug('Closed a file via sftp: ' + self.filename)
        return SFTP_OK