# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/spider/smbspider.py
# Compiled at: 2016-12-29 01:49:52
from time import time, strftime, localtime
from cme.remotefile import RemoteFile
from impacket.smb3structs import FILE_READ_DATA
from impacket.smbconnection import SessionError
from sys import exit
import re, traceback

class SMBSpider:

    def __init__(self, connection):
        self.logger = connection.logger
        self.smbconnection = connection.conn
        self.start_time = time()
        self.args = connection.args
        self.results = None
        self.regex = None
        if self.args.regex:
            try:
                self.regex = [ re.compile(regex) for regex in self.args.regex ]
            except Exception as e:
                self.logger.error(('Regex compilation error: {}').format(e))
                exit(1)

        self.logger.info('Started spidering')
        return

    def get_lastm_time(self, result_obj):
        lastm_time = None
        try:
            lastm_time = strftime('%Y-%m-%d %H:%M', localtime(result_obj.get_mtime_epoch()))
        except Exception:
            pass

        return lastm_time

    def spider(self, subfolder, depth):
        """
            Apperently spiders don't like stars *!
            who knew? damn you spiders
        """
        if subfolder == '' or subfolder == '.':
            subfolder = '*'
        else:
            if subfolder.startswith('*/'):
                subfolder = subfolder[2:] + '/*'
            else:
                subfolder = subfolder.replace('/*/', '/') + '/*'
            filelist = None
            try:
                filelist = self.smbconnection.listPath(self.args.share, subfolder)
                self.dir_list(filelist, subfolder)
                if depth == 0:
                    return
            except SessionError as e:
                if not filelist:
                    self.logger.error(('Failed to connect to share {}: {}').format(self.args.share, e))
                    return

            for result in filelist:
                if result.is_directory() and result.get_longname() != '.' and result.get_longname() != '..':
                    if subfolder == '*':
                        self.spider(subfolder.replace('*', '') + result.get_longname(), depth - 1)
                    elif subfolder != '*' and subfolder[:-2].split('/')[(-1)] not in self.args.exclude_dirs:
                        self.spider(subfolder.replace('*', '') + result.get_longname(), depth - 1)

        return

    def dir_list(self, files, path):
        path = path.replace('*', '')
        for result in files:
            if self.args.pattern:
                for pattern in self.args.pattern:
                    if result.get_longname().lower().find(pattern.lower()) != -1:
                        if result.is_directory():
                            self.logger.highlight(('//{}/{}{} [dir]').format(self.args.share, path, result.get_longname()))
                        else:
                            self.logger.highlight(("//{}/{}{} [lastm:'{}' size:{}]").format(self.args.share, path, result.get_longname(), 'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result), result.get_filesize()))

            elif self.regex:
                for regex in self.regex:
                    if regex.findall(result.get_longname()):
                        if result.is_directory():
                            self.logger.highlight(('//{}/{}{} [dir]').format(self.args.share, path, result.get_longname()))
                        else:
                            self.logger.highlight(("//{}/{}{} [lastm:'{}' size:{}]").format(self.args.share, path, result.get_longname(), 'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result), result.get_filesize()))

            if self.args.content:
                if not result.is_directory():
                    self.search_content(path, result)

    def search_content(self, path, result):
        path = path.replace('*', '')
        try:
            rfile = RemoteFile(self.smbconnection, path + result.get_longname(), self.args.share, access=FILE_READ_DATA)
            rfile.open()
            while True:
                try:
                    contents = rfile.read(4096)
                    if not contents:
                        break
                except SessionError as e:
                    if 'STATUS_END_OF_FILE' in str(e):
                        break
                except Exception:
                    traceback.print_exc()
                    break

                if self.args.pattern:
                    for pattern in self.args.pattern:
                        if contents.lower().find(pattern.lower()) != -1:
                            self.logger.highlight(("//{}/{}{} [lastm:'{}' size:{} offset:{} pattern:'{}']").format(self.args.share, path, result.get_longname(), 'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result), result.get_filesize(), rfile.tell(), pattern))

                elif self.regex:
                    for regex in self.regex:
                        if regex.findall(contents):
                            self.logger.highlight(("//{}/{}{} [lastm:'{}' size:{} offset:{} regex:'{}']").format(self.args.share, path, result.get_longname(), 'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result), result.get_filesize(), rfile.tell(), regex.pattern))

            rfile.close()
            return
        except SessionError as e:
            if 'STATUS_SHARING_VIOLATION' in str(e):
                pass
        except Exception:
            traceback.print_exc()

    def finish(self):
        self.logger.info(('Done spidering (Completed in {})').format(time() - self.start_time))