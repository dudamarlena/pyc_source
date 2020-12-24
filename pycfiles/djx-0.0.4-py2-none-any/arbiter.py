# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/arbiter.py
# Compiled at: 2019-02-14 00:35:18
from __future__ import print_function
import errno, os, random, select, signal, sys, time, traceback
from gunicorn.errors import HaltServer, AppImportError
from gunicorn.pidfile import Pidfile
from gunicorn import sock, systemd, util
from gunicorn import __version__, SERVER_SOFTWARE

class Arbiter(object):
    """
    Arbiter maintain the workers processes alive. It launches or
    kills them if needed. It also manages application reloading
    via SIGHUP/USR2.
    """
    WORKER_BOOT_ERROR = 3
    APP_LOAD_ERROR = 4
    START_CTX = {}
    LISTENERS = []
    WORKERS = {}
    PIPE = []
    SIG_QUEUE = []
    SIGNALS = [ getattr(signal, 'SIG%s' % x) for x in ('HUP QUIT INT TERM TTIN TTOU USR1 USR2 WINCH').split()
              ]
    SIG_NAMES = dict((getattr(signal, name), name[3:].lower()) for name in dir(signal) if name[:3] == 'SIG' and name[3] != '_')

    def __init__(self, app):
        os.environ['SERVER_SOFTWARE'] = SERVER_SOFTWARE
        self._num_workers = None
        self._last_logged_active_worker_count = None
        self.log = None
        self.setup(app)
        self.pidfile = None
        self.systemd = False
        self.worker_age = 0
        self.reexec_pid = 0
        self.master_pid = 0
        self.master_name = 'Master'
        cwd = util.getcwd()
        args = sys.argv[:]
        args.insert(0, sys.executable)
        self.START_CTX = {'args': args, 
           'cwd': cwd, 
           0: sys.executable}
        return

    def _get_num_workers(self):
        return self._num_workers

    def _set_num_workers(self, value):
        old_value = self._num_workers
        self._num_workers = value
        self.cfg.nworkers_changed(self, value, old_value)

    num_workers = property(_get_num_workers, _set_num_workers)

    def setup(self, app):
        self.app = app
        self.cfg = app.cfg
        if self.log is None:
            self.log = self.cfg.logger_class(app.cfg)
        if 'GUNICORN_FD' in os.environ:
            self.log.reopen_files()
        self.worker_class = self.cfg.worker_class
        self.address = self.cfg.address
        self.num_workers = self.cfg.workers
        self.timeout = self.cfg.timeout
        self.proc_name = self.cfg.proc_name
        self.log.debug(('Current configuration:\n{0}').format(('\n').join(('  {0}: {1}').format(config, value.value) for config, value in sorted(self.cfg.settings.items(), key=lambda setting: setting[1]))))
        if self.cfg.env:
            for k, v in self.cfg.env.items():
                os.environ[k] = v

        if self.cfg.preload_app:
            self.app.wsgi()
        return

    def start(self):
        """        Initialize the arbiter. Start listening and set pidfile if needed.
        """
        self.log.info('Starting gunicorn %s', __version__)
        if 'GUNICORN_PID' in os.environ:
            self.master_pid = int(os.environ.get('GUNICORN_PID'))
            self.proc_name = self.proc_name + '.2'
            self.master_name = 'Master.2'
        self.pid = os.getpid()
        if self.cfg.pidfile is not None:
            pidname = self.cfg.pidfile
            if self.master_pid != 0:
                pidname += '.2'
            self.pidfile = Pidfile(pidname)
            self.pidfile.create(self.pid)
        self.cfg.on_starting(self)
        self.init_signals()
        if not self.LISTENERS:
            fds = None
            listen_fds = systemd.listen_fds()
            if listen_fds:
                self.systemd = True
                fds = range(systemd.SD_LISTEN_FDS_START, systemd.SD_LISTEN_FDS_START + listen_fds)
            elif self.master_pid:
                fds = []
                for fd in os.environ.pop('GUNICORN_FD').split(','):
                    fds.append(int(fd))

            self.LISTENERS = sock.create_sockets(self.cfg, self.log, fds)
        listeners_str = (',').join([ str(l) for l in self.LISTENERS ])
        self.log.debug('Arbiter booted')
        self.log.info('Listening at: %s (%s)', listeners_str, self.pid)
        self.log.info('Using worker: %s', self.cfg.worker_class_str)
        if hasattr(self.worker_class, 'check_config'):
            self.worker_class.check_config(self.cfg, self.log)
        self.cfg.when_ready(self)
        return

    def init_signals(self):
        """        Initialize master signal handling. Most of the signals
        are queued. Child signals only wake up the master.
        """
        for p in self.PIPE:
            os.close(p)

        self.PIPE = pair = os.pipe()
        for p in pair:
            util.set_non_blocking(p)
            util.close_on_exec(p)

        self.log.close_on_exec()
        for s in self.SIGNALS:
            signal.signal(s, self.signal)

        signal.signal(signal.SIGCHLD, self.handle_chld)

    def signal(self, sig, frame):
        if len(self.SIG_QUEUE) < 5:
            self.SIG_QUEUE.append(sig)
            self.wakeup()

    def run(self):
        """Main master loop."""
        self.start()
        util._setproctitle('master [%s]' % self.proc_name)
        try:
            self.manage_workers()
            while True:
                self.maybe_promote_master()
                sig = self.SIG_QUEUE.pop(0) if self.SIG_QUEUE else None
                if sig is None:
                    self.sleep()
                    self.murder_workers()
                    self.manage_workers()
                    continue
                if sig not in self.SIG_NAMES:
                    self.log.info('Ignoring unknown signal: %s', sig)
                    continue
                signame = self.SIG_NAMES.get(sig)
                handler = getattr(self, 'handle_%s' % signame, None)
                if not handler:
                    self.log.error('Unhandled signal: %s', signame)
                    continue
                self.log.info('Handling signal: %s', signame)
                handler()
                self.wakeup()

        except StopIteration:
            self.halt()
        except KeyboardInterrupt:
            self.halt()
        except HaltServer as inst:
            self.halt(reason=inst.reason, exit_status=inst.exit_status)
        except SystemExit:
            raise
        except Exception:
            self.log.info('Unhandled exception in main loop', exc_info=True)
            self.stop(False)
            if self.pidfile is not None:
                self.pidfile.unlink()
            sys.exit(-1)

        return

    def handle_chld(self, sig, frame):
        """SIGCHLD handling"""
        self.reap_workers()
        self.wakeup()

    def handle_hup(self):
        """        HUP handling.
        - Reload configuration
        - Start the new worker processes with a new configuration
        - Gracefully shutdown the old worker processes
        """
        self.log.info('Hang up: %s', self.master_name)
        self.reload()

    def handle_term(self):
        """SIGTERM handling"""
        raise StopIteration

    def handle_int(self):
        """SIGINT handling"""
        self.stop(False)
        raise StopIteration

    def handle_quit(self):
        """SIGQUIT handling"""
        self.stop(False)
        raise StopIteration

    def handle_ttin(self):
        """        SIGTTIN handling.
        Increases the number of workers by one.
        """
        self.num_workers += 1
        self.manage_workers()

    def handle_ttou(self):
        """        SIGTTOU handling.
        Decreases the number of workers by one.
        """
        if self.num_workers <= 1:
            return
        self.num_workers -= 1
        self.manage_workers()

    def handle_usr1(self):
        """        SIGUSR1 handling.
        Kill all workers by sending them a SIGUSR1
        """
        self.log.reopen_files()
        self.kill_workers(signal.SIGUSR1)

    def handle_usr2(self):
        """        SIGUSR2 handling.
        Creates a new master/worker set as a slave of the current
        master without affecting old workers. Use this to do live
        deployment with the ability to backout a change.
        """
        self.reexec()

    def handle_winch(self):
        """SIGWINCH handling"""
        if self.cfg.daemon:
            self.log.info('graceful stop of workers')
            self.num_workers = 0
            self.kill_workers(signal.SIGTERM)
        else:
            self.log.debug('SIGWINCH ignored. Not daemonized')

    def maybe_promote_master(self):
        if self.master_pid == 0:
            return
        else:
            if self.master_pid != os.getppid():
                self.log.info('Master has been promoted.')
                self.master_name = 'Master'
                self.master_pid = 0
                self.proc_name = self.cfg.proc_name
                del os.environ['GUNICORN_PID']
                if self.pidfile is not None:
                    self.pidfile.rename(self.cfg.pidfile)
                util._setproctitle('master [%s]' % self.proc_name)
            return

    def wakeup(self):
        """        Wake up the arbiter by writing to the PIPE
        """
        try:
            os.write(self.PIPE[1], '.')
        except IOError as e:
            if e.errno not in [errno.EAGAIN, errno.EINTR]:
                raise

    def halt(self, reason=None, exit_status=0):
        """ halt arbiter """
        self.stop()
        self.log.info('Shutting down: %s', self.master_name)
        if reason is not None:
            self.log.info('Reason: %s', reason)
        if self.pidfile is not None:
            self.pidfile.unlink()
        self.cfg.on_exit(self)
        sys.exit(exit_status)
        return

    def sleep(self):
        """        Sleep until PIPE is readable or we timeout.
        A readable PIPE means a signal occurred.
        """
        try:
            ready = select.select([self.PIPE[0]], [], [], 1.0)
            if not ready[0]:
                return
            while os.read(self.PIPE[0], 1):
                pass

        except (select.error, OSError) as e:
            error_number = getattr(e, 'errno', e.args[0])
            if error_number not in [errno.EAGAIN, errno.EINTR]:
                raise
        except KeyboardInterrupt:
            sys.exit()

    def stop(self, graceful=True):
        """        Stop workers

        :attr graceful: boolean, If True (the default) workers will be
        killed gracefully  (ie. trying to wait for the current connection)
        """
        unlink = self.reexec_pid == self.master_pid == 0 and not self.systemd
        sock.close_sockets(self.LISTENERS, unlink)
        self.LISTENERS = []
        sig = signal.SIGTERM
        if not graceful:
            sig = signal.SIGQUIT
        limit = time.time() + self.cfg.graceful_timeout
        self.kill_workers(sig)
        while self.WORKERS and time.time() < limit:
            time.sleep(0.1)

        self.kill_workers(signal.SIGKILL)

    def reexec(self):
        """        Relaunch the master and workers.
        """
        if self.reexec_pid != 0:
            self.log.warning('USR2 signal ignored. Child exists.')
            return
        if self.master_pid != 0:
            self.log.warning('USR2 signal ignored. Parent exists.')
            return
        master_pid = os.getpid()
        self.reexec_pid = os.fork()
        if self.reexec_pid != 0:
            return
        self.cfg.pre_exec(self)
        environ = self.cfg.env_orig.copy()
        environ['GUNICORN_PID'] = str(master_pid)
        if self.systemd:
            environ['LISTEN_PID'] = str(os.getpid())
            environ['LISTEN_FDS'] = str(len(self.LISTENERS))
        else:
            environ['GUNICORN_FD'] = (',').join(str(l.fileno()) for l in self.LISTENERS)
        os.chdir(self.START_CTX['cwd'])
        os.execvpe(self.START_CTX[0], self.START_CTX['args'], environ)

    def reload(self):
        old_address = self.cfg.address
        for k in self.cfg.env:
            if k in self.cfg.env_orig:
                os.environ[k] = self.cfg.env_orig[k]
            else:
                try:
                    del os.environ[k]
                except KeyError:
                    pass

        self.app.reload()
        self.setup(self.app)
        self.log.reopen_files()
        if old_address != self.cfg.address:
            for l in self.LISTENERS:
                l.close()

            self.LISTENERS = sock.create_sockets(self.cfg, self.log)
            listeners_str = (',').join([ str(l) for l in self.LISTENERS ])
            self.log.info('Listening at: %s', listeners_str)
        self.cfg.on_reload(self)
        if self.pidfile is not None:
            self.pidfile.unlink()
        if self.cfg.pidfile is not None:
            self.pidfile = Pidfile(self.cfg.pidfile)
            self.pidfile.create(self.pid)
        util._setproctitle('master [%s]' % self.proc_name)
        for _ in range(self.cfg.workers):
            self.spawn_worker()

        self.manage_workers()
        return

    def murder_workers(self):
        """        Kill unused/idle workers
        """
        if not self.timeout:
            return
        workers = list(self.WORKERS.items())
        for pid, worker in workers:
            try:
                if time.time() - worker.tmp.last_update() <= self.timeout:
                    continue
            except (OSError, ValueError):
                continue

            if not worker.aborted:
                self.log.critical('WORKER TIMEOUT (pid:%s)', pid)
                worker.aborted = True
                self.kill_worker(pid, signal.SIGABRT)
            else:
                self.kill_worker(pid, signal.SIGKILL)

    def reap_workers(self):
        """        Reap workers to avoid zombie processes
        """
        try:
            while True:
                wpid, status = os.waitpid(-1, os.WNOHANG)
                if not wpid:
                    break
                if self.reexec_pid == wpid:
                    self.reexec_pid = 0
                else:
                    exitcode = status >> 8
                    if exitcode == self.WORKER_BOOT_ERROR:
                        reason = 'Worker failed to boot.'
                        raise HaltServer(reason, self.WORKER_BOOT_ERROR)
                    if exitcode == self.APP_LOAD_ERROR:
                        reason = 'App failed to load.'
                        raise HaltServer(reason, self.APP_LOAD_ERROR)
                    worker = self.WORKERS.pop(wpid, None)
                    if not worker:
                        continue
                    worker.tmp.close()
                    self.cfg.child_exit(self, worker)

        except OSError as e:
            if e.errno != errno.ECHILD:
                raise

        return

    def manage_workers(self):
        """        Maintain the number of workers by spawning or killing
        as required.
        """
        if len(self.WORKERS.keys()) < self.num_workers:
            self.spawn_workers()
        workers = self.WORKERS.items()
        workers = sorted(workers, key=lambda w: w[1].age)
        while len(workers) > self.num_workers:
            pid, _ = workers.pop(0)
            self.kill_worker(pid, signal.SIGTERM)

        active_worker_count = len(workers)
        if self._last_logged_active_worker_count != active_worker_count:
            self._last_logged_active_worker_count = active_worker_count
            self.log.debug(('{0} workers').format(active_worker_count), extra={'metric': 'gunicorn.workers', 'value': active_worker_count, 
               'mtype': 'gauge'})

    def spawn_worker(self):
        self.worker_age += 1
        worker = self.worker_class(self.worker_age, self.pid, self.LISTENERS, self.app, self.timeout / 2.0, self.cfg, self.log)
        self.cfg.pre_fork(self, worker)
        pid = os.fork()
        if pid != 0:
            worker.pid = pid
            self.WORKERS[pid] = worker
            return pid
        for sibling in self.WORKERS.values():
            sibling.tmp.close()

        worker.pid = os.getpid()
        try:
            try:
                util._setproctitle('worker [%s]' % self.proc_name)
                self.log.info('Booting worker with pid: %s', worker.pid)
                self.cfg.post_fork(self, worker)
                worker.init_process()
                sys.exit(0)
            except SystemExit:
                raise
            except AppImportError as e:
                self.log.debug('Exception while loading the application', exc_info=True)
                print('%s' % e, file=sys.stderr)
                sys.stderr.flush()
                sys.exit(self.APP_LOAD_ERROR)
            except:
                self.log.exception('Exception in worker process')
                if not worker.booted:
                    sys.exit(self.WORKER_BOOT_ERROR)
                sys.exit(-1)

        finally:
            self.log.info('Worker exiting (pid: %s)', worker.pid)
            try:
                worker.tmp.close()
                self.cfg.worker_exit(self, worker)
            except:
                self.log.warning('Exception during worker exit:\n%s', traceback.format_exc())

    def spawn_workers(self):
        """        Spawn new workers as needed.

        This is where a worker process leaves the main loop
        of the master process.
        """
        for _ in range(self.num_workers - len(self.WORKERS.keys())):
            self.spawn_worker()
            time.sleep(0.1 * random.random())

    def kill_workers(self, sig):
        """        Kill all workers with the signal `sig`
        :attr sig: `signal.SIG*` value
        """
        worker_pids = list(self.WORKERS.keys())
        for pid in worker_pids:
            self.kill_worker(pid, sig)

    def kill_worker(self, pid, sig):
        """        Kill a worker

        :attr pid: int, worker pid
        :attr sig: `signal.SIG*` value
         """
        try:
            os.kill(pid, sig)
        except OSError as e:
            if e.errno == errno.ESRCH:
                try:
                    worker = self.WORKERS.pop(pid)
                    worker.tmp.close()
                    self.cfg.worker_exit(self, worker)
                    return
                except (KeyError, OSError):
                    return

            raise