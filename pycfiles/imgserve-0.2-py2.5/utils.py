# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/imgserve/utils.py
# Compiled at: 2009-08-22 09:32:49
"""
Various utility functions, some code taken from Lamson project by Zed
Shaw
"""
import sys, os, stat, signal, atexit, tempfile, daemon, socket
from daemon.pidlockfile import PIDLockFile
from lockfile import NotLocked, NotMyLock
from imgserve.logfile import ManagedStdio

class CustomPIDLockFile(PIDLockFile):

    def release(self):
        """Ignore NotMyLock exception to avoid error in child process"""
        if os.getpid() != self.read_pid():
            return
        try:
            PIDLockFile.release(self)
        except (NotLocked, NotMyLock):
            raise


def get_filelike_log(logdir):
    logpath = os.path.join(logdir, 'imgserve.log')
    if not os.path.exists(logdir):
        os.makedirs(logdir)
        os.chmod(logdir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    output = ManagedStdio(logpath)
    if os.path.exists(logpath):
        try:
            os.chmod(logpath, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
        except:
            print 'unable to chmod log file to %s' % '640'

    return output


def daemonize(pid, chdir, chroot, umask, files_preserve=None, do_open=True, data=None):
    """
    Uses python-daemonize to do all the junk needed to make a server a
    server.  It supports all the features daemonize has, except that
    chroot probably won't work at all without some serious
    configuration on the system.
    """
    context = daemon.DaemonContext()
    context.pidfile = CustomPIDLockFile(pid)
    context.files_preserve = files_preserve or []
    context.working_directory = os.path.expanduser(chdir)
    context.signal_map = {signal.SIGHUP: lambda signum, frame: data.stop(), 
       signal.SIGTERM: lambda signum, frame: data.kill()}
    if chroot:
        context.chroot_directory = os.path.expanduser(chroot)
    if umask != False:
        context.umask = umask
    if do_open:
        context.open()
    return context


def drop_priv(uid, gid):
    """
    Changes the uid/gid to the two given, you should give
    utils.daemonize 0,0 for the uid,gid so that it becomes root, which
    will allow you to then do this.
    """
    print 'Dropping to uid=%d, gid=%d' % (uid, gid)
    daemon.daemon.change_process_owner(uid, gid)
    print 'Now running as uid=%d, gid=%d' % (os.getgid(), os.getuid())


def check_for_pid(pid, FORCE):
    """
    Checks if a pid file is there, and if it is sys.exit.  If FORCE
    given then it will remove the file and not exit if it's there.
    """
    if os.path.exists(pid):
        if not FORCE:
            print 'PID file %s exists, so assuming daemon is running.  Give -FORCE to force it to start.' % pid
            sys.exit(1)
            return
        else:
            os.unlink(pid)
    else:
        dirname = os.path.dirname(pid)
        if not os.path.exists(dirname):
            os.makedirs(dirname)


def start_server(pid, logdir, FORCE, chroot, chdir, uid, gid, umask, loader, host, port):
    """
    Starts the server by doing a daemonize and then dropping priv
    accordingly.  It will only drop to the uid/gid given if both are
    given.
    """
    check_for_pid(pid, FORCE)
    if uid and gid:
        drop_priv(uid, gid)
    elif uid or gid:
        print 'You probably meant to give a uid and gid, but you gave: uid=%r, gid=%r.  Will not change to any user.' % (uid, gid)
    port_in_use = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
        except socket.error, msg:
            print msg
            port_in_use = True

    finally:
        sock.close()

    if port_in_use:
        sys.exit(1)
    manager = loader()
    daemonize(pid, chdir, chroot, umask, files_preserve=[], data=manager)
    output = get_filelike_log(logdir)
    sys.stdout = output
    sys.stderr = output
    print '---------------------------'
    print 'imgserve initializing ...'
    print '---------------------------'
    manager.start(host, port)


def get_filename_parts_from_url(url):
    """
    Get the file basename and extention tuple from a url string.
    """
    fullname = url.split('/')[(-1)].split('#')[0].split('?')[0]
    t = list(os.path.splitext(fullname))
    if t[1]:
        t[1] = t[1][1:]
    return t


def make_reply(which, data=None):
    """
    Return a reply object that is going to be returned to users.

    `which' tells which reply to make.  `data' can be used to pass
    extra data that reply object may pass to users.
    """
    reply = {'valid': {'dstURL': data}, 'parse': {'msg': 'request parse error'}, 'invalid': {'msg': 'request invalid', 'code': data}}
    if which not in reply.keys():
        return
    return reply[which]


def make_filepath(filename=None, suffix=''):
    new_dir = tempfile.mkdtemp()
    if not filename:
        (fd, filepath) = tempfile.mkstemp(suffix=suffix, dir=new_dir)
        os.close(fd)
    else:
        filepath = os.path.join(new_dir, filename)
    return filepath


def clean_filepath(filepath):
    if os.path.exists(filepath):
        os.unlink(filepath)
    parent_dir = os.path.dirname(filepath)
    if os.path.exists(parent_dir):
        os.rmdir(parent_dir)