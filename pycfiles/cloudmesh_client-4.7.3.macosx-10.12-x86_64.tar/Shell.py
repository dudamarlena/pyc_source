# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/Shell.py
# Compiled at: 2017-04-25 11:50:32
from __future__ import print_function
from pipes import quote
import errno, glob, os, os.path, platform, subprocess, zipfile
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.util import path_expand

class SubprocessError(Exception):

    def __init__(self, cmd, returncode, stderr, stdout):
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout

    def __str__(self):

        def indent(lines, amount, ch=' '):
            padding = amount * ch
            return padding + ('\n' + padding).join(lines.split('\n'))

        cmd = (' ').join(map(quote, self.cmd))
        s = ''
        s += 'Command: %s\n' % cmd
        s += 'Exit code: %s\n' % self.returncode
        if self.stderr:
            s += 'Stderr:\n' + indent(self.stderr, 4)
        if self.stdout:
            s += 'Stdout:\n' + indent(self.stdout, 4)
        return s


class Subprocess(object):

    def __init__(self, cmd, cwd=None, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=None):
        Console.debug_msg(('Running cmd: {}').format((' ').join(map(quote, cmd))))
        proc = subprocess.Popen(cmd, stderr=stderr, stdout=stdout, cwd=cwd, env=env)
        stdout, stderr = proc.communicate()
        self.returncode = proc.returncode
        self.stderr = stderr
        self.stdout = stdout
        if self.returncode != 0:
            raise SubprocessError(cmd, self.returncode, self.stderr, self.stdout)


