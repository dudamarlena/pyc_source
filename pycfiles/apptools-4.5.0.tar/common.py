# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.6/site-packages/apptool/common.py
# Compiled at: 2010-10-09 01:07:17
import os, re, sys, zipfile, subprocess, cli

def mainWorkDir():
    return os.path.join(os.path.expanduser('~'), 'AppTool')


class ZipUtil(object):

    def __init__(self, zipwrite=False, zipextract=False, zipname=None):
        self.zipwrite = zipwrite
        self.zipextract = zipextract
        self.zipname = zipname
        self.appdir = os.path.join(mainWorkDir(), 'Apps')

    def _zipWrite(self):
        try:
            try:
                z = zipfile.ZipFile(self.zipname, 'w', zipfile.ZIP_DEFLATED)
                for (dp, dn, fn) in os.walk(self.appdir):
                    for f in fn:
                        abs = os.path.join(dp, f)
                        arc = abs[len(self.appdir) + 1:]
                        z.write(abs, arc)

            except (IOError, OSError), e:
                cli.warning(str(e))

        finally:
            z.close()

    def _zipExtract(self):
        try:
            e = zipfile.ZipFile(self.zipname, 'r')
            try:
                e.extractall()
            except (IOError, OSError), e:
                cli.warning(str(e))

        finally:
            e.close()

    def work(self):
        if self.zipwrite:
            return self._zipWrite()
        if self.zipextract:
            return self._zipExtract()


def adbPath():
    path = os.getenv('PATH').split(os.pathsep)
    if os.name == 'nt':
        adb = 'adb.exe'
    else:
        adb = 'adb'
    adbpath = None
    if '' in path:
        path.remove('')
    for p in path:
        if adb in os.listdir(p):
            adbpath = os.path.join(p, adb)
            break

    if not adbpath:
        return cli.error("`%s' not found anywhere in `PATH'" % adb)
    else:
        return adbpath


def device():
    adb = adbPath()
    d = subprocess.Popen([
     adb, 'devices'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    d = list(d.communicate())
    if '' in d:
        d.remove('')
    if len(d) > 1:
        return cli.error('Too many devices connected at once')
    if not re.findall('[0-9]', d[0]):
        return cli.error('No device connected at this time')
    return True


def adbPull(dest):
    adb = adbPath()
    if device():
        cmd_one = subprocess.Popen([
         adb, 'pull', '/data/app', os.path.join(dest, 'app')], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_one.communicate()
        cmd_two = subprocess.Popen([
         adb, 'pull', '/data/app-private', os.path.join(dest, 'app-private')], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_two.communicate()


def adbInstall(src):
    adb = adbPath()
    if device():
        cmd = subprocess.Popen([adb, 'install', src])
        cmd.communicate()