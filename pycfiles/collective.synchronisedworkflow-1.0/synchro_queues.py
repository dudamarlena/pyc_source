# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/scripts/synchro_queues.py
# Compiled at: 2008-12-16 18:21:20
import sys, os, os.path
from subprocess import Popen
from tempfile import gettempdir
from optparse import OptionParser
import logging
from utils import create_queue_structure
from utils import good_name
from utils import lock
from utils import unlock
from utils import islock
logger = logging.getLogger('collective.synchro')
SSH_CMD = 'ssh -o  PasswordAuthentication=no %s@%s %s'
_SYS_USER = None
_SYS_GRP = None

def main(args=None):
    parser = OptionParser()
    parser.add_option('-u', '--user', dest='user', help='user name (default current user)', default=get_sysuser())
    parser.add_option('-H', '--host', dest='host', help='the ip or adress of destination server (default localhost)', default='localhost')
    parser.add_option('-s', '--source', dest='source', help='the path of a synchro queue in local host (required)', default=None)
    parser.add_option('-d', '--dest', dest='dest', help='the path of a synchro queue in remote host (required)', default=None)
    parser.add_option('-l', '--logdir', dest='logdir', help='log localisation (by default system temp dir)', default=gettempdir())
    parser.add_option('-V', '--vardir', dest='var', help='log localisation (by default system temp dir)', default=gettempdir())
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', help='log localisation (by default system temp dir)', default=False)
    parser.add_option('-q', '--quiet', dest='quiet', action='store_false', help='print logging message in stdout', default=True)
    (options, args) = parser.parse_args()
    if not options.source or not options.dest:
        parser.print_help()
        sys.exit(-1)
    level = logging.INFO
    if options.verbose and not options.quiet:
        level = logging.DEBUG
    if options.quiet:
        logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(message)s', filename=os.path.join(options.logdir, 'synchro.log'), filemode='a')
    else:
        logging.basicConfig(level=level)
    lock_file = os.path.join(options.var, 'synchro.lock')
    lock(lock_file, logger)
    try:
        remote_queue = SshRemoteQueue(options.user, options.host, os.path.join(options.dest, 'IMPORT', 'TO_PROCESS'), options.var)
        queue = ExportQueue(options.source, remote_queue)
        queue.fire()
    finally:
        unlock(lock_file)
    return


def create_queue(args=None):
    parser = OptionParser()
    parser.add_option('-d', '--directory', dest='path', help='path to create')
    (options, args) = parser.parse_args()
    if not options.path:
        parser.print_help()
        sys.exit(-1)

    class Dir(object):
        __module__ = __name__

        def __init__(self, path):
            self.path = path

    create_queue_structure(Dir(options.path))


def get_sysuser():
    global _SYS_USER
    if _SYS_USER:
        return _SYS_USER
    envvars = ('LOGNAME', 'USER', 'USERNAME')
    for x in envvars:
        v = os.environ.get(x, None)
        if v:
            _SYS_USER = v
            return _SYS_USER

    try:
        import pwd
        _SYS_USER = pwd.getpwuid(os.getuid())[0]
        return _SYS_USER
    except:
        pass

    _SYS_USER = os.getlogin()
    return _SYS_USER


class ExportQueue(object):
    __module__ = __name__

    def __init__(self, path, remote_queue):
        """ constructor of a queue """
        self.path = path
        self.remote_queue = remote_queue
        create_queue_structure(self)

    def fire(self):
        """ move all file to be processing """
        for f in os.listdir(self.export_to_process_path):
            if not islock(f) and good_name(f):
                rf = os.path.basename(f)
                try:
                    os.rename(os.path.join(self.export_to_process_path, f), os.path.join(self.export_processing_path, rf))
                except IOError, e:
                    logger.exception('can not rename %s to %s' % os.path.join(self.export_to_process_path, f), os.path.join(self.export_processing_path, rf))
                    raise

        files = os.listdir(self.export_processing_path)
        files.sort(lambda x, y: cmp(float(good_name(x).groups()[1]), float(good_name(y).groups()[1])))
        for f in files:
            self.remote_queue.put(os.path.join(self.export_processing_path, f))

        if len(files):
            logger.info('found to synchronize %d files' % len(files))
            self.remote_queue.fire(self.export_done_path)
        else:
            logger.info('no file to synchronize between queues')


class SshRemoteQueue(object):
    __module__ = __name__

    def __init__(self, user, host, path, var):
        """ constructor of an Ssh Remote Queue """
        self.user = user
        self.host = host
        self.path = path
        self.var = var
        self.stderr = os.path.join(self.var, 'err')
        self.stdout = os.path.join(self.var, 'out')
        self.batch = os.path.join(self.var, 'batch')
        self.cmds = []
        self.errs = []
        self.outs = []
        self.puts = []
        if not self.exists(path):
            error = open(os.path.join(self.var, 'err'), 'r').read()
            raise SshError('%s' % error)

    def available(self):
        """ return True if succed """
        command = SSH_CMD % (self.user, self.host, 'ls')
        return self.cmd(command)

    def cmd(self, command):
        """ launch a command via popen """
        p = Popen(command, stdout=open(self.stdout, 'w'), stderr=open(self.stderr, 'w'), shell=True)
        sts = os.waitpid(p.pid, 0)
        self.errs.append(open(self.stderr, 'r').read())
        self.outs.append(open(self.stdout, 'r').read())
        self.cmds.append(command)
        logger.info(self.cmds[(-1)])
        if self.outs[(-1)]:
            logger.debug('stdout: %s' % self.outs[(-1)])
        if len(self.errs[(-1)]):
            logger.error(self.errs[(-1)])
            return False
        return True

    def exists(self, path):
        """ test if remote path is ok """
        command = SSH_CMD % (self.user, self.host, 'ls %s' % path)
        return self.cmd(command)

    def put(self, file):
        """ add a processing file """
        self.puts.append(file)

    def fire(self, done_path):
        """ synchronise queue """
        if os.path.exists(self.batch):
            raise SshError('There is a batch file in %s directory' % self.var)
        batch = open(self.batch, 'w')
        for file in self.puts:
            logger.debug('treat %s' % file)
            file_name = os.path.basename(file)
            remote_file_path = os.path.join(self.path, file_name)
            if not islock(file_name):
                lock_file = '%s.lock' % file
                try:
                    logger.debug('rename %s %s' % (file, lock_file))
                    os.rename(file, lock_file)
                except OSError, IOError:
                    __traceback_info__ = (
                     self, file, lock_file)
                    logger.exception('error failed to rename %s to %s ' % (file, lock_file))
                    batch.close()
                    os.unlink(self.batch)
                    raise

            else:
                logger.error('file %s is already locked, its not normal')
            file_lock_name = os.path.basename(lock_file)
            remote_lock_file = os.path.join(self.path, file_lock_name)
            done_file = os.path.join(done_path, file_name)
            batch.write('put %s %s\n' % (lock_file, self.path))
            batch.write('rename %s %s\n' % (remote_lock_file, remote_file_path))
            batch.write('!mv %s %s\n' % (lock_file, done_file))

        self.puts = []
        batch.close()
        command = 'sftp -b %s %s@%s' % (self.batch, self.user, self.host)
        self.cmd(command)
        os.unlink(self.batch)


class SshError(Exception):
    """ to deal with error """
    __module__ = __name__