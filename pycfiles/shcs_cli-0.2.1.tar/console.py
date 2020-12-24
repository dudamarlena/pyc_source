# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/shcs_cli/shcs_cli/console.py
# Compiled at: 2016-09-12 15:12:47
from __future__ import print_function
import cmd, sys
from myterm.table import Table
from shcs_cli import __version__ as VERSION
import os.path

class Console(cmd.Cmd):
    """Console of shcs server"""
    prompt = '>>>'

    def __init__(self, cli, *arg, **kw):
        cmd.Cmd.__init__(self, *arg, **kw)
        self.cli = cli
        self.path = ''

    def _add_path(self, path):
        if path == '..':
            return ('/').join(self.path.split('/')[:-1])
        if len(self.path):
            return self.path + '/' + path
        return path

    def check_dir(self, path):
        try:
            test = self.cli.post('ws/path', login=True, path=('/').join(path.split('/')[:-1]))
            if path.split('/')[(-1)] not in [ t['name'] for t in test['dirs'] ] and path != '':
                return False
            return True
        except:
            return False

    def check_file(self, path):
        try:
            test = self.cli.post('ws/path', login=True, path=('/').join(path.split('/')[:-1]))
            if path.split('/')[(-1)] not in [ t['name'] for t in test['files'] ] and path != '':
                return False
            return True
        except:
            return False

    def do_cd(self, path):
        """cd {dir} : change directory"""
        if path:
            path = self._add_path(path)
            if self.check_dir(path):
                self.path = path
            else:
                print('%s not exist' % path, file=sys.stderr)
        else:
            print('nopath', file=sys.stderr)

    def help_cd(self):
        print(self.do_cd.__doc__)

    def do_pwd(self, arg):
        """pwd : print current directory"""
        print(self.path, file=sys.stdinfo)

    def help_pwd(self):
        print(self.do_pwd.__doc__)

    def do_ls(self, arg):
        """ls : print list of files and directory"""
        res = self.cli.post('ws/path', login=True, path=self.path)
        for d in res['dirs']:
            print('d %s' % d['name'], file=sys.stdinfo)

        for f in res['files']:
            print('  %s' % f['name'], file=sys.stdout)

    def help_ls(self):
        print(self.do_ls.__doc__)

    def do_ll(self, arg):
        self.do_ls(arg)

    def help_ll(self):
        print(self.do_ls.__doc__)

    def do_version(self, arg):
        """version : print current version client and server"""
        versions = Table()
        versions.add_columns('module', 'version')
        versions.append(*self.cli.get('ws/version'))
        versions.append({'module': 'shcs_cli', 'version': VERSION})
        versions.append({'module': 'python local', 'version': ('.').join([ str(a) for a in sys.version_info[0:3] ])})
        versions.orderby('module')
        versions.pprint(noheader=True)

    def help_version(self):
        print(self.do_version.__doc__)

    def do_get(self, path):
        """get {file} : get file from server on current working directory local"""
        path = self._add_path(path)
        if self.check_file(path):
            res = self.cli.get(path, login=True)
            with open(path.split('/')[(-1)], 'wb') as (file_):
                file_.write(res._content)
            print('download %s is ok' % path.split('/')[(-1)], file=sys.stdinfo)
        else:
            print('%s not exist' % path, file=sys.stderr)

    def help_get(self):
        print(self.do_get.__doc__)

    def do_put(self, src):
        """put {file} : upload file on server on current directory"""
        self.cli.post('ws/uploadcli/' + self.path + '/' + os.path.basename(src), login=True, data=open(src, 'rb'))
        print('upload is ok', file=sys.stdinfo)

    def help_put(self):
        print(self.do_put.__doc__)

    def do_mkdir(self, path):
        """mkdir {dir} : create directory"""
        if not self.check_dir(self._add_path(path)) and not self.check_file(self._add_path(path)):
            self.cli.post('ws/mkdir', login=True, path=self.path, name=path)
            print('%s is created' % path, file=sys.stdinfo)
        else:
            print('%s exist' % path, file=sys.stderr)

    def help_mkdir(self):
        print(self.do_mkdir.__doc__)

    def do_rm(self, path):
        """rm {path} : delete directrory or file"""
        path = self._add_path(path)
        if self.check_dir(path):
            self.cli.post('ws/rm', login=True, path=path)
            print('%s is deleted' % path, file=sys.stdinfo)
        else:
            print('%s not exist' % path, file=sys.stderr)

    def help_rm(self):
        print(self.do_rm.__doc__)

    def default(self, line):
        sys.stderr.write('*** Unknown syntax: %s\n' % line)

    def do_exit(self, arg):
        """quit console"""
        sys.exit(1)