class Shell(object):
    cygwin_path = 'bin'
    command = {'windows': {}, 'linux': {}, 'darwin': {}}

    @classmethod
    def check_output(cls, *args, **kwargs):
        """Thin wrapper around :func:`subprocess.check_output`
        """
        return subprocess.check_output(*args, **kwargs)

    @classmethod
    def ls(cls, *args):
        return cls.execute('ls', args)

    @classmethod
    def ps(cls, *args):
        return cls.execute('ps', args)

    @classmethod
    def bash(cls, *args):
        return cls.execute('bash', args)

    @classmethod
    def cat(cls, *args):
        return cls.execute('cat', args)

    @classmethod
    def git(cls, *args):
        return cls.execute('git', args)

    @classmethod
    def VBoxManage(cls, *args):
        return cls.execute('VBoxManage', args)

    @classmethod
    def blockdiag(cls, *args):
        return cls.execute('blockdiag', args)

    @classmethod
    def cm(cls, *args):
        return cls.execute('cm', args)

    @classmethod
    def fgmetric(cls, *args):
        return cls.execute('fgmetric', args)

    @classmethod
    def fgrep(cls, *args):
        return cls.execute('fgrep', args)

    @classmethod
    def gchproject(cls, *args):
        return cls.execute('gchproject', args)

    @classmethod
    def gchuser(cls, *args):
        return cls.execute('gchuser', args)

    @classmethod
    def glusers(cls, *args):
        return cls.execute('glusers', args)

    @classmethod
    def gmkproject(cls, *args):
        return cls.execute('gmkproject', args)

    @classmethod
    def grep(cls, *args):
        return cls.execute('grep', args)

    @classmethod
    def gstatement(cls, *args):
        return cls.execute('gstatement', args)

    @classmethod
    def head(cls, *args):
        return cls.execute('head', args)

    @classmethod
    def keystone(cls, *args):
        return cls.execute('keystone', args)

    @classmethod
    def kill(cls, *args):
        return cls.execute('kill', args)

    @classmethod
    def ls(cls, *args):
        return cls.execute('ls', args)

    @classmethod
    def mongoimport(cls, *args):
        return cls.execute('mongoimport', args)

    @classmethod
    def mysql(cls, *args):
        return cls.execute('mysql', args)

    @classmethod
    def nosetests(cls, *args):
        return cls.execute('nosetests', args)

    @classmethod
    def nova(cls, *args):
        return cls.execute('nova', args)

    @classmethod
    def ping(cls, host=None, count=1):
        return cls.execute('ping', ('-c {} {}').format(count, host))

    @classmethod
    def pwd(cls, *args):
        return cls.execute('pwd', args)

    @classmethod
    def rackdiag(cls, *args):
        return cls.execute('rackdiag', args)

    @classmethod
    def rm(cls, *args):
        return cls.execute('rm', args)

    @classmethod
    def rsync(cls, *args):
        return cls.execute('rsync', args)

    @classmethod
    def scp(cls, *args):
        return cls.execute('scp', args)

    @classmethod
    def sort(cls, *args):
        return cls.execute('sort', args)

    @classmethod
    def sh(cls, *args):
        return cls.execute('sh', args)

    @classmethod
    def ssh(cls, *args):
        return cls.execute('ssh', args)

    @classmethod
    def sudo(cls, *args):
        return cls.execute('sudo', args)

    @classmethod
    def tail(cls, *args):
        return cls.execute('tail', args)

    @classmethod
    def vagrant(cls, *args):
        return cls.execute('vagrant', args)

    @classmethod
    def mongod(cls, *args):
        return cls.execute('mongod', args)

    @classmethod
    def grep(cls, *args):
        return cls.execute('grep', args)

    @classmethod
    def dialog(cls, *args):
        return cls.execute('dialog', args)

    @classmethod
    def pip(cls, *args):
        return cls.execute('pip', args)

    @classmethod
    def remove_line_with(cls, lines, what):
        result = []
        for line in lines:
            if what not in line:
                result = result + [line]

        return result

    @classmethod
    def find_lines_with(cls, lines, what):
        result = []
        for line in lines:
            if what in line:
                result = result + [line]

        return result

    def __init__(cls):
        if cls.operating_system() == 'windows':
            cls.find_cygwin_executables()

    @classmethod
    def find_cygwin_executables(cls):
        """
        find the executables 
        """
        exe_paths = glob.glob(cls.cygwin_path + '\\*.exe')
        for c in exe_paths:
            exe = c.split('\\')
            name = exe[1].split('.')[0]
            cls.command['windows'][name] = c

    @classmethod
    def terminal_type(cls):
        """
        returns  darwin, cygwin, cmd, or linux
        """
        what = platform.system().lower()
        kind = 'UNDEFINED_TERMINAL_TYPE'
        if 'linux' in what:
            kind = 'linux'
        elif 'darwin' in what:
            kind = 'darwin'
        elif 'cygwin' in what:
            kind = 'cygwin'
        elif 'windows' in what:
            kind = 'windows'
        return kind

    @classmethod
    def which(cls, command):
        t = cls.ttype()
        if 'windows' in t and cls.command_exists(name):
            return cls.command['windows'][name]
        else:
            if 'linux' in t:
                cmd = [
                 'which', command]
                result = subprocess.check_output(cmd).rstrip()
                if len(result) == 0:
                    return
                return result
            return

    @classmethod
    def command_exists(cls, name):
        t = cls.ttype()
        if 'windows' in t:
            cls.find_cygwin_executables()
            return name in cls.command['windows']
        if 'linux' in t:
            r = which(name)
            return r

    @classmethod
    def list_commands(cls):
        t = cls.ttype()
        if 'windows' in t:
            cls.find_cygwin_executables()
            print(('\n').join(cls.command['windows']))
        else:
            print('ERROR: this command is not supported for this OS')

    @classmethod
    def operating_system(cls):
        return platform.system().lower()

    @classmethod
    def execute(cls, cmd, arguments='', shell=False, cwd=None, traceflag=True, witherror=True):
        """Run Shell command

        :param cmd: command to run
        :param arguments: we dont know yet
        :param capture: if true returns the output
        :return:
        """
        result = None
        terminal = cls.terminal_type()
        os_command = [
         cmd]
        if terminal in ('linux', 'windows'):
            os_command = [
             cmd]
        else:
            if 'cygwin' in terminal:
                if not cls.command_exists(cmd):
                    print('ERROR: the command could not be found', cmd)
                    return
                os_command = [
                 cls.command[cls.operating_system()][cmd]]
            if isinstance(arguments, list):
                os_command = os_command + arguments
            elif isinstance(arguments, tuple):
                os_command = os_command + list(arguments)
            elif isinstance(arguments, str):
                os_command = os_command + arguments.split()
            else:
                print('ERROR: Wrong parameter type', type(arguments))
            if cwd is None:
                cwd = os.getcwd()
            try:
                if shell:
                    result = subprocess.check_output(os_command, stderr=subprocess.STDOUT, shell=True, cwd=cwd)
                else:
                    result = subprocess.check_output(os_command, stderr=subprocess.STDOUT, cwd=cwd)
            except:
                if witherror:
                    Console.error('problem executing subprocess', traceflag=traceflag)

        if result is not None:
            result = result.strip().decode()
        return result

    @classmethod
    def mkdir(cls, newdir):
        """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
        """
        newdir = path_expand(newdir)
        try:
            os.makedirs(newdir)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(newdir):
                pass
            else:
                raise

    def unzip(source_filename, dest_dir):
        """
        unzips a file into the destination directory
        :param dest_dir: the destination directory
        :return:
        """
        with zipfile.ZipFile(source_filename) as (zf):
            for member in zf.infolist():
                words = member.filename.split('/')
                path = path_expand(dest_dir)
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''):
                        continue
                    path = os.path.join(path, word)

                zf.extract(member, path)


def main():
    shell = Shell()
    print(shell.terminal_type())
    r = shell.execute('pwd')
    print(r)
    r = shell.execute('ls', ['-l', '-a'])
    print(r)
    r = shell.execute('ls', '-l -a')
    print(r)
    r = shell.ls('-aux')
    print(r)
    r = shell.ls('-a', '-u', '-x')
    print(r)
    r = shell.pwd()
    print(r)


if __name__ == '__main__':
    main